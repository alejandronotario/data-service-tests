import boto3
import json
from decimal import Decimal
import os
from typing import Any, Dict, List

# LocalStack configuration
ENDPOINT_URL = "http://localhost:4566"
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"

# Resource names
BUCKET_NAME = "fire-damage-bucket"
TABLE_NAME = "fire_damage"
BATCH_SIZE = 25

# Connection to AWS LocalStack
dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION)


def convert_types(data: Any) -> Any:
    """Converts data to match the expected types in DynamoDB."""
    if isinstance(data, list):
        return [convert_types(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_types(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))  # DynamoDB does not accept float, use Decimal
    elif isinstance(data, int):
        return Decimal(data)
    elif isinstance(data, str) and data.isdigit():
        return Decimal(data)
    return data

# Load the GeoJSON file
file_path = os.path.join(os.path.dirname(__file__), "../data/fire_data.geojson")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file was not found at the path: {file_path}")

with open(file_path, "r") as file:
    json_data: Dict[str, Any] = json.load(file)

# Extract only the data part
features: List[Dict[str, Any]] = json_data.get("features", [])


def batch_insert_dynamodb(table_name: str, features: List[Dict[str, Any]]) -> None:
    """Inserts data into DynamoDB using batch_writer()."""
    
    table = dynamodb.Table(TABLE_NAME)

    with table.batch_writer() as batch:
        for feature in features:
            item: Dict[str, Any] = feature["properties"]
            batch.put_item(Item=convert_types(item))  # Convert types before inserting

    print(f"✅ Data successfully inserted into the table {table_name} 🚀")


if __name__ == "__main__":
    batch_insert_dynamodb(table_name=TABLE_NAME, features=features)
