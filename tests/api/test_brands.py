import pytest

from api.assertions import assert_api_response, assert_response_time
from api.models.responses import BrandsResponse
from config import settings


@pytest.mark.smoke
def test_get_all_brands_returns_brands(products_client):
    response = products_client.get_all_brands()

    body = assert_api_response(response, model=BrandsResponse)
    assert body.brands, "Brands list is empty"
    assert_response_time(response, settings.qa.api_sla_ms)


def test_brand_ids_are_unique(products_client):
    brands = assert_api_response(
        products_client.get_all_brands(), model=BrandsResponse
    ).brands

    ids = [brand.id for brand in brands]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    assert not duplicates, f"Duplicate brand ids: {duplicates}"
