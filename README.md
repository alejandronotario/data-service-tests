# data-service-tests

This document outlines the steps to set up and test the data service for the project using LocalStack, Terraform, and FastAPI.

> **Note:** LocalStack is used to emulate AWS services locally. The Terraform configuration below uses custom endpoints for DynamoDB, and STS.

---

## Prerequisites

- **Docker and Docker Compose:** To run LocalStack.
- **Terraform:** For provisioning the infrastructure.
- **AWS CLI:** For manual testing of the emulated services.
- **Python 3.11.5** (or your chosen version via pyenv).
- **LocalStack:** Emulated via Docker Compose.
- **FastAPI and Uvicorn:** For running the backend API.

---

## Project Structure

```pgsql
project-root/
│
├── data/
│   └── fire_data.json          # Test data file (a simple JSON file, can be extracted from a GeoJSON)
│
├── infra/
│   └── terraform/
│       ├── provider.tf         # AWS provider configuration for LocalStack (including STS)   
│       ├── dynamodb.tf         # Creation of DynamoDB tables: "fire_damage" and "Predictions"
│       ├── variables.tf        # Variables (bucket name, table names, etc.)
│       └── outputs.tf          # Useful outputs (bucket name and table names)
│
├── docker-compose.yml            # Docker Compose file to run LocalStack
│
├── src/
│   ├── data_ingestion/
│   │   └── upload_geojson.py   # Script to upload data from the file to the "fire_damage" table
│   └── api/
│       └── main.py             # FastAPI backend: GET endpoint to fetch the first n records from DynamoDB
│
├── tests/
│   └── test_api.py             # (Optional) Script to test querying the "fire_damage" table
│
└── README.md                   # This document
```

1. Start LocalStack:

```bash
docker-compose up -d
```
2. Deploy DynamoDB Tables with Terraform (from infra/terraform):

```bash
terraform init
terraform plan
terraform apply -auto-approve
```
3. Verify Tables:

```bash
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

4. Ingest GeoJSON Data into DynamoDB:

```bash
python app/main.py
```

5. Run the FastAPI Backend:

```bash
uvicorn src.api.main:app --reload
```

6. Query the API Endpoint: Access:

```bash
http://127.0.0.1:8000/records?limit=5
```
