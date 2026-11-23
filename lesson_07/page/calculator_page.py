from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    def open(self):
        self.driver.get(self.URL)

    def set_delay(self, seconds):
        delay_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#delay"))
        )
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    def click_button(self, label):
        xpath = f"//span[text()='{label}']"
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()

    def get_result(self, expected_text):
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".screen"), expected_text
            )
        )
        return self.driver.find_element(
            By.CSS_SELECTOR, ".screen"
        ).text
