import os
import httpx
from dotenv import load_dotenv
from src.utils.constants import BASE_HEADERS

load_dotenv()


class SquareClient:
    def __init__(self):
        self.base_url = os.getenv("SQUARE_BASE_URL")
        token = os.getenv("SQUARE_TOKEN")

        headers = BASE_HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(base_url=self.base_url, headers=headers)

    def get(self, endpoint: str):
        """GET-запрос к Square API"""
        return self.client.get(endpoint)

    def post(self, endpoint: str, json: dict = None):
        """POST-запрос к Square API"""
        return self.client.post(endpoint, json=json)

    def close(self):
        """Закрытие соединения"""
        self.client.close()
