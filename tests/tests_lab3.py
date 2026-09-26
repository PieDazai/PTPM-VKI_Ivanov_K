import unittest
from unittest.mock import Mock

from src.registration_service import RegistrationService
from src.database import Database
from src.user_interface import ConsoleUserInterface
from src.controller import Controller


class TestLab3(unittest.TestCase):

    def test_database_add_and_get(self):
        database = Database()

        database.add_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!",
            1,
            ""
        )

        result = database.get_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!"
        )

        self.assertEqual(
            result,
            (1, "")
        )

    def test_database_delete(self):
        database = Database()

        database.add_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!",
            1,
            ""
        )

        database.delete_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!"
        )

        result = database.get_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!"
        )

        self.assertIsNone(result)

    def test_controller_new_registration(self):
        calculator = RegistrationService()
        database = Database()

        user_interface = Mock()
        user_interface.get_data.return_value = (
            "Ivan123",
            "Пароль1!",
            "Пароль1!"
        )

        external_service = Mock()

        controller = Controller(
            calculator,
            database,
            user_interface,
            external_service
        )

        result = controller.start()

        self.assertEqual(
            result,
            (True, "")
        )

        external_service.send.assert_called_once()

    def test_controller_gets_result_from_database(self):
        calculator = Mock()
        database = Database()

        database.add_user(
            "Ivan123",
            "Пароль1!",
            "Пароль1!",
            1,
            ""
        )

        user_interface = Mock()
        user_interface.get_data.return_value = (
            "Ivan123",
            "Пароль1!",
            "Пароль1!"
        )

        external_service = Mock()

        controller = Controller(
            calculator,
            database,
            user_interface,
            external_service
        )

        result = controller.start()

        self.assertEqual(
            result,
            (1, "")
        )

        calculator.calculate.assert_not_called()

    def test_controller_invalid_registration(self):
        calculator = RegistrationService()
        database = Database()

        user_interface = Mock()
        user_interface.get_data.return_value = (
            "Ivan123",
            "Пароль1!",
            "ДругойПароль1!"
        )

        external_service = Mock()

        controller = Controller(
            calculator,
            database,
            user_interface,
            external_service
        )

        result = controller.start()

        self.assertEqual(
            result,
            (
                False,
                "Пароли не совпадают"
            )
        )

        external_service.send.assert_called_once()

    def test_console_input(self):
        user_interface = ConsoleUserInterface()

        with unittest.mock.patch(
            "builtins.input",
            side_effect=[
                "Ivan123",
                "Пароль1!",
                "Пароль1!"
            ]
        ):
            result = user_interface.get_data()

        self.assertEqual(
            result,
            (
                "Ivan123",
                "Пароль1!",
                "Пароль1!"
            )
        )

if __name__ == "__main__":
    unittest.main()