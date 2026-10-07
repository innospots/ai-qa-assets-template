from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from cases.base import TestCase

from .artifacts import latest_debug_dir, parse_debug_dir_from_output
from .prelaunch import maestro_command


@dataclass
class RunResult:
    case_id: str
    flow_path: str
    exit_code: int
    started_at: str
    ended_at: str
    duration_ms: int
    stdout: str
    stderr: str
    artifacts_dir: Optional[str]


class MaestroRunner:
    def __init__(
        self,
        workspace: Path,
        maestro_bin: str = "maestro",
        debug_root: Optional[Path] = None,
        app_id: str = "com.example.demo",
        device: Optional[str] = None,
        maestro_config: Optional[Path] = None,
        report_format: Optional[str] = None,
        report_output: Optional[Path] = None,
        debug_output: Optional[Path] = None,
        test_output_dir: Optional[Path] = None,
        extra_env: Optional[List[str]] = None,
    ) -> None:
        self.workspace = workspace
        self.maestro_bin = maestro_bin
        self.debug_root = debug_root
        self.app_id = app_id
        self.device = device
        self.maestro_config = maestro_config
        self.report_format = report_format
        self.report_output = report_output
        self.debug_output = debug_output
        self.test_output_dir = test_output_dir
        self.extra_env = extra_env or []

    def run(self, case: TestCase, flow_arg: Optional[str] = None) -> RunResult:
        if flow_arg:
            flow_cli = flow_arg
            flow = Path(flow_arg)
        else:
            flow = Path(case.flow_path)
            if not flow.is_absolute():
                flow = Path(str(self.workspace)) / case.flow_path
            flow_cli = str(flow)
        if not flow.exists():
            alt = Path(str(self.workspace)) / case.flow_path
            if alt.exists():
                flow = alt
                flow_cli = str(alt)
            else:
                raise FileNotFoundError(f"flow 不存在: {flow_cli}")

        cmd: List[str] = []
        if self.device:
            cmd.append(f"--device={self.device}")
        cmd.append("test")
        if self.maestro_config:
            cmd.append(f"--config={self.maestro_config}")
        if self.report_format:
            cmd.append(f"--format={self.report_format}")
        if self.report_output:
            cmd.append(f"--output={self.report_output}")
        if self.debug_output:
            cmd.append(f"--debug-output={self.debug_output}")
        if self.test_output_dir:
            cmd.append(f"--test-output-dir={self.test_output_dir}")
        cmd.extend(self.extra_env)
        has_app_id = any(item.startswith("APP_ID=") for item in self.extra_env)
        if not has_app_id:
            cmd.extend(["-e", f"APP_ID={self.app_id}"])
        cmd.append(flow_cli)
        started = datetime.now()
        proc = subprocess.run(
            maestro_command(self.maestro_bin, *cmd),
            cwd=str(self.workspace),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        ended = datetime.now()
        combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
        artifacts = parse_debug_dir_from_output(combined)
        if artifacts is None:
            if self.debug_output and Path(self.debug_output).exists():
                artifacts = Path(self.debug_output)
            elif self.debug_root is not None:
                artifacts = latest_debug_dir(self.debug_root, after=started)

        return RunResult(
            case_id=case.case_id,
            flow_path=case.flow_path,
            exit_code=proc.returncode,
            started_at=started.isoformat(timespec="seconds"),
            ended_at=ended.isoformat(timespec="seconds"),
            duration_ms=int((ended - started).total_seconds() * 1000),
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
            artifacts_dir=str(artifacts) if artifacts else None,
        )
