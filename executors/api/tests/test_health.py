"""API 执行层：pytest + httpx，Flow 清单中的 test 节点指向本模块。"""

from __future__ import annotations

import os

import httpx
import pytest

PROBE_PATH = os.environ.get("API_PROBE_PATH", "/get")
MISSING_PATH = os.environ.get("API_MISSING_PATH", "/status/404")


@pytest.fixture(scope="session")
def api_base_url() -> str:
    base = os.environ.get("API_BASE_URL", "").strip()
    if not base:
        pytest.skip("API_BASE_URL is not configured")
    return base.rstrip("/")


@pytest.fixture(scope="session")
def http_client(api_base_url: str) -> httpx.Client:
    timeout = float(os.environ.get("API_TIMEOUT_SECONDS", "30"))
    with httpx.Client(base_url=api_base_url, timeout=timeout, follow_redirects=True) as client:
        yield client


def test_tc_api_health_001(http_client: httpx.Client) -> None:
    response = http_client.get(PROBE_PATH)
    assert 200 <= response.status_code < 300
    assert response.content


def test_tc_api_health_101(http_client: httpx.Client) -> None:
    response = http_client.get(MISSING_PATH)
    assert response.status_code == 404
