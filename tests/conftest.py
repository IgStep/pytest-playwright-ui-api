import logging
import os
import random
from collections.abc import Callable, Generator

import pytest
from faker import Faker
from playwright.sync_api import APIRequestContext, Playwright

from api.client import AccountsClient, ProductsClient
from api.data.factories import build_user
from api.models.user import UserData
from config import settings

logger = logging.getLogger(__name__)

TEST_LAYERS = ("api", "ui")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Tests are marked by folder (tests/api -> api, tests/ui -> ui).
    for item in items:
        layer = item.path.parent.name
        if layer in TEST_LAYERS:
            item.add_marker(layer)


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
def api_context(playwright: Playwright) -> Generator[APIRequestContext]:
    # The trailing slash matters: with "/api", a path like "/productsList"
    # resolves against the site root instead of the API.
    request_context = playwright.request.new_context(
        base_url=f"{settings.qa.base_url}/api/"
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def products_client(api_context: APIRequestContext) -> ProductsClient:
    return ProductsClient(api_context)


@pytest.fixture(scope="session")
def accounts_client(api_context: APIRequestContext) -> AccountsClient:
    return AccountsClient(api_context)


@pytest.fixture
def new_user(faker: Faker) -> UserData:
    """User data that is not registered yet."""
    return build_user(faker)


@pytest.fixture
def cleanup_user(
    accounts_client: AccountsClient,
) -> Generator[Callable[[UserData], None]]:
    """Register users for deletion after the test, whether it passes or fails.

    Use it for accounts created by the test itself (via API or UI).
    """
    users: list[UserData] = []
    yield users.append

    for user in users:
        response = accounts_client.delete_account(user.email, user.password)
        # 404 means the test already deleted the account (or never created it).
        if response.response_code not in (200, 404):
            logger.warning("Failed to delete test user %s: %s", user.email, response)


@pytest.fixture
def registered_user(
    accounts_client: AccountsClient,
    new_user: UserData,
    cleanup_user: Callable[[UserData], None],
) -> UserData:
    """User created via API as a precondition; deleted after the test."""
    response = accounts_client.create_account(new_user)
    assert response.response_code == 201, f"Precondition failed: {response}"
    cleanup_user(new_user)
    return new_user
