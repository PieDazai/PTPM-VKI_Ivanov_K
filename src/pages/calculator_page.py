from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class CalculatorPage:
    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"

    # --- Локаторы (приватные) ---
    _FIRST_INPUT = (By.CSS_SELECTOR, 'input[ng-model="a"]')
    _SECOND_INPUT = (By.CSS_SELECTOR, 'input[ng-model="b"]')
    _OPERATION_SELECT = (By.CSS_SELECTOR, 'select[ng-model="operation"]')
    _RESULT = (By.CSS_SELECTOR, 'b.result')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Внутренний помощник ---

    def _set_number(self, locator, value):
        field = self.wait.until(EC.element_to_be_clickable(locator))
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(str(value))

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self._FIRST_INPUT))
        return self

    def enter_first_number(self, value):
        self._set_number(self._FIRST_INPUT, value)

    def enter_second_number(self, value):
        self._set_number(self._SECOND_INPUT, value)

    def select_operation(self, op):
        if op not in ("+", "-", "*", "/"):
            raise ValueError(f"Неизвестная операция: {op}")
        select = Select(
            self.wait.until(EC.element_to_be_clickable(self._OPERATION_SELECT))
        )
        select.select_by_value(op)

    def get_result_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self._RESULT))
        return element.text.strip()

    def get_result_value(self):
        text = self.get_result_text()
        return float(text.split("=")[1].strip())

    def calculate(self, a, b, op):
        self.enter_first_number(a)
        self.enter_second_number(b)
        self.select_operation(op)
        return self.get_result_value()