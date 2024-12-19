# Debt Collection API Project

This project is a Django-based API for managing client accounts and consumer data.
Deployed to AWS Lambda and AWS API Gateway to trigger the lambda function. AWS Aurora Postgres serverless DB is used for cost savings.

## Requirements

- [Python 3.12+](https://www.python.org/downloads/)

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/your-username/debt-collection-be.git
   cd xyz_debt_collection_api
   ```

2. Build and start the Docker containers:

   ```
   python manage.py runserver
   ```

3. Run migrations:

   ```
   python manage.py migrate
   ```

## Running the API

The API is available at `https://rhbiwq9m5f.execute-api.us-east-1.amazonaws.com/dev`.

### Endpoints

1. Ingest Accounts:

   - URL: `POST /accounts/upload`
   - Description: Ingests account data from a CSV file at the specified URL.

2. Get Accounts:
   - URL: `GET /accounts`
   - Query Parameters:
     - `min_balance`: Minimum account balance (inclusive)
     - `max_balance`: Maximum account balance (inclusive)
     - `consumer_name`: Filter by consumer name (case-insensitive, partial match)
     - `status`: Filter by account status (case-insensitive, exact match)
     - `per_page`: Filter by the number of records to return. The default is 10
     - `page_number`: default is 1
   - Description: Retrieves accounts based on the provided filters and returned in ascending order by the id.

## Testing the API

You can test the API using [curl](https://curl.se/) or any API testing tool like [Postman](https://www.postman.com/). Here are some example curl commands:

1. Upload CSV containing accounts, debtors:

   [Download the CSV file](consumers_balances.csv)


  ![Alt text](Screenshot%202024-12-18%20at%2010.10.53 PM.png)


2. Get Accounts:

   ```
   curl "https://rhbiwq9m5f.execute-api.us-east-1.amazonaws.com/dev/accounts?min_balance=100&max_balance=1000&status=in_collection"
   ```


### Running Unit Tests

To run the unit tests for this project:

```
python manage.py test
```

## Data Model

Application's data structure is modeled as follows:

1. Store for many clients 
2. The accounts details provided above in the CSV file can have many consumers/debtors that owe the debt, and the consumers/debtors can have many accounts
   --> many to many relationship 


