from registration_service import RegistrationService
from database import Database
from user_interface import ConsoleUserInterface
from external_service import EmailService
from controller import Controller

registration_service = RegistrationService()
database = Database()
user_interface = ConsoleUserInterface()
external_service = EmailService()

controller = Controller(
    registration_service,
    database,
    user_interface,
    external_service
)

controller.start()