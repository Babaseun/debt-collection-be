from enum import Enum
from django.db import models


class StatusType(Enum):
    INACTIVE = "INACTIVE"
    PAID_IN_FULL = "PAID_IN_FULL"
    IN_COLLECTION = "IN_COLLECTION"


class Client(models.Model):
    client_reference_no = models.CharField(
        max_length=255, primary_key=True
    )  # Client reference to multiple accounts obtained from csv
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "client"


# The Debtors
class Consumer(models.Model):
    ssn = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "consumer"


# Account information obtained from CSV file
class Account(models.Model):
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[(item.value, item.name) for item in StatusType],
        null=True,
    )  # TODO
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="accounts"
    )
    consumers = models.ManyToManyField(Consumer, related_name="accounts")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "account"
