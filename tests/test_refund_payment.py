import pytest
import allure
# from src.utils.waiters import wait_for/




@allure.feature("Payments")
@allure.story("Refund Payment")
@pytest.mark.api
@pytest.mark.parametrize(
    'amount, currency', [
        (50, "USD"),
        (100, "USD"),
        (150, "EUR"),
    ]
)
def test_refund_payment(payments_service, amount, currency):

    with allure.step(f'Create payment for {amount} {currency}'):
        created = payments_service.create_payment(amount=amount, currency=currency)
        payment_id = created.json()["payment"]["id"]
        allure.attach(str(payment_id), 'Payment ID', allure.attachment_type.TEXT)

    with allure.step(f'Refund payment for ID'):
        refund = payments_service.create_refund(payment_id, amount=amount, currency=currency)
        allure.attach(refund.text, 'Refund response', allure.attachment_type.JSON)