from page_objects.main import MainPage
from page_objects.products import ProductsPage
from page_objects.signup_login import SignupLoginPage


class PageCreator:
    def __init__(self, page, url):
        self.page = page
        self.url = url

    def main_page(self):
        return MainPage(self.page, self.url)

    def signup_login_page(self):
        return SignupLoginPage(self.page, self.url)

    def products_page(self):
        return ProductsPage(self.page, self.url)
