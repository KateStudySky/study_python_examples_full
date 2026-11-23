import pytest
from selenium import webdriver
from lesson_07.page.login_page import LoginPage
from lesson_07.page.main_shop_page import MainShopPage
from lesson_07.page.cart_page import CartPage
from lesson_07.page.checkout_page import CheckoutPage


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_shopping_cart(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    main_page = MainShopPage(driver)
    for item in [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]:
        main_page.add_to_cart(item)
    main_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_form("Иван", "Петров", "123456")
    total = checkout_page.get_total()

    assert total == "Total: $58.29"
