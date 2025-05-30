class ProductsPage:
    def __init__(self, page, url):
        self.page = page
        self.url = url
        self.search_field = page.get_by_role("textbox", name="Search Product")
        self.all_products_heading = page.get_by_role("heading", name="All Products")
        self.category_heading = page.get_by_role("heading", name="Category")
        self.brands_heading = page.get_by_role("heading", name="Brands")

    def open(self):
        self.page.goto(f"{self.url}/products", wait_until="domcontentloaded")
