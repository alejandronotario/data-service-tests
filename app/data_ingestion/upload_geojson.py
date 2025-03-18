import json
import boto3

def upload_geojson_to_dynamodb(geojson_file, table_name, endpoint_url="http://localhost:4566"):
    # Initialize DynamoDB resource for LocalStack with test credentials
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        endpoint_url=endpoint_url,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    table = dynamodb.Table(table_name)

    with open(geojson_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    count = 0
    for feature in features:
        props = feature.get("properties", {})
        # Convert OBJECTID to string (DynamoDB key must be a string in this case)
        if "OBJECTID" in props:
            props["OBJECTID"] = str(props["OBJECTID"])
        else:
            continue
        try:
            table.put_item(Item=props)
            count += 1
        except Exception as e:
            print(f"Error uploading record: {e}")
    print(f"Uploaded {count} records to table '{table_name}'.")

if __name__ == "__main__":
    # Adjust the file path as needed (relative to this script)
    upload_geojson_to_dynamodb("../data/sample.geojson", "fire_damage")
