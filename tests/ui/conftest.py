import pytest
from playwright.sync_api import Page

from config import settings
from page_objects.page_creator import PageCreator


@pytest.fixture
def ui(page: Page) -> PageCreator:
    # Built on pytest-playwright's `page`, so --browser, --browser-channel,
    # --headed, --screenshot, --tracing and --video all apply.
    return PageCreator(page, settings.qa.base_url)
