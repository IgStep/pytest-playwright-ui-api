from playwright.sync_api import expect


def test_product_page_loaded(ui):
    product_page = ui.products_page()
    product_page.open()

    expect(product_page.search_field).to_be_visible()
    expect(product_page.all_products_heading).to_be_visible()
    expect(product_page.category_heading).to_be_visible()
