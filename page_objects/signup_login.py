from playwright.sync_api import Page

from page_objects.signup_details import SignupDetails


class SignupLoginPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.signup_details = SignupDetails(self.page, self.url)
        # elements
        self.signup_heading = self.page.get_by_role("heading", name="New User Signup!")
        self.signup_name_field = self.page.get_by_role("textbox", name="Name")
        self.signup_email_field = (
            self.page.locator("form")
            .filter(has_text="Signup")
            .get_by_placeholder("Email Address")
        )
        self.signup_button = self.page.get_by_role("button", name="Signup")
        self.login_email_field = self.page.locator("[data-qa='login-email']")
        self.login_password_field = self.page.locator("[data-qa='login-password']")
        self.login_button = self.page.locator("[data-qa='login-button']")
        self.login_error_text = self.page.get_by_text(
            "Your email or password is incorrect!"
        )

    def open(self):
        self.page.goto(f"{self.url}/login", wait_until="domcontentloaded")

    def login(self, email: str, password: str):
        self.login_email_field.fill(email)
        self.login_password_field.fill(password)
        self.login_button.click()
