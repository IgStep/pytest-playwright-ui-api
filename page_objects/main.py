from playwright.sync_api import Locator, Page


class MainPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        # elements
        self.menu_items = self.page.locator(".shop-menu li")
        self.bottom_copyright_text = self.page.get_by_text(
            "Copyright © 2021 All rights"
        )
        self.signup_login_menu_item = self.page.get_by_role(
            "link", name="Signup / Login"
        )

    def logged_in_as(self, name: str) -> Locator:
        return self.page.get_by_text(f"Logged in as {name}")

    def open(self):
        self.page.goto(f"{self.url}/", wait_until="domcontentloaded")
