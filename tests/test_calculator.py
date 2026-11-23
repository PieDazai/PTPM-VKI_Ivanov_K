import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.pages.calculator_page import CalculatorPage

class CalculatorTests(unittest.TestCase):

    def setUp(self):
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        self.driver = webdriver.Chrome(options=opts)
        self.page = CalculatorPage(self.driver)
        self.page.open()

    def tearDown(self):
        self.driver.quit()

    # ---------- Базовые операции ----------

    def test_addition(self):
        self.assertEqual(self.page.calculate(2, 3, "+"), 5)

    def test_subtraction(self):
        self.assertEqual(self.page.calculate(10, 4, "-"), 6)

    def test_multiplication(self):
        self.assertEqual(self.page.calculate(6, 7, "*"), 42)

    def test_division(self):
        self.assertEqual(self.page.calculate(8, 2, "/"), 4)

    # ---------- Любые числа ----------

    def test_negative_operands(self):
        self.assertEqual(self.page.calculate(-5, 3, "+"), -2)

    def test_negative_and_negative(self):
        self.assertEqual(self.page.calculate(-4, -6, "*"), 24)

    def test_float_operands(self):
        self.assertAlmostEqual(self.page.calculate(1.5, 2.5, "*"), 3.75, places=4)

    def test_float_division(self):
        self.assertAlmostEqual(self.page.calculate(1, 3, "/"), 1 / 3, places=4)

    def test_zero_operands(self):
        self.assertEqual(self.page.calculate(0, 0, "+"), 0)

    def test_large_numbers(self):
        self.assertEqual(self.page.calculate(100000, 200000, "*"), 20000000000)

    # ---------- Деление на ноль ----------

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.page.calculate(5, 0, "/")

    def test_negative_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.page.calculate(-5, 0, "/")

if __name__ == "__main__":
    unittest.main()