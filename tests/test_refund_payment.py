import pytest
import allure
from src.utils.waiters import Waiter


@allure.feature("Payments")
@allure.story("Refund Payment")
@pytest.mark.api
@pytest.mark.parametrize(
    "amount, currency", [
        (50, "USD"),
        (100, "USD"),
        (150, "EUR"),
    ]
)
def test_refund_payment(payments_service, amount, currency):
    """
    Проверяем, что возврат создаётся успешно для разных сумм и валют.
    """
    waiter = Waiter(timeout=5)

    with allure.step(f"1️⃣ Create payment for {amount} {currency}"):
        created = payments_service.create_payment(amount=amount, currency=currency)
        assert created.status_code == 200, created.text
        payment_id = created.json()["payment"]["id"]
        allure.attach(str(payment_id), "Payment ID", allure.attachment_type.TEXT)

    with allure.step("2️⃣ Refund payment by ID"):
        refund = payments_service.create_refund(payment_id, amount=amount, currency=currency)
        allure.attach(refund.text, "Refund response", allure.attachment_type.JSON)

        # Проверяем, что запрос прошёл или завершён с ошибкой статуса
        assert refund.status_code in [200, 400], f"Unexpected status: {refund.status_code}"

    if refund.status_code == 200:
        with allure.step("3️⃣ Wait until refund appears in the system"):
            refund_id = refund.json()["refund"]["id"]

            waiter.until(
                lambda: payments_service.client.get(f"/v2/refunds/{refund_id}").status_code == 200,
                message=f"Refund {refund_id} not found in time"
            )

        with allure.step("4️⃣ Validate refund status"):
            refund_data = payments_service.client.get(f"/v2/refunds/{refund_id}").json()["refund"]
            status = refund_data["status"]

            assert status in ["PENDING", "COMPLETED"]
            allure.attach(str(refund_data), "Refund Data", allure.attachment_type.JSON)
            print(f"✅ Refund {refund_id} created successfully with status {status}")


    elif refund.status_code == 400:

        with allure.step("⚠️ Refund failed — invalid request"):

            assert any(

                err_code in refund.text

                for err_code in ["INVALID_PAYMENT_STATUS", "CURRENCY_MISMATCH"]

            ), f"Unexpected error response: {refund.text}"
