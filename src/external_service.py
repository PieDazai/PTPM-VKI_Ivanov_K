from abc import ABC, abstractmethod

class ExternalService(ABC):

    @abstractmethod
    def send_mail(self, data):
        pass

class EmailService(ExternalService):

    def send_mail(self, data):
        print ("Внешний сервис. Данные отправлены. " + data)