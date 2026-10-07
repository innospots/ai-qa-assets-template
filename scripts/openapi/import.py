#!/usr/bin/env python3
"""用途：将本地 OpenAPI 3.x 文件中的指定接口转换为待审查测试资产草稿。

参数：--spec 文件、--domain 业务域、--operation METHOD /path 或 --all、--output 输出目录。
输出：每个接口一个独立草稿包；已存在的草稿不会被覆盖。
限制：仅解析本地 YAML/JSON；不推断业务预期，不解析外部 $ref，不生成可直接运行的正式测试。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml


METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
DOMAIN_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
ROOT = Path(__file__).resolve().parents[2]


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从本地 OpenAPI 3.x 文件创建 API 测试资产草稿")
    parser.add_argument("--spec", required=True, type=Path, help="本地 YAML/JSON 规范文件")
    parser.add_argument("--domain", help="业务域 slug，例如 catalog")
    parser.add_argument("--output", type=Path, default=ROOT / "generated" / "openapi-drafts")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--operation", help="显式选择 METHOD /path，例如 GET /items/{id}")
    group.add_argument("--all", action="store_true", help="显式选择全部接口")
    group.add_argument("--list", action="store_true", help="只列出接口，不创建草稿")
    return parser.parse_args()


def load_spec(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"规范文件不存在：{path}")
    if path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("规范文件超过 10 MiB 上限")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"无法解析 OpenAPI 文件：{exc}") from exc
    if not isinstance(data, dict) or not re.fullmatch(r"3\.(?:0|1)\.[0-9]+(?:[-+].*)?", str(data.get("openapi", ""))):
        raise ValueError("仅支持 OpenAPI 3.0/3.1 YAML 或 JSON")
    if not isinstance(data.get("paths"), dict):
        raise ValueError("OpenAPI paths 必须是对象")
    return data


def operations(spec: dict) -> dict[str, tuple[str, str, dict, dict]]:
    found = {}
    for path, path_item in spec["paths"].items():
        if not isinstance(path, str) or not path.startswith("/") or not isinstance(path_item, dict):
            raise ValueError(f"无效的 path item：{path!r}")
        for method, operation in path_item.items():
            if str(method).lower() not in METHODS:
                continue
            if not isinstance(operation, dict):
                raise ValueError(f"无效的接口定义：{method} {path}")
            key = f"{method.upper()} {path}"
            found[key] = (str(method).upper(), path, path_item, operation)
    return dict(sorted(found.items()))


def operation_slug(method: str, path: str) -> str:
    parts = ["by-" + m.group(1) if (m := re.fullmatch(r"\{([^{}]+)\}", part)) else part for part in path.strip("/").split("/")]
    raw = "-".join([method.lower(), *parts])
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")[:70].rstrip("-")
    digest = hashlib.sha256(f"{method} {path}".encode()).hexdigest()[:8]
    return f"{slug or method.lower()}-{digest}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_bundle(target: Path, domain: str, spec: dict, source: Path, item: tuple[str, str, dict, dict]) -> None:
    method, path, path_item, operation = item
    scene = operation_slug(method, path)
    stem = f"{domain.upper().replace('-', '-')}-{scene.upper()}"
    ds_id = f"DS-{stem}-001"
    tc_id = f"TC-{stem}-001"
    test_name = f"test_{tc_id.lower().replace('-', '_')}"
    test_file = f"test_{scene.replace('-', '_')}.py"
    title = str(operation.get("summary") or f"{method} {path}").replace("\n", " ").replace("|", "\\|")
    required = [
        {"name": p.get("name"), "in": p.get("in"), "schema": p.get("schema")}
        for p in [*(path_item.get("parameters") or []), *(operation.get("parameters") or [])]
        if isinstance(p, dict) and p.get("required") is True
    ]
    source_label = f"{method} {path}"
    notice = "> **待审查草稿**：OpenAPI 只提供接口契约；业务预期、数据、鉴权和清理策略须按需求确认后进入正式资产。\n"

    write(target / "README.md", f"# {source_label} 测试资产草稿\n\n来源：`{source.name}`；选择键：`{source_label}`。\n\n{notice}\n审核顺序：核对需求与接口契约 → 完成 TDS → 完成 Case 业务预期和数据 → 实现 pytest 断言 → 将资产移入正式目录 → 执行校验与单 Flow。当前 pytest 骨架会跳过执行。\n\n业务域目录为 `{domain}`；data Object 命名空间为 `output.{domain.replace('-', '_')}`。`resources/operation.json` 保存当前接口、路径参数和组件快照，供评审查阅；外部 `$ref` 不会自动解析。\n")
    write(target / "designs" / domain / "index.md", f"# {domain} 模块草稿索引\n\n{notice}\n| 场景 | 接口选择键 | 来源 |\n| --- | --- | --- |\n| [{scene}]({scene}.design.md) | `{source_label}` | `{source.name}` |\n")
    write(target / "designs" / domain / f"{scene}.design.md", f"# {title} 测试设计草稿\n\n{notice}\n## 来源与范围\n\n- OpenAPI：`{source.name}` → `{source_label}`\n- operationId：`{operation.get('operationId', '未提供')}`（仅辅助命名）\n- 响应状态：{', '.join(map(str, (operation.get('responses') or {}).keys())) or '未声明'}\n\n## 场景意图\n\n| DS ID | 意图 | 状态 |\n| --- | --- | --- |\n| {ds_id} | 根据接口契约及需求确认 {title} 的成功路径 | 待确认 |\n\n## 风险与待确认\n\n- 成功与失败的业务预期、权限、边界及优先级。\n- 请求数据、前置状态、清理策略和响应断言。\n- `$ref`、鉴权与服务地址的实际解析方式。\n")
    write(target / "cases" / domain / f"{scene}.case.md", f"---\nid: {stem}\nname: {json.dumps(title, ensure_ascii=False)}\nmodule: {domain}\nscene: {scene}\nsource:\n  tds: {stem}-DESIGN\npriority: P1\ntags: [{domain}, regression]\nplatform: [api]\nstatus: draft\n---\n\n# {title} 用例草稿\n\n{notice}\n## 测试用例清单\n\n| Case ID | TDS 意图 | 状态 |\n| --- | --- | --- |\n| {tc_id} | {ds_id} | 待确认 |\n\n## 测试数据\n\n- 路径与方法见 `data/{domain}/{scene}.js`；实际请求值待确认。\n- 必填参数：{', '.join(str(p['name']) for p in required) or '规范未声明'}。\n\n## 正向测试\n\n### {tc_id} {title}\n\n- **追溯**：{ds_id}\n- **步骤**：准备经确认的请求数据并调用 `{source_label}`。\n- **预期结果**：待结合需求确认；不得仅凭响应状态自动认定业务成功。\n\n## 反向测试\n\n- 待结合需求、权限与错误契约补充，不从 OpenAPI 自行推断。\n")
    write(target / "flows" / domain / scene / f"{tc_id}.yaml", f"executor: api\nname: {json.dumps(tc_id + ' ' + title, ensure_ascii=False)}\ntags: [{domain}, regression, positive, p1, draft]\ntest: executors/api/tests/{test_file}::{test_name}\n")
    js_data = {"path": path, "method": method, "requiredParameters": required}
    write(target / "data" / domain / f"{scene}.js", f"// 接口契约快照；请求示例及业务值待评审后填写。\noutput.{domain.replace('-', '_')} = output.{domain.replace('-', '_')} || {{}};\noutput.{domain.replace('-', '_')}.operation = {json.dumps(js_data, ensure_ascii=False, indent=2, default=str)};\n")
    write(target / "env" / "api.env.example", "# 目标环境地址与敏感值由本地或 CI 提供；不要提交真实值。\nAPI_BASE_URL=\n")
    write(target / "executors" / "api" / "tests" / test_file, f'''"""{source_label} 的待审查执行骨架；业务断言确认前不运行请求。"""\n\nimport pytest\n\n\ndef {test_name}():\n    pytest.skip("待确认：请求数据、鉴权、业务预期和清理策略")\n''')
    contract = {
        "openapi": spec["openapi"], "info": spec.get("info"), "servers": spec.get("servers"),
        "security": spec.get("security"), "method": method, "path": path,
        "pathParameters": path_item.get("parameters", []), "operation": operation,
        "components": spec.get("components", {}),
    }
    write(target / "resources" / "operation.json", json.dumps(contract, ensure_ascii=False, indent=2, default=str) + "\n")


def main() -> int:
    args = arguments()
    try:
        spec = load_spec(args.spec)
        found = operations(spec)
        if args.list:
            for key in found:
                print(key)
            return 0
        if not args.domain or not DOMAIN_PATTERN.fullmatch(args.domain):
            raise ValueError("--domain 必须是小写业务域 slug（例如 catalog）")
        if not found:
            raise ValueError("规范中没有可导入接口")
        key = args.operation.strip() if args.operation else None
        if key:
            match = re.fullmatch(r"([A-Za-z]+)\s+(/\S*)", key)
            key = f"{match.group(1).upper()} {match.group(2)}" if match else key
            if key not in found:
                raise ValueError(f"接口不存在：{key}；可使用 --list 查看选择键")
        selected = {key: found[key]} if key else found
        targets = [(args.output / args.domain / operation_slug(item[0], item[1]), item) for item in selected.values()]
        existing = [path for path, _ in targets if path.exists()]
        if existing:
            raise ValueError("草稿已存在，不会覆盖：" + ", ".join(str(p) for p in existing))
        for target, item in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = Path(tempfile.mkdtemp(prefix=".openapi-draft-", dir=target.parent))
            try:
                build_bundle(temporary, args.domain, spec, args.spec, item)
                temporary.rename(target)
            finally:
                if temporary.exists():
                    shutil.rmtree(temporary)
            print(target)
        return 0
    except (ValueError, OSError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
