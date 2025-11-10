import os
import sys
from ctypes import pythonapi

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

@pytest.fixture
def created_payment_id(payments_service):
    response = payments_service.create_payment(amount=100)
    assert response.status_code == 200
    return response.json()["payment"]["id"]