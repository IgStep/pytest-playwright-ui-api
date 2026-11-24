import pytest

from api.assertions import assert_api_response, assert_response_time
from api.models.responses import BrandsResponse, ProductsResponse
from config import settings

KNOWN_USER_TYPES = {"Women", "Men", "Kids"}


@pytest.mark.smoke
def test_get_all_products_returns_catalog(products_client):
    response = products_client.get_all_products()

    body = assert_api_response(response, model=ProductsResponse)
    assert body.products, "Product catalog is empty"
    assert_response_time(response, settings.qa.api_sla_ms)


def test_product_ids_are_unique(products_client):
    products = assert_api_response(
        products_client.get_all_products(), model=ProductsResponse
    ).products

    ids = [product.id for product in products]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    assert not duplicates, f"Duplicate product ids: {duplicates}"


def test_products_belong_to_known_user_types(products_client):
    products = assert_api_response(
        products_client.get_all_products(), model=ProductsResponse
    ).products

    unknown = {p.category.usertype.usertype for p in products} - KNOWN_USER_TYPES
    assert not unknown, f"Unexpected user types: {unknown}"


def test_every_product_brand_is_listed_in_brands(products_client):
    """Referential integrity between productsList and brandsList."""
    products = assert_api_response(
        products_client.get_all_products(), model=ProductsResponse
    ).products
    brands = assert_api_response(
        products_client.get_all_brands(), model=BrandsResponse
    ).brands

    unlisted = {p.brand for p in products} - {b.brand for b in brands}
    assert not unlisted, f"Product brands missing from brandsList: {unlisted}"
