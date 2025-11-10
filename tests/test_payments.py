import pytest
from src.utils.constants import LOCATIONS

@pytest.mark.api
def test_get_locations(square_client):
    response = square_client.get(LOCATIONS)
    assert response.status_code == 200
    data = response.json()
    assert "locations" in data
    print(f"Found {len(data['locations'])} locations")



@pytest.mark.api
def test_create_payment(payments_service):
    response = payments_service.create_payment(amount=100)
    assert response.status_code == 200, response.text
    data = response.json()
    payment = data["payment"]
    assert payment["status"] == "COMPLETED"
    print(f"✅ Payment created: {payment['id']}")

@pytest.mark.api
def test_get_list_of_payments(payments_service):

    response = payments_service.get_payments()
    assert response.status_code == 200
    print(response.json())
