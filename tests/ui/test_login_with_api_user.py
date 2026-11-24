import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_login_with_user_created_via_api(ui, registered_user):
    """Precondition set up via API, so the test only exercises the login UI."""
    login_page = ui.signup_login_page()
    login_page.open()

    login_page.login(registered_user.email, registered_user.password)

    expect(ui.main_page().logged_in_as(registered_user.name)).to_be_visible()


def test_login_with_wrong_password_is_rejected(ui, registered_user):
    login_page = ui.signup_login_page()
    login_page.open()

    login_page.login(registered_user.email, "wrong-password")

    expect(login_page.login_error_text).to_be_visible()
