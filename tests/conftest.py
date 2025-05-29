from config import settings
import pytest
from playwright.sync_api import Page

from page_objects.page_creator import PageCreator


@pytest.fixture()
def ui(page: Page):
    url = settings.qa.base_url
    yield PageCreator(page, url)
