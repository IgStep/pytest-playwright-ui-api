import pytest

from api.assertions import assert_api_response
from api.client import ProductsClient
from api.models.responses import ProductsResponse


def _search(products_client: ProductsClient, term: str):
    return assert_api_response(
        products_client.search_product(term), model=ProductsResponse
    ).products


@pytest.mark.smoke
@pytest.mark.parametrize("term", ["top", "tshirt", "jean", "dress", "saree"])
def test_search_returns_only_matching_products(products_client, term):
    products = _search(products_client, term)

    assert products, f"No products found for {term!r}"
    # The API matches against both the product name and its category.
    mismatched = [
        p.name
        for p in products
        if term not in p.name.lower() and term not in p.category.category.lower()
    ]
    assert not mismatched, f"Products not matching {term!r}: {mismatched}"


def test_search_results_are_subset_of_catalog(products_client):
    catalog = assert_api_response(
        products_client.get_all_products(), model=ProductsResponse
    ).products

    found = _search(products_client, "top")

    assert set(found) <= set(catalog), "Search returned products missing from catalog"


def test_search_is_case_insensitive(products_client):
    lower = _search(products_client, "top")
    upper = _search(products_client, "TOP")

    assert [p.id for p in lower] == [p.id for p in upper]


def test_search_without_matches_returns_empty_list(products_client):
    assert _search(products_client, "no-such-product-xyz") == []


@pytest.mark.parametrize("term", ["", " "], ids=["empty", "whitespace"])
def test_blank_search_returns_whole_catalog(products_client, term):
    catalog = assert_api_response(
        products_client.get_all_products(), model=ProductsResponse
    ).products

    assert _search(products_client, term) == catalog


@pytest.mark.negative
def test_search_without_parameter_is_rejected(products_client):
    response = products_client.request("POST", ProductsClient.SEARCH_PRODUCT)

    assert_api_response(
        response,
        code=400,
        message="Bad request, search_product parameter is missing in POST request.",
    )
