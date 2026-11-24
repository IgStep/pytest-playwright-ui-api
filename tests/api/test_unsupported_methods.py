"""Unsupported HTTP methods.

The API rejects them in two different ways, and both are pinned here:
- catalog/lookup endpoints answer HTTP 200 with ``responseCode: 405`` in the body;
- account mutation endpoints (and PATCH anywhere) answer a real HTTP 405
  with a framework-style ``{"detail": ...}`` body.
"""

import pytest

from api.assertions import assert_api_response
from api.client import AccountsClient, ProductsClient
from api.models.responses import ApiMessage, HttpErrorDetail

pytestmark = pytest.mark.negative

SUPPORTED_METHODS = {
    ProductsClient.PRODUCTS_LIST: "GET",
    ProductsClient.BRANDS_LIST: "GET",
    ProductsClient.SEARCH_PRODUCT: "POST",
    AccountsClient.VERIFY_LOGIN: "POST",
    AccountsClient.USER_DETAIL_BY_EMAIL: "GET",
    AccountsClient.CREATE_ACCOUNT: "POST",
    AccountsClient.UPDATE_ACCOUNT: "PUT",
    AccountsClient.DELETE_ACCOUNT: "DELETE",
}
BODY_REPORTED_ENDPOINTS = {
    ProductsClient.PRODUCTS_LIST,
    ProductsClient.BRANDS_LIST,
    ProductsClient.SEARCH_PRODUCT,
    AccountsClient.VERIFY_LOGIN,
    AccountsClient.USER_DETAIL_BY_EMAIL,
}
METHODS = ("GET", "POST", "PUT", "DELETE", "PATCH")


def _unsupported(reported_in_body: bool) -> list:
    cases = []
    for endpoint, supported in SUPPORTED_METHODS.items():
        for method in METHODS:
            if method == supported:
                continue
            in_body = endpoint in BODY_REPORTED_ENDPOINTS and method != "PATCH"
            if in_body == reported_in_body:
                cases.append(pytest.param(method, endpoint, id=f"{method} {endpoint}"))
    return cases


@pytest.mark.parametrize(("method", "endpoint"), _unsupported(reported_in_body=True))
def test_unsupported_method_reported_in_body(products_client, method, endpoint):
    response = products_client.request(method, endpoint)

    assert_api_response(
        response,
        code=405,
        message="This request method is not supported.",
        model=ApiMessage,
    )


@pytest.mark.parametrize(("method", "endpoint"), _unsupported(reported_in_body=False))
def test_unsupported_method_rejected_with_http_405(products_client, method, endpoint):
    response = products_client.request(method, endpoint)

    error = assert_api_response(
        response, http_status=405, code=None, model=HttpErrorDetail
    )
    assert error.detail == f'Method "{method}" not allowed.'
