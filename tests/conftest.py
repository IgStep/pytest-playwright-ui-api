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
