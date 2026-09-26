class Controller:

    def __init__(
            self,
            registration_service,
            database,
            user_interface,
            external_service
    ):
        self.registration_service = registration_service
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def start(self):
        while True:
            action, login, password, confirm_password = (
                self.user_interface.get_data()
            )

            if action == "1":
                self.register_user(
                    login,
                    password,
                    confirm_password
                )
            elif action == "2":
                self.delete_user(
                    login,
                    password
                )
            else:
                message = "Некорректный выбор"

                self.external_service.send_mail("Ошибка: " + message)

    def register_user(
            self,
            login,
            password,
            confirm_password
    ):
        result, message = self.registration_service.register(
            login,
            password,
            confirm_password
        )

        if not result:
            self.external_service.send_mail("Ошибка: " + message)
            return None

        saved_user = self.database.get_user(login)

        if saved_user is not None:
            self.external_service.send_mail("Ошибка: " + "Пользователь уже существует")
            return None

        self.database.add_user(
            login,
            self.registration_service.hash_password(password),
            self.registration_service.hash_password(confirm_password),
            result,
            message
        )

        self.external_service.send_mail("Регистрация успешна")
        return None

    def delete_user(
            self,
            login,
            password
    ):
        deleted = self.database.delete_user(
            login,
            self.registration_service.hash_password(password)
        )

        if deleted:
            result, message = True, "Аккаунт удален"
        else:
            result, message = False, "Пользователь не найден"

        self.external_service.send_mail(message)

        return None