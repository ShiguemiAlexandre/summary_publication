from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging


load_dotenv()

class Credencials:
    def __init__(self):
        self.TOKEN = os.getenv("API_KEY_GEMINI")
        self.logger = logging.getLogger(__name__)
    
    def login(self, model_name: str = "gemini-2.5-flash"):
        """
        Configura a autenticação com a API do Gemini e retorna uma instância do modelo generativo.

        Returns:
            GenerativeModel: Modelo configurado pronto para gerar conteúdo.
        """
        self.logger.info("Iniciando Gemini")

        self.logger.info(f"Utilizando modelo {model_name}")

        try:
            genai.configure(api_key=self.TOKEN)
            model = genai.GenerativeModel(model_name=model_name)
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}")
            raise e

        self.logger.info("Gemini iniciado com sucesso")
        return model

