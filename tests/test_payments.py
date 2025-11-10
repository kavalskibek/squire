import pytest
from src.utils.constants import LOCATIONS
from src.utils.waiters import wait_for

@pytest.mark.api
def test_get_locations(square_client):
    response = square_client.get(LOCATIONS)
    assert response.status_code == 200
    data = response.json()
    assert "locations" in data
    print(f"Found {len(data['locations'])} locations")



@pytest.mark.api
def test_create_payment_and_wait_in_list(payments_service):
    """Создание платежа и ожидание появления в списке"""
    # 1. Создаём платёж
    created = payments_service.create_payment(amount=100)
    assert created.status_code == 200
    payment_id = created.json()["payment"]["id"]

    # 2. Определяем функцию-условие
    def payment_exists():
        response = payments_service.get_payments()
        if response.status_code != 200:
            return False
        data = response.json().get("payments", [])
        return any(p["id"] == payment_id for p in data)

    # 3. Ждём появления платежа
    found = wait_for(payment_exists, timeout=5, interval=0.5)
    assert found, f"❌ Payment {payment_id} not found in list after 5s"

    print(f"✅ Payment {payment_id} successfully appeared in list")

    print(f"✅ Payment {payment_id} successfully appeared in list")