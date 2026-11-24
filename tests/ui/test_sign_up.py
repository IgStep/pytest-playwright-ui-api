from playwright.sync_api import expect

from api.assertions import assert_api_response


def test_sign_up(ui, new_user, accounts_client, cleanup_user):
    """Account is created through the UI, then verified and removed via API."""
    cleanup_user(new_user)

    main_page = ui.main_page()
    main_page.open()
    main_page.signup_login_menu_item.click()

    signup_page = ui.signup_login_page()
    expect(signup_page.signup_heading).to_be_visible()
    signup_page.signup_name_field.fill(new_user.name)
    signup_page.signup_email_field.fill(new_user.email)
    signup_page.signup_button.click()

    signup_details = signup_page.signup_details
    expect(signup_details.details_title_text).to_be_visible()

    signup_details.sex_type_radiobutton.click()
    signup_details.first_name_field.fill(new_user.firstname)
    signup_details.last_name_field.fill(new_user.lastname)
    signup_details.password_field.fill(new_user.password)
    signup_details.company_field.fill(new_user.company)
    signup_details.address_field.fill(new_user.address1)
    signup_details.state_field.fill(new_user.state)
    signup_details.city_field.fill(new_user.city)
    signup_details.zipcode_field.fill(new_user.zipcode)
    signup_details.mobile_number_field.fill(new_user.mobile_number)
    signup_details.create_account_button.click()
    expect(signup_details.account_created_text).to_be_visible()

    assert_api_response(
        accounts_client.verify_login(new_user.email, new_user.password),
        code=200,
        message="User exists!",
    )
