import boto3
import json
from decimal import Decimal
import os

# Configuración de LocalStack
ENDPOINT_URL = "http://localhost:4566"
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"

# Nombres de los recursos
BUCKET_NAME = "fire-damage-bucket"
TABLE_NAME = "fire_damage"
BATCH_SIZE = 25
# Conexión con AWS LocalStack

dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION)



def convert_types(data):
    """Convierte los datos para que coincidan con los tipos esperados en DynamoDB."""
    if isinstance(data, list):
        return [convert_types(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_types(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))  # DynamoDB no acepta float, usa Decimal
    elif isinstance(data, int):
        return Decimal(data)
    elif isinstance(data, str) and data.isdigit():
        return Decimal(data)
    return data
# Cargar el fichero GeoJSON

file_path = os.path.join(os.path.dirname(__file__), "../data/fire_data.geojson")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo no se encontró en la ruta: {file_path}")

with open(file_path, "r") as file:
    json_data = json.load(file)

# Extraer solo la parte de los datos
features = json_data.get("features", [])


def batch_insert_dynamodb(table_name, features):
    """Inserta datos en DynamoDB usando batch_writer()."""
    
    table = dynamodb.Table(TABLE_NAME)

    with table.batch_writer() as batch:
        for feature in features:
            item = feature["properties"]
            batch.put_item(Item=convert_types(item))  # Convertimos los tipos antes de insertar

    print(f"✅ Datos insertados en la tabla {table_name} exitosamente 🚀")


if __name__ == "__main__":
    batch_insert_dynamodb(table_name=TABLE_NAME, features=features)
