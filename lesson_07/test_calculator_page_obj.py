import pytest
from selenium import webdriver
from lesson_07.page.calculator_page import CalculatorPage


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_calculator(driver):
    page = CalculatorPage(driver)
    page.open()
    page.set_delay(4)

    for label in ["7", "+", "8", "="]:
        page.click_button(label)

    assert page.get_result("15") == "15"
