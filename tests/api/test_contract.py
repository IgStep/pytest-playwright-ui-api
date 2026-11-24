"""Contract tests: every endpoint's payload against its strict schema.

Models forbid unknown fields, so any added, removed or retyped field fails
here. Run alone as a fast gate with ``pytest -m contract``.
"""

import pytest

from api.assertions import assert_api_response
from api.client import AccountsClient, ProductsClient
from api.models.responses import (
    ApiMessage,
    BrandsResponse,
    ProductsResponse,
    UserDetailResponse,
)

pytestmark = pytest.mark.contract


def test_products_list_contract(products_client):
    assert_api_response(products_client.get_all_products(), model=ProductsResponse)


def test_brands_list_contract(products_client):
    assert_api_response(products_client.get_all_brands(), model=BrandsResponse)


def test_search_product_contract(products_client):
    assert_api_response(products_client.search_product("top"), model=ProductsResponse)


def test_user_detail_contract(accounts_client, registered_user):
    assert_api_response(
        accounts_client.get_user_detail_by_email(registered_user.email),
        model=UserDetailResponse,
    )


@pytest.mark.parametrize(
    ("method", "endpoint", "code"),
    [
        ("POST", ProductsClient.SEARCH_PRODUCT, 400),
        ("POST", AccountsClient.VERIFY_LOGIN, 400),
        ("GET", AccountsClient.USER_DETAIL_BY_EMAIL, 400),
        ("POST", AccountsClient.CREATE_ACCOUNT, 400),
        ("DELETE", AccountsClient.DELETE_ACCOUNT, 400),
        ("POST", ProductsClient.PRODUCTS_LIST, 405),
    ],
)
def test_error_envelope_contract(products_client, method, endpoint, code):
    assert_api_response(
        products_client.request(method, endpoint), code=code, model=ApiMessage
    )
