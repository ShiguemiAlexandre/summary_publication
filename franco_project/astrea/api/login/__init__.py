import requests
from dotenv import load_dotenv
import os
from validation.requests import ValidationStatusCode
import logging
from astrea.api.exceptions.login import UnauthorizedAstrea

class Login:
    def __init__(self):
        load_dotenv()
        self.LOGIN = os.getenv("LOGIN_ASTREA")
        self.PASSWORD = os.getenv("PASSWORD_ASTREA")

        self.URL = "https://app.astrea.net.br/api/v2/session/login"

        self.validation_status_code = ValidationStatusCode()

        self.logger = logging.getLogger(__name__)
    
    def post(self):
        self.logger.info("Realizando o login")

        payload = {
            "username": self.LOGIN,
            "password": self.PASSWORD
        }

        response = requests.post(self.URL, json=payload)

        if not self.validation_status_code.validate(
            request=response,
            permited_status_code=[200]
        ):
            self.logger.error("Usuário não autenticado")
            raise response.raise_for_status()

        self.logger.info("Login realizado com sucesso")

        return response.json()
        