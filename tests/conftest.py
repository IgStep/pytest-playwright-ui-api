from collections.abc import Generator

import pytest
from faker import Faker
from playwright.sync_api import APIRequestContext, Playwright

from config import settings


@pytest.fixture()
def faker():
    return Faker()


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Generator[APIRequestContext]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        ),
    }
    request_context = playwright.request.new_context(
        base_url=f"{settings.qa.base_url}/api", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()
