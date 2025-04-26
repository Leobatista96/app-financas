import requests
import json
from decouple import config


class EvolutionAPI:

    def __init__(self):
        self.evolution_api_url = config('EVOLUTION_API_URL')
        self.instance = config('INSTANCE_ID')
        self.send_message_url = f'{self.evolution_api_url}/message/sendText/{self.instance}'
        self.number = config('NUMBER')
        self.evolution_api_key = config('EVOLUTION_API_KEY')

    def send_whatsapp_message(self, message):

        headers = {
            "apikey": self.evolution_api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "number": self.number,
            "text": message,
        }

        response = requests.post(
            url=self.send_message_url,
            headers=headers,
            json=payload,
        )
