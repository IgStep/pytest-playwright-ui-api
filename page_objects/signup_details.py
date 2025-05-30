from playwright.sync_api import Page


class SignupDetails:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.details_title_text = self.page.get_by_text("Enter Account Information")
        self.sex_type_radiobutton = page.get_by_role("radio", name="Mr.")  # Mr or Mrs
        self.first_name_field = page.get_by_role("textbox", name="First name *")
        self.last_name_field = page.get_by_role("textbox", name="Last name *")
        self.password_field = page.get_by_role("textbox", name="Password *")
        self.company_field = page.get_by_role("textbox", name="Company", exact=True)
        self.address_field = page.get_by_role(
            "textbox", name="Address * (Street address, P."
        )
        self.state_field = page.get_by_role("textbox", name="State *")
        self.city_field = page.get_by_role("textbox", name="City * Zipcode *")
        self.zipcode_field = page.locator("#zipcode")
        self.mobile_number_field = page.get_by_role("textbox", name="Mobile Number *")
        self.create_account_button = page.get_by_role("button", name="Create Account")
        self.account_created_text = page.get_by_text("Account Created!")
