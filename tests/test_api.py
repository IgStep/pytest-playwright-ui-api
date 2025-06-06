def test_get_product_list(api):
    response = api.get("/productsList")
    assert response.ok
    assert response.status == 200


def test_all_brands_list(api):
    response = api.get("/brandsList")
    assert response.ok
    assert response.status == 200
    assert len(response.json()["brands"]) > 0
