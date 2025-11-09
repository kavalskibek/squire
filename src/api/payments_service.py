import uuid
from src.utils.constants import PAYMENTS, REFUNDS


class PaymentService:  # ← ДОБАВИЛ "s"!
    def __init__(self, client):
        self.client = client

    def create_payment(self, amount=100, **kwargs):
        payload = {
            "idempotency_key": str(uuid.uuid4()),
            "source_id": "cnon:card-nonce-ok",
            "amount_money": {  # ← ОБЯЗАТЕЛЬНО!
                "amount": amount,  # ← в центах: 100 = $1.00
                "currency": "USD"
            },
            "autocomplete": True,
            **kwargs
        }
        # ← УБРАЛ /payments — PAYMENTS уже содержит /v2/payments
        return self.client.post(PAYMENTS, json_data=payload)