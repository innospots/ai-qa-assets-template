from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Reporter:
    def __init__(self, reports_dir: Path, templates_dir: Path) -> None:
        self.reports_dir = reports_dir
        self.templates_dir = templates_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def write(
        self,
        suite_name: str,
        results: List[Dict[str, Any]],
        meta: Optional[Dict[str, Any]] = None,
        nested_timestamp: bool = True,
    ) -> Dict[str, Path]:
        if nested_timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_dir = self.reports_dir / ts
        else:
            out_dir = self.reports_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        passed = sum(1 for r in results if r.get("verify", {}).get("passed"))
        failed = len(results) - passed
        summary = {
            "suite": suite_name,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "meta": meta or {},
            "results": results,
        }

        json_path = out_dir / "summary.json"
        json_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        html_path = out_dir / "report.html"
        self._write_html(html_path, summary)

        junit_path = out_dir / "junit.xml"
        self._write_junit(junit_path, suite_name, results)

        return {
            "dir": out_dir,
            "json": json_path,
            "html": html_path,
            "junit": junit_path,
        }

    def _write_html(self, path: Path, summary: Dict[str, Any]) -> None:
        env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("report.html.j2")
        path.write_text(template.render(summary=summary), encoding="utf-8")

    def _write_junit(
        self,
        path: Path,
        suite_name: str,
        results: List[Dict[str, Any]],
    ) -> None:
        suite = ET.Element(
            "testsuite",
            name=suite_name,
            tests=str(len(results)),
            failures=str(
                sum(1 for r in results if not r.get("verify", {}).get("passed"))
            ),
        )
        for item in results:
            case_id = item.get("case_id", "unknown")
            duration_s = (item.get("run", {}).get("duration_ms") or 0) / 1000.0
            tc = ET.SubElement(
                suite,
                "testcase",
                classname=item.get("module", "maestro"),
                name=case_id,
                time=f"{duration_s:.3f}",
            )
            verify = item.get("verify", {})
            if not verify.get("passed"):
                failed_checks = [
                    c
                    for c in verify.get("checks", [])
                    if not c.get("ok")
                ]
                msg = "; ".join(
                    f"{c.get('name')}={c.get('detail')}" for c in failed_checks
                ) or "verification failed"
                fail = ET.SubElement(tc, "failure", message=msg)
                fail.text = item.get("run", {}).get("stderr") or msg
        tree = ET.ElementTree(suite)
        tree.write(path, encoding="utf-8", xml_declaration=True)
