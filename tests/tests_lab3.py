import unittest
from unittest.mock import Mock, patch

from src.registration_service import RegistrationService
from src.database import Database
from src.user_interface import ConsoleUserInterface
from src.controller import Controller


class TestLab3(unittest.TestCase):

    def setUp(self):
        self.registration_service = RegistrationService()
        self.database = Database(":memory:")
        self.user_interface = ConsoleUserInterface()

        self.external_service = Mock()

        self.controller = Controller(
            self.registration_service,
            self.database,
            self.user_interface,
            self.external_service
        )

    def test_database_add_and_get_user(self):
        password_hash = (
            self.registration_service.hash_password(
                "Йййййй_1!"
            )
        )

        self.database.add_user(
            "Qwerty123",
            password_hash,
            password_hash,
            True,
            "Регистрация успешна"
        )

        result = self.database.get_user("Qwerty123")

        self.assertEqual(
            result,
            (1, "Регистрация успешна")
        )

    def test_database_delete_user(self):
        password_hash = (
            self.registration_service.hash_password(
                "Йййййй_1!"
            )
        )

        self.database.add_user(
            "Qwerty123",
            password_hash,
            password_hash,
            True,
            "Регистрация успешна"
        )

        deleted = self.database.delete_user(
            "Qwerty123",
            password_hash
        )

        self.assertTrue(deleted)

        result = self.database.get_user("Qwerty123")

        self.assertIsNone(result)

    def test_database_get_unknown_user(self):
        result = self.database.get_user("Unknown123")

        self.assertIsNone(result)

    def test_user_interface_registration(self):
        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "Qwerty123",
                "Йййййй_1!",
                "Йййййй_1!"
            ]
        ):
            result = self.user_interface.get_data()

        self.assertEqual(
            result,
            (
                "1",
                "Qwerty123",
                "Йййййй_1!",
                "Йййййй_1!"
            )
        )

    def test_user_interface_delete(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2",
                "Qwerty123",
                "Йййййй_1!"
            ]
        ):
            result = self.user_interface.get_data()

        self.assertEqual(
            result,
            (
                "2",
                "Qwerty123",
                "Йййййй_1!",
                None
            )
        )

    def test_user_interface_exit(self):
        with patch(
            "builtins.input",
            return_value="q"
        ):
            result = self.user_interface.get_data()

        self.assertEqual(
            result,
            ("q", None, None, None)
        )

    def test_user_interface_invalid_action(self):
        with patch(
            "builtins.input",
            return_value="fwf"
        ):
            result = self.user_interface.get_data()

        self.assertEqual(
            result,
            (None, None, None, None)
        )


 # Интеграционные

    def test_controller_register_user(self):
        result = self.controller.register_user(
            "Qwerty123",
            "Йййййй_1!",
            "Йййййй_1!"
        )

        self.assertEqual(
            result,
            (True, "Регистрация успешна")
        )

        user = self.database.get_user("Qwerty123")

        self.assertEqual(
            user,
            (1, "Регистрация успешна")
        )

        self.external_service.send_mail.assert_called_once_with(
            "Регистрация успешна"
        )

    def test_controller_invalid_registration(self):
        result = self.controller.register_user(
            "Qwerty123",
            "123",
            "123"
        )

        self.assertEqual(
            result,
            (
                False,
                "Пароль не соответствует требованиям"
            )
        )

        self.external_service.send_mail.assert_called_once_with(
            "Ошибка: Пароль не соответствует требованиям"
        )

    def test_controller_existing_user(self):
        password = "Йййййй_1!"

        password_hash = (
            self.registration_service.hash_password(password)
        )

        self.database.add_user(
            "Qwerty123",
            password_hash,
            password_hash,
            True,
            "Регистрация успешна"
        )

        result = self.controller.register_user(
            "Qwerty123",
            password,
            password
        )

        self.assertEqual(
            result,
            (
                False,
                "Пользователь уже существует"
            )
        )

        self.external_service.send_mail.assert_called_once_with(
            "Ошибка: Пользователь уже существует"
        )

    def test_controller_delete_existing_user(self):
        password = "Йййййй_1!"

        password_hash = (
            self.registration_service.hash_password(password)
        )

        self.database.add_user(
            "Qwerty123",
            password_hash,
            password_hash,
            True,
            "Регистрация успешна"
        )

        result = self.controller.delete_user(
            "Qwerty123",
            password
        )

        self.assertEqual(
            result,
            (
                True,
                "Аккаунт удален"
            )
        )

        self.assertIsNone(
            self.database.get_user("Qwerty123")
        )

    def test_controller_delete_unknown_user(self):
        result = self.controller.delete_user(
            "Unknown123",
            "Йййййй_1!"
        )

        self.assertEqual(
            result,
            (
                False,
                "Пользователь не найден"
            )
        )

        self.external_service.send_mail.assert_called_once_with(
            "Пользователь не найден"
        )


if __name__ == "__main__":
    unittest.main()