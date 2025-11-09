import os
import sys
import pytest

# Абсолютный путь до корня проекта
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем корень проекта в системный путь, если его нет
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Теперь можно импортировать из src
from src.api.square_client import SquareClient
from src.api.payments_service import PaymentService

# @pytest.fixture(scope="session")
# def square_client():
#     return SquareClient()


@pytest.fixture(scope="session")
def square_client():
    client = SquareClient()
    yield client
    client.close()

@pytest.fixture
def payments_service(square_client):
    """Фикстура бизнес-логики"""
    return PaymentService(square_client)