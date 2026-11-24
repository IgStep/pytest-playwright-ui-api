from api.client.base_client import ApiResponse, BaseApiClient


class ProductsClient(BaseApiClient):
    PRODUCTS_LIST = "productsList"
    BRANDS_LIST = "brandsList"
    SEARCH_PRODUCT = "searchProduct"

    def get_all_products(self) -> ApiResponse:
        return self.request("GET", self.PRODUCTS_LIST)

    def get_all_brands(self) -> ApiResponse:
        return self.request("GET", self.BRANDS_LIST)

    def search_product(self, term: str) -> ApiResponse:
        return self.request("POST", self.SEARCH_PRODUCT, form={"search_product": term})
