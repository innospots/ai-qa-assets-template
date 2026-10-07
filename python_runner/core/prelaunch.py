from __future__ import annotations

import os
import subprocess
import time
from typing import List, Optional


def maestro_command(maestro_bin: str, *args: str) -> List[str]:
    """Windows 上可用 MAESTRO_BIN_WRAPPER 包一层 bash，以便调用无 .bat 的假 CLI。"""
    cmd = [maestro_bin, *args]
    wrapper = os.environ.get("MAESTRO_BIN_WRAPPER")
    if wrapper:
        return [wrapper, *cmd]
    return cmd


def check_adb(adb_bin: str = "adb") -> str:
    proc = subprocess.run(
        [adb_bin, "devices"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"adb 不可用: {proc.stderr or proc.stdout}")
    lines = [
        ln.strip()
        for ln in (proc.stdout or "").splitlines()
        if ln.strip() and not ln.startswith("List of devices")
    ]
    online = [ln for ln in lines if "\tdevice" in ln]
    if not online:
        raise RuntimeError("未检测到在线设备，请检查 USB 调试 / 模拟器")
    return online[0].split("\t", 1)[0]


def prelaunch(
    app_id: str,
    adb_bin: str = "adb",
    wait_seconds: int = 5,
) -> None:
    """MIUI 友好：用 adb monkey 前台拉起 App，绕过 Maestro 后台 Abort。"""
    monkey = [
        adb_bin,
        "shell",
        "monkey",
        "-p",
        app_id,
        "-c",
        "android.intent.category.LAUNCHER",
        "1",
    ]
    result = subprocess.run(
        monkey,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        am = [
            adb_bin,
            "shell",
            "am",
            "start",
            "-a",
            "android.intent.action.MAIN",
            "-c",
            "android.intent.category.LAUNCHER",
            "-p",
            app_id,
        ]
        subprocess.run(
            am,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    time.sleep(max(0, int(wait_seconds)))


def ensure_tools(
    maestro_bin: str = "maestro",
    adb_bin: str = "adb",
    require_adb: bool = True,
) -> None:
    bins = [("maestro", maestro_bin)]
    if require_adb:
        bins.append(("adb", adb_bin))
    for name, bin_name in bins:
        proc = subprocess.run(
            maestro_command(bin_name, "--version")
            if name == "maestro"
            else [bin_name, "version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if name == "adb":
            if proc.returncode != 0:
                check_adb(adb_bin)
        elif proc.returncode != 0:
            raise RuntimeError(
                f"{name} 不可用 ({bin_name}): {proc.stderr or proc.stdout}"
            )
