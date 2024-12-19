from decimal import Decimal
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from .models import Account
from .models import Client as ClientModel
from .models import Consumer


class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_model = ClientModel.objects.create(client_reference_no="TEST001")
        # Create multiple consumers
        self.consumers = [
            Consumer.objects.create(
                ssn="123-45-6789", name="John Doe", address="123 Test St"
            ),
            Consumer.objects.create(
                ssn="987-65-4321", name="Jane Doe", address="456 Another St"
            ),
        ]
        self.account = Account.objects.create(
            balance=Decimal("1000.00"), status="ACTIVE", client=self.client_model
        )
        # Associate multiple consumers with the account
        self.account.consumers.add(*self.consumers)  # Add multiple consumers
        self.account.save()

    def test_get_accounts_no_filters(self):
        response = self.client.get(reverse("get_accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["accounts"]), 1)

    def test_get_accounts_with_filters(self):
        Account.objects.create(
            balance=Decimal("500.00"), status="INACTIVE", client=self.client_model
        )

        response = self.client.get(
            reverse("get_accounts"), {"min_balance": "750", "status": "ACTIVE"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["accounts"]), 1)
        self.assertEqual(response.json()["accounts"][0]["status"], "ACTIVE")

    def test_get_accounts_no_results(self):
        response = self.client.get(reverse("get_accounts"), {"min_balance": "5000"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["accounts"]), 0)
