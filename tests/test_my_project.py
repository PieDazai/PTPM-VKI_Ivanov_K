import unittest

from src import registrator

class TestRegistrator(unittest.TestCase):
    #  python -m unittest discover -s tests -p "test_*.py" -v

    #############MAIL################

    def test_valid_email(self):
        self.assertTrue(
            registrator.is_valid_email("student@mail.ru")
        )

    def test_valid_email_with_numbers(self):
        self.assertTrue(
            registrator.is_valid_email("student123@mail.ru")
        )

    def test_invalid_email_without_domain(self):
        self.assertFalse(
            registrator.is_valid_email("student@mail")
        )

    def test_invalid_email_without_at(self):
        self.assertFalse(
            registrator.is_valid_email("studentmail.ru")
        )

    ##########PHONE################

    def test_valid_phone(self):
        self.assertTrue(
            registrator.is_valid_phone("+7-123-456-7890")
        )

    def test_invalid_phone_without_plus(self):
        self.assertFalse(
            registrator.is_valid_phone("7-123-456-7890")
        )

    def test_invalid_phone_with_wrong_format(self):
        self.assertFalse(
            registrator.is_valid_phone("+7-123-456-789")
        )

    ################USERNAME################3

    def test_valid_username(self):
        self.assertTrue(
            registrator.is_valid_username("kirill")
        )

    def test_valid_username_with_numbers(self):
        self.assertTrue(
            registrator.is_valid_username("kirill666")
        )

    def test_valid_username_with_underscore(self):
        self.assertTrue(
            registrator.is_valid_username("kirill_666")
        )

    def test_invalid_username_short(self):
        self.assertFalse(
            registrator.is_valid_username("aaa")
        )

    def test_invalid_username_with_special_symbol(self):
        self.assertFalse(
            registrator.is_valid_username("aaaaa!@#$@$")
        )

    def test_invalid_username_with_russian_letters(self):
        self.assertFalse(
            registrator.is_valid_username("коняшка")
        )

    #######PASSWORD##########

    def test_valid_password(self):
        self.assertTrue(
            registrator.is_valid_password("Паролькрутой11!")
        )

    def test_invalid_password_too_short(self):
        self.assertFalse(
            registrator.is_valid_password("ааа")
        )

    def test_invalid_password_with_english_letters(self):
        self.assertFalse(
            registrator.is_valid_password("Паролькрутой11!qq")
        )

    def test_invalid_password_without_uppercase_letter(self):
        self.assertFalse(
            registrator.is_valid_password("паролькрутой11!")
        )

    def test_invalid_password_without_lowercase_letter(self):
        self.assertFalse(
            registrator.is_valid_password("ПАРОЛЬКРУТОЙ11!")
        )

    def test_invalid_password_without_digit(self):
        self.assertFalse(
            registrator.is_valid_password("Паролькрутой!")
        )

    def test_invalid_password_without_special_symbol(self):
        self.assertFalse(
            registrator.is_valid_password("Паролькрутой1")
        )

    #########REGISTRATION#############

    def test_register_with_empty_login(self):
        result = registrator.register_user(
            "",
            "Паролькрутой1!",
            "Паролькрутой1!"
        )

        self.assertEqual(
            result,
            (False, "Логин не может быть пустым")
        )

    def test_register_blacklist_login(self):
        result = registrator.register_user(
            "admin",
            "Паролькрутой1!",
            "Паролькрутой1!"
        )

        self.assertEqual(
            result,
            (False, "Логин запрещен")
        )

    def test_register_invalid_login(self):
        result = registrator.register_user(
            "a",
            "Паролькрутой1!",
            "Паролькрутой1!"
        )

        self.assertEqual(
            result,
            (False, "Некорректный формат логина")
        )

    def test_register_invalid_password(self):
        result = registrator.register_user(
            "kirill",
            "aaaa",
            "aaaa"
        )

        self.assertEqual(
            result,
            (False, "Пароль не соответствует требованиям")
        )

    def test_register_passwords_do_not_match(self):
        result = registrator.register_user(
            "student",
            "Паролькрутой1!",
            "Паролькрутой2!"
        )

        self.assertEqual(
            result,
            (False, "Пароли не совпадают")
        )

    def test_register_success(self):
        result = registrator.register_user(
            "kirill",
            "Паролькрутой1!",
            "Паролькрутой1!"
        )

        self.assertEqual(
            result,
            (True, "")
        )

if __name__ == "__main__":
    unittest.main()