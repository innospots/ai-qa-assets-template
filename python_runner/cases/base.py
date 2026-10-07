from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Expectation:
    """用例期望：执行后校验规则。"""

    exit_code: int = 0
    screenshot_names: List[str] = field(default_factory=list)
    # exit_code==0 时，日志中不应再出现这些模式
    forbid_log_patterns: List[str] = field(
        default_factory=lambda: ["CommandFailed"]
    )


@dataclass
class TestCase:
    """一条可执行用例：元数据 + Maestro flow 路径。"""

    case_id: str
    module: str
    flow_path: str
    locale: str
    tags: List[str] = field(default_factory=list)
    prelaunch: bool = True
    description: str = ""
    expect: Expectation = field(default_factory=Expectation)
