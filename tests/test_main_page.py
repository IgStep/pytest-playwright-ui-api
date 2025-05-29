from playwright.sync_api import expect


def test_check_main_page_loaded(ui):
    main_page = ui.main_page()
    main_page.open()
    expect(main_page.bottom_copyright_text).to_be_visible()


def test_check_menu_items_number(ui):
    expected_menu_items_number = 8

    main_page = ui.main_page()
    main_page.open()
    expect(main_page.menu_items).to_have_count(expected_menu_items_number)
