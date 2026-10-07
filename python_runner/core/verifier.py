from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from cases.base import TestCase

from .artifacts import collect_log_text, find_screenshot
from .runner import RunResult


@dataclass
class CheckItem:
    name: str
    ok: bool
    detail: Any = ""


@dataclass
class VerifyResult:
    passed: bool
    checks: List[CheckItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": [
                {"name": c.name, "ok": c.ok, "detail": c.detail} for c in self.checks
            ],
        }


class Verifier:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    def verify(self, case: TestCase, run: RunResult) -> VerifyResult:
        checks: List[CheckItem] = []

        ok_exit = run.exit_code == case.expect.exit_code
        checks.append(
            CheckItem(
                name="exit_code",
                ok=ok_exit,
                detail=f"actual={run.exit_code}, expected={case.expect.exit_code}",
            )
        )

        artifacts = Path(run.artifacts_dir) if run.artifacts_dir else None
        for shot in case.expect.screenshot_names:
            found = find_screenshot(artifacts, self.workspace, shot)
            checks.append(
                CheckItem(
                    name=f"screenshot:{shot}",
                    ok=found is not None,
                    detail=str(found) if found else "not found",
                )
            )

        log_text = collect_log_text(artifacts)
        log_text += "\n" + (run.stdout or "") + "\n" + (run.stderr or "")
        if run.exit_code == 0:
            for pat in case.expect.forbid_log_patterns:
                hit = re.search(pat, log_text)
                checks.append(
                    CheckItem(
                        name=f"log_not:{pat}",
                        ok=hit is None,
                        detail="found" if hit else "clean",
                    )
                )

        # flow 文件存在性（创建阶段保障，执行后再确认）
        flow = self.workspace / case.flow_path
        checks.append(
            CheckItem(
                name="flow_exists",
                ok=flow.exists(),
                detail=str(flow),
            )
        )

        return VerifyResult(passed=all(c.ok for c in checks), checks=checks)
