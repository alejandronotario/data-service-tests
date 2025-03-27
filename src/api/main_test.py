from typing import Dict, List

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Test API", version="1.0-test")

# Static test data simulating DynamoDB records from the "fire_damage" table
test_data = [
    {
        "OBJECTID": "1",
        "DAMAGE": "None",
        "STREETNUMBER": "123",
        "STREETNAME": "Main St",
        "CITY": "Testville",
    },
    {
        "OBJECTID": "2",
        "DAMAGE": "Minor",
        "STREETNUMBER": "456",
        "STREETNAME": "Second St",
        "CITY": "Testville",
    },
    {
        "OBJECTID": "3",
        "DAMAGE": "Major",
        "STREETNUMBER": "789",
        "STREETNAME": "Third St",
        "CITY": "Testville",
    },
    {
        "OBJECTID": "4",
        "DAMAGE": "Severe",
        "STREETNUMBER": "101",
        "STREETNAME": "Fourth St",
        "CITY": "Testville",
    },
    {
        "OBJECTID": "5",
        "DAMAGE": "None",
        "STREETNUMBER": "102",
        "STREETNAME": "Fifth St",
        "CITY": "Testville",
    },
    {
        "OBJECTID": "6",
        "DAMAGE": "Minor",
        "STREETNUMBER": "103",
        "STREETNAME": "Sixth St",
        "CITY": "Testville",
    },
]


@app.get("/records", response_model=List[Dict])
def get_records(
    limit: int = Query(5, description="Number of records to retrieve")
):
    """
    Retrieves the first `limit` records from the test data.
    """
    try:
        return test_data[:limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main_test:app", host="0.0.0.0", port=8000, reload=True
    )
