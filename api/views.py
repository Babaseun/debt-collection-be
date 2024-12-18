import csv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import FileUploadSerializer
from accounts.models import Account, Client, Consumer
from django.core.paginator import Paginator
from .utils import Utils


@api_view(["POST"])
def save_csv_data(request):
    try:
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES["file"]
            decoded_file = file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                client_reference_no = row["client reference no"]
                client, _ = Client.objects.get_or_create(
                    client_reference_no=client_reference_no, name="Aktos"
                )

                consumer, _ = Consumer.objects.get_or_create(
                    ssn=row["ssn"],
                    defaults={
                        "name": row["consumer name"],
                        "address": row["consumer address"],
                    },
                )

                account, account_created = Account.objects.get_or_create(
                    balance=float(row["balance"]),
                    status=Utils.parse_status(row["status"]).value,
                    client=client,
                )

                if account_created:
                    # Add consumers to the account only if it was created
                    account.consumers.add(consumer)
                    account.save()

            return Response(
                {"message": "CSV data ingested successfully"}, status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_accounts(request):
    min_balance = request.GET.get("min_balance")
    max_balance = request.GET.get("max_balance")
    status_type = request.GET.get("status")
    consumer_name = request.GET.get("consumer_name")

    page_number = request.GET.get("page_number", 1)
    per_page = request.GET.get("per_page", 10)

    accounts = Account.objects.all()
    if consumer_name:
        accounts = accounts.filter(consumers__name__icontains=consumer_name)

    if max_balance:
        accounts = accounts.filter(balance__lte=float(max_balance))

    if min_balance:
        accounts = accounts.filter(balance__gte=float(min_balance))

    if max_balance:
        accounts = accounts.filter(balance__lte=float(max_balance))

    if status_type:
        accounts = accounts.filter(status=status_type.upper())

    paginator = Paginator(accounts, per_page)
    page = paginator.get_page(page_number)

    accounts_data = [
        {
            "id": account.id,
            "balance": account.balance,
            "status": account.status,
            "client": account.client.client_reference_no,
            "created_at": account.created_at,
            "updated_at": account.updated_at,
            "consumers": [
                {
                    "name": consumer.name,
                    "ssn": consumer.ssn,
                    "address": consumer.address,
                }
                for consumer in account.consumers.all()
            ],
        }
        for account in page
    ]

    response = {
        "accounts": accounts_data,
        "page_number": page.number,
        "pages": paginator.num_pages,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
    }
    return Response(response, status.HTTP_200_OK)
