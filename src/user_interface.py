from abc import ABC, abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def get_data(self):
        pass

class ConsoleUserInterface(UserInterface):

    def get_data(self):
        action = input(
            "Выберите действие:\n"
            "1 - регистрация\n"
            "2 - удаление аккаунта\n"
            "q - выход из программы\n"
            "Ваш выбор: "
        )

        if action not in ("q", "1", "2"):
            return None, None, None, None

        if action == "q":
            return "q", None, None, None

        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        if action == "1":
            confirm_password = input(
                "Повторите пароль: "
            )

            return (
                action,
                login,
                password,
                confirm_password
            )

        return (
            action,
            login,
            password,
            None
        )