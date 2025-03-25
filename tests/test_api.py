
from fastapi.testclient import TestClient
from src.api.main_test import app

client = TestClient(app)

def test_get_records_default_limit():
    # Request the default number of records (limit=5)
    response = client.get("/records")
    assert response.status_code == 200
    data = response.json()
    # Default limit should return 5 records
    assert isinstance(data, list)
    assert len(data) == 5
    # Verify that each record has the expected keys
    for record in data:
        assert "OBJECTID" in record
        assert "DAMAGE" in record

def test_get_records_custom_limit():
    # Request 3 records explicitly
    response = client.get("/records?limit=3")
    assert response.status_code == 200
    data = response.json()
    # Should return 3 records
    assert isinstance(data, list)
    assert len(data) == 3