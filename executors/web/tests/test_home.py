"""Web 执行层：pytest-playwright，Flow 清单中的 test 节点指向本模块。"""

from __future__ import annotations

import os

import pytest

HOME_PATH = os.environ.get("WEB_HOME_PATH", "/")
HOME_TITLE = os.environ.get("WEB_HOME_TITLE_CONTAINS", "Example")
NOT_FOUND_PATH = os.environ.get("WEB_NOT_FOUND_PATH", "/this-path-does-not-exist-qa-template")


@pytest.fixture(scope="session")
def web_base_url() -> str:
    base = os.environ.get("WEB_BASE_URL", "").strip()
    if not base:
        pytest.skip("WEB_BASE_URL is not configured")
    return base.rstrip("/")


def test_tc_web_home_001(page, web_base_url: str) -> None:
    response = page.goto(f"{web_base_url}{HOME_PATH}", wait_until="domcontentloaded")
    assert response is not None
    assert response.ok
    assert HOME_TITLE.lower() in page.title().lower()


def test_tc_web_home_101(page, web_base_url: str) -> None:
    response = page.goto(f"{web_base_url}{NOT_FOUND_PATH}", wait_until="domcontentloaded")
    assert response is not None
    if response.status == 404:
        return
    content = page.content().lower()
    assert "not found" in content or "404" in content
