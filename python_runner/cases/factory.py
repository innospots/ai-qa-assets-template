from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

# 各语言文案：用于生成 data/<module>/locales.js
LOCALE_PRESETS: Dict[str, Dict[str, str]] = {
    "zh": {
        "langOption": "简体中文",
        "home": "首页",
        "recordings": "选择",
        "recording": "录音中",
        "processing": "1 条录音处理中",
        "endTranscribe": "结束并转写",
        "confirm": "确认",
        "confirmSpeaker": "确认当前说话人",
        "screenshotName": "saved_zh",
        "comment": "简体中文",
    },
    "en": {
        "langOption": "English",
        "home": "Home",
        "recordings": "Recordings",
        "recording": "Recording",
        "processing": "1 recording processing",
        "endTranscribe": "End & transcribe",
        "confirm": "Confirm",
        "confirmSpeaker": "Confirm current speaker",
        "screenshotName": "saved_en",
        "comment": "英文",
    },
    "ja": {
        "langOption": "日本語",
        "home": "ホーム",
        "recordings": "選択",
        "recording": "録音中",
        "processing": "1条録音処理中",
        "endTranscribe": "終了して文字起こし",
        "confirm": "確認",
        "confirmSpeaker": "現在の話者を確認",
        "screenshotName": "saved_ja",
        "comment": "日本語",
    },
}


def _js_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def render_locales_js(module: str, locales: List[str]) -> str:
    lines = [
        f"// 业务域：{module} 界面文案。",
        f"output.{module} = output.{module} || {{}};",
        f"output.{module}.locales = {{",
    ]
    for loc in locales:
        if loc not in LOCALE_PRESETS:
            raise KeyError(f"不支持的 locale: {loc}")
        p = LOCALE_PRESETS[loc]
        lines.append(f"  {loc}: {{")
        lines.append(f"    description: '{_js_escape(p['comment'])}界面文案',")
        for key in (
            "langOption",
            "home",
            "recordings",
            "recording",
            "processing",
            "endTranscribe",
            "confirm",
            "confirmSpeaker",
        ):
            lines.append(f"    {key}: '{_js_escape(p[key])}',")
        lines.append(f"    screenshotName: '{module}_{p['screenshotName']}'")
        lines.append("  },")
    lines.append("};")
    lines.append("")
    return "\n".join(lines)


def create_module_scaffold(
    workspace: Path,
    module: str,
    locales: Optional[List[str]] = None,
    overwrite: bool = False,
) -> List[Path]:
    """创建 Module 与 data 骨架；Case/Flow 需按 cases → flows 规范另行补齐。"""
    locales = locales or ["zh", "en", "ja"]
    created: list[Path] = []

    data_dir = workspace / "data" / module
    data_dir.mkdir(parents=True, exist_ok=True)
    locales_js = data_dir / "locales.js"
    if not locales_js.exists() or overwrite:
        locales_js.write_text(
            render_locales_js(module=module, locales=locales),
            encoding="utf-8",
        )
        created.append(locales_js)

    module_dir = workspace / "modules" / module
    module_dir.mkdir(parents=True, exist_ok=True)
    main_yaml = module_dir / "main.yaml"
    if not main_yaml.exists() or overwrite:
        main_yaml.write_text(
            "appId: ${APP_ID}\n"
            f"name: {module} 主操作\n"
            "---\n"
            f"# TODO: 实现 {module} 可复用动作；入口 Flow 放在 flows/{module}/\n"
            "- extendedWaitUntil:\n"
            "    visible: ${TEXT_HOME}\n"
            "    timeout: 15000\n",
            encoding="utf-8",
        )
        created.append(main_yaml)

    return created
