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


    def get_payments(self ):
        return self.client.get(PAYMENTS)


    def cancel_payment(self, idempotency_key: str = None):

        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())
        payload = {'idempotency_key': idempotency_key}

        endpoint = f'{PAYMENTS}/{payment_id}/cancel'
        return self.client.post(endpoint, json_data=payload)


    def get_payment_by_id(self, payment_id: str):

        endpoint = f'{PAYMENTS}/{payment_id}'
        return self.client.get(endpoint)


    def create_refund(self, payment_id: str,  amount: int, currency: str ='USD'  ):

        payload = {
            "idempotency_key": str(uuid.uuid4()),
            'amount_money': amount,
            'currency': currency,
            'payment_id': payment_id
        }

        return self.client.post(REFUNDS, json_data=payload)
