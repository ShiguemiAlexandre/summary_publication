from openai import OpenAI
from dotenv import load_dotenv
import os

class GPTOpenAI:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("API_KEY_OPENAI"))
    
    def generate(self, prompt: str, model: str = "gpt-4o-mini", store: bool = True) -> str:
        """
        Gera texto usando o modelo especifico
        """
        return self.client.responses.create(
            model=model,
            input=prompt,
            store=store
        )["content"].get("text")
