import logging
import os
import random
from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from config import settings

logger = logging.getLogger(__name__)


@pytest.fixture
def faker_seed(request: pytest.FixtureRequest) -> int:
    """Random seed per test, logged so a failure can be replayed via FAKER_SEED.

    Overrides the faker plugin's default fixed seed (0), which would give every
    test identical data.
    """
    seed = int(os.environ.get("FAKER_SEED", random.randrange(1_000_000)))
    logger.info("Faker seed for %s: %s", request.node.nodeid, seed)
    return seed


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
