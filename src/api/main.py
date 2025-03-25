from fastapi import FastAPI, HTTPException, Query
import boto3
import os

app = FastAPI()

# Configuration: use environment variables or default values for LocalStack
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")

# Create a DynamoDB resource for LocalStack
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)
table = dynamodb.Table("fire_damage")

@app.get("/records", response_model=list)
def get_records(limit: int = Query(5, description="Number of records to retrieve")):
    try:
        response = table.scan(Limit=limit)
        items = response.get("Items", [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
