import re
from decimal import Decimal
from playwright.sync_api import Page, expect

URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"


def amount(text: str) -> Decimal:
    match = re.search(r"\$\s*(\d+\.\d{2})", text)
    assert match, f"Could not find price: {text}"
    return Decimal(match.group(1))


def login(page: Page, username: str):
    page.goto(URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()


def reset_app_state(page: Page):
    page.locator("#react-burger-menu-btn").click()
    page.locator("#reset_sidebar_link").click()

    close_button = page.locator("#react-burger-cross-btn")
    if close_button.is_visible():
        close_button.click()

    expect(page.locator(".shopping_cart_badge")).to_have_count(0)


def logout(page: Page):
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def product_details(product):
    name = product.locator(
        '[data-test="inventory-item-name"]'
    ).inner_text()

    price = amount(
        product.locator(
            '[data-test="inventory-item-price"]'
        ).inner_text()
    )

    return name, price


def checkout_and_verify(page: Page, expected_products):
    page.locator(".shopping_cart_link").click()

    cart_items = page.locator(".cart_item")
    expect(cart_items).to_have_count(len(expected_products))

    actual_cart = [
        product_details(cart_items.nth(i))
        for i in range(cart_items.count())
    ]

    assert sorted(actual_cart) == sorted(expected_products)

    page.locator('[data-test="checkout"]').click()

    page.locator('[data-test="firstName"]').fill("QA")
    page.locator('[data-test="lastName"]').fill("Student")
    page.locator('[data-test="postalCode"]').fill("1200")

    page.locator('[data-test="continue"]').click()

    overview_items = page.locator(".cart_item")
    expect(overview_items).to_have_count(len(expected_products))

    actual_products = [
        product_details(overview_items.nth(i))
        for i in range(overview_items.count())
    ]

    assert sorted(actual_products) == sorted(expected_products)

    expected_subtotal = sum(
        (price for _, price in expected_products),
        Decimal("0.00")
    )

    subtotal = amount(
        page.locator('[data-test="subtotal-label"]').inner_text()
    )

    tax = amount(
        page.locator('[data-test="tax-label"]').inner_text()
    )

    total = amount(
        page.locator('[data-test="total-label"]').inner_text()
    )

    assert subtotal == expected_subtotal
    assert total == subtotal + tax

    page.locator('[data-test="finish"]').click()

    expect(
        page.locator('[data-test="complete-header"]')
    ).to_have_text("Thank you for your order!")


def test_q1_locked_out_user_error(page: Page):
    login(page, "locked_out_user")

    expect(
        page.locator('[data-test="error"]')
    ).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )

    expect(
        page.locator('[data-test="login-button"]')
    ).to_be_visible()


def test_q2_standard_user_three_products(page: Page):
    login(page, "standard_user")

    expect(page).to_have_url(
        re.compile(r"/inventory\.html$")
    )

    reset_app_state(page)

    products = page.locator('[data-test="inventory-item"]')
    expect(products.first).to_be_visible()

    assert products.count() >= 3

    selected = []

    for i in range(3):
        product = products.nth(i)

        selected.append(product_details(product))

        product.get_by_role(
            "button", name="Add to cart"
        ).click()

    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_text("3")

    checkout_and_verify(page, selected)

    reset_app_state(page)
    logout(page)


def test_q3_performance_glitch_z_to_a(page: Page):
    page.set_default_timeout(60000)

    login(page, "performance_glitch_user")
    reset_app_state(page)

    page.locator(
        '[data-test="product-sort-container"]'
    ).select_option("za")

    products = page.locator('[data-test="inventory-item"]')

    names = [
        product.locator(
            '[data-test="inventory-item-name"]'
        ).inner_text()
        for product in products.all()
    ]

    assert names == sorted(names, reverse=True)

    first_product = products.first
    selected = [product_details(first_product)]

    first_product.get_by_role(
        "button", name="Add to cart"
    ).click()

    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    checkout_and_verify(page, selected)
    reset_app_state(page)
    logout(page)