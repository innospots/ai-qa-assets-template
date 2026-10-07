from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cases import format_case_table, list_suites, select_cases
from cases.factory import create_module_scaffold
from core import MaestroRunner, Reporter, Verifier, check_adb, ensure_tools, prelaunch

WORKSPACE_DEFAULT = ROOT.parent
MAESTRO_ENV_KEYS = (
    "APP_ID",
    "TEST_ADMIN_PASSWORD",
    "TEST_MEMBER_PASSWORD",
    "TEST_DISABLED_PASSWORD",
)


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data


def load_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve() if args.workspace else WORKSPACE_DEFAULT
    cases = select_cases(
        suite=args.suite,
        case_id=args.case,
        tags=args.tags,
        flow_path=args.flow,
        workspace=workspace,
    )
    print(f"suites: {', '.join(list_suites(workspace))}")
    print(format_case_table(cases))
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    cfg = load_config(Path(args.config).resolve())
    workspace = Path(args.workspace or cfg.get("workspace") or WORKSPACE_DEFAULT).resolve()
    created = create_module_scaffold(
        workspace=workspace,
        module=args.module,
        locales=args.locales,
        overwrite=bool(args.overwrite),
    )
    if not created:
        print("没有新建文件（目标已存在且未指定 --overwrite）")
        return 0
    print("已创建:")
    for p in created:
        print(f"  - {p}")
    print(
        "提示: 请补齐 modules/<module>/main.yaml，编写 cases/{module}/"
        " 与 flows/{module}/ 后再 run。"
    )
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config).resolve()
    cfg = load_config(cfg_path)

    workspace = Path(
        args.workspace or cfg.get("workspace") or WORKSPACE_DEFAULT
    ).resolve()
    env_values: Dict[str, str] = {}
    if args.env_file:
        env_path = Path(args.env_file)
        if not env_path.is_absolute():
            env_path = (workspace / env_path).resolve()
        env_values = load_env_file(env_path)

    reports_dir = Path(
        args.reports_dir
        or cfg.get("reports_dir")
        or (workspace / "artifacts" / "maestro")
    ).resolve()
    templates_dir = ROOT / "templates"
    maestro_bin = (
        args.maestro_bin
        or os.environ.get("MAESTRO_BIN")
        or cfg.get("maestro_bin")
        or "maestro"
    )
    adb_bin = args.adb_bin or cfg.get("adb_bin") or "adb"
    app_id = (
        args.app_id
        or env_values.get("APP_ID")
        or cfg.get("app_id")
        or "com.example.demo"
    )
    wait_s = int(cfg.get("prelaunch_wait_seconds", 5))
    debug_root = None
    if args.debug_output:
        debug_root = Path(args.debug_output)
    elif cfg.get("maestro_debug_root"):
        debug_root = Path(cfg["maestro_debug_root"])

    platform = (args.platform or "android").lower()
    skip_prelaunch = bool(args.skip_prelaunch) or os.environ.get(
        "MAESTRO_SKIP_PRELAUNCH", ""
    ) in {"1", "true", "TRUE"}
    require_adb = platform == "android" and not skip_prelaunch
    ensure_tools(maestro_bin=maestro_bin, adb_bin=adb_bin, require_adb=require_adb)

    device = args.device or env_values.get("MAESTRO_DEVICE") or ""
    if require_adb:
        device = check_adb(adb_bin) or device
    print(f"[env] platform={platform} device={device or '-'} workspace={workspace}")

    extra_env: List[str] = []
    for key in MAESTRO_ENV_KEYS:
        value = env_values.get(key)
        if value:
            extra_env.extend(["-e", f"{key}={value}"])

    cases = select_cases(
        suite=args.suite,
        case_id=args.case,
        tags=args.tags,
        flow_path=args.flow,
        workspace=workspace,
    )
    if not cases:
        if args.tags:
            print(f"没有匹配 tags={args.tags} 的用例，跳过", file=sys.stderr)
            return 0
        print("没有匹配到用例", file=sys.stderr)
        return 2

    runner = MaestroRunner(
        workspace=workspace,
        maestro_bin=maestro_bin,
        debug_root=debug_root,
        app_id=app_id,
        device=device or None,
        maestro_config=Path(args.maestro_config) if args.maestro_config else workspace / ".maestro" / "config.yaml",
        report_format=args.format,
        report_output=Path(args.output) if args.output else None,
        debug_output=Path(args.debug_output) if args.debug_output else None,
        test_output_dir=Path(args.test_output_dir) if args.test_output_dir else None,
        extra_env=extra_env,
    )
    verifier = Verifier(workspace=workspace)
    reporter = Reporter(reports_dir=reports_dir, templates_dir=templates_dir)
    flat = bool(args.flat_reports)

    results: List[Dict[str, Any]] = []
    for case in cases:
        print(f"\n=== RUN {case.case_id} ({case.flow_path}) ===")
        if case.prelaunch and require_adb and not skip_prelaunch:
            print(f"[prelaunch] {app_id}")
            prelaunch(app_id=app_id, adb_bin=adb_bin, wait_seconds=wait_s)

        run = runner.run(
            case,
            flow_arg=args.flow if args.flow and len(cases) == 1 else None,
        )
        verify = verifier.verify(case, run)
        status = "PASS" if verify.passed else "FAIL"
        print(
            f"[{status}] exit={run.exit_code} "
            f"duration={run.duration_ms}ms artifacts={run.artifacts_dir}"
        )
        for c in verify.checks:
            mark = "OK" if c.ok else "NG"
            print(f"  - [{mark}] {c.name}: {c.detail}")

        results.append(
            {
                "case_id": case.case_id,
                "module": case.module,
                "locale": case.locale,
                "tags": case.tags,
                "description": case.description,
                "flow_path": case.flow_path,
                "run": asdict(run),
                "verify": verify.to_dict(),
            }
        )

    suite_name = args.suite or args.case or args.flow or "selected"
    if args.tags:
        suite_name = args.tags[0] if len(args.tags) == 1 else ",".join(args.tags)
    paths = reporter.write(
        suite_name=str(suite_name),
        results=results,
        meta={
            "device": device,
            "workspace": str(workspace),
            "platform": platform,
        },
        nested_timestamp=not flat,
    )
    print("\n=== REPORT ===")
    for k, p in paths.items():
        print(f"{k}: {p}")

    failed = [r for r in results if not r["verify"]["passed"]]
    if not failed:
        return 0
    codes = [int(r["run"].get("exit_code") or 1) for r in failed]
    nonzero = [c for c in codes if c]
    return nonzero[0] if nonzero else 1


def _add_select_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--workspace", default=None, help="仓库根目录")
    p.add_argument("--suite", default=None, help="领域目录名，如 recording、chat")
    p.add_argument("--case", default=None, help="单个 Case ID，与 Flow 文件名一致")
    p.add_argument("--flow", default=None, help="单个 Flow 路径")
    p.add_argument(
        "--tags",
        nargs="*",
        default=None,
        help="按 Flow tags 过滤，如 smoke",
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Maestro 编排层：由 scripts/maestro 调用，执行 Flow 并生成报告",
    )
    p.add_argument(
        "--config",
        default=str(ROOT / "config.yaml"),
        help="python_runner 配置文件",
    )
    sub = p.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="列出 flows/journeys 中的用例")
    _add_select_args(list_p)
    list_p.set_defaults(func=cmd_list)

    run_p = sub.add_parser("run", help="执行用例并输出报告")
    _add_select_args(run_p)
    run_p.add_argument("--platform", default="android", help="android 或 ios")
    run_p.add_argument("--env-file", default=None, help="env/*.env 文件")
    run_p.add_argument("--device", default=None, help="Maestro --device")
    run_p.add_argument("--maestro-bin", default=None, help="maestro 可执行文件")
    run_p.add_argument("--adb-bin", default=None, help="adb 可执行文件")
    run_p.add_argument("--app-id", default=None, help="覆盖 APP_ID")
    run_p.add_argument("--maestro-config", default=None, help=".maestro/config.yaml")
    run_p.add_argument("--format", default=None, help="Maestro 报告格式 JUNIT 或 HTML")
    run_p.add_argument("--output", default=None, help="Maestro --output")
    run_p.add_argument("--debug-output", default=None, help="Maestro --debug-output")
    run_p.add_argument("--test-output-dir", default=None, help="Maestro --test-output-dir")
    run_p.add_argument("--reports-dir", default=None, help="Python 汇总报告目录")
    run_p.add_argument(
        "--flat-reports",
        action="store_true",
        help="报告直接写入 reports-dir，不再套时间戳子目录",
    )
    run_p.add_argument(
        "--skip-prelaunch",
        action="store_true",
        help="跳过 adb 预启动",
    )
    run_p.set_defaults(func=cmd_run)

    create_p = sub.add_parser("create", help="为新模块生成 Module/data 骨架")
    create_p.add_argument("--workspace", default=None, help="仓库根目录")
    create_p.add_argument("--module", required=True, help="模块名，如 chat")
    create_p.add_argument(
        "--locales",
        nargs="*",
        default=["zh", "en", "ja"],
        help="语言列表，默认 zh en ja",
    )
    create_p.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖已存在的 locale/data 文件",
    )
    create_p.set_defaults(func=cmd_create)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
