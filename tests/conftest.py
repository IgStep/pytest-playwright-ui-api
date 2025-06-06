from faker import Faker
from typing import Generator
from config import settings
import pytest

from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    APIRequestContext,
)

from page_objects.page_creator import PageCreator


@pytest.fixture(scope="session")
def browser_type(
        playwright: Playwright, browser_name: str
) -> Generator[BrowserType, None, None]:
    browser_type = None
    if browser_name == "chromium":
        browser_type = playwright.chromium
    elif browser_name == "firefox":
        browser_type = playwright.firefox
    elif browser_name == "webkit":
        browser_type = playwright.webkit
    assert browser_type, f"Unkown browser name '{browser_name}'"
    yield browser_type


@pytest.fixture(scope="session")
def browser(browser_type: BrowserType) -> Generator[Browser, None, None]:
    browser = browser_type.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def ui(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    url = settings.qa.base_url
    yield PageCreator(page, url)
    page.close()


@pytest.fixture()
def faker():
    return Faker()


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/137.0.0.0 Safari/537.36"
        # "Authorization": f"token {API_TOKEN}",
    }
    request_context = playwright.request.new_context(
        base_url=f"{settings.qa.base_url}/api", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()
