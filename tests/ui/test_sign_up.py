from playwright.sync_api import expect


def test_sign_up(ui, faker):
    main_page = ui.main_page()
    main_page.open()
    main_page.signup_login_menu_item.click()

    signup_page = ui.signup_login_page()
    expect(signup_page.signup_heading).to_be_visible()
    signup_page.signup_name_field.fill(faker.user_name())
    signup_page.signup_email_field.fill(faker.email())
    signup_page.signup_button.click()

    signup_details = signup_page.signup_details
    expect(signup_details.details_title_text).to_be_visible()

    signup_details.sex_type_radiobutton.click()
    signup_details.first_name_field.fill(faker.first_name())
    signup_details.last_name_field.fill(faker.last_name())
    signup_details.password_field.fill(faker.password())
    signup_details.company_field.fill(faker.company())
    signup_details.address_field.fill(
        f"{faker.street_address()}, {faker.city()}, {faker.company()}"
    )
    signup_details.state_field.fill(faker.state())
    signup_details.city_field.fill(faker.city())
    signup_details.zipcode_field.fill(faker.zipcode())
    signup_details.mobile_number_field.fill(faker.phone_number())
    signup_details.create_account_button.click()
    expect(signup_details.account_created_text).to_be_visible()
