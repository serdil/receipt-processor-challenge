def test_process_receipt(client):
    """Test the /receipts/process endpoint."""
    # Test with a valid receipt
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                },
                {
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                }
            ],
            "total": "18.74"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert isinstance(response.json()["id"], str)
    assert len(response.json()["id"]) > 0

def test_process_receipt_invalid_data(client):
    """Test the /receipts/process endpoint with invalid data."""
    # Test with missing required fields
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            # Missing purchaseTime
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                }
            ],
            "total": "6.49"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity

    # Test with invalid data types
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "invalid"  # Invalid price format
                }
            ],
            "total": "6.49"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_get_points(client):
    """Test the /receipts/{id}/points endpoint."""
    # First, process a receipt to get an ID
    process_response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                },
                {
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                }
            ],
            "total": "18.74"
        }
    )
    receipt_id = process_response.json()["id"]

    # Then, get the points for that receipt
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert "points" in points_response.json()
    assert isinstance(points_response.json()["points"], int)
    # The exact points value depends on the implementation, but we can check it's non-negative
    assert points_response.json()["points"] >= 0

def test_get_points_invalid_id(client):
    """Test the /receipts/{id}/points endpoint with an invalid ID."""
    # Test with a non-existent ID
    response = client.get("/receipts/nonexistent-id/points")
    assert response.status_code == 404  # Not Found

def test_example_receipts(client):
    """Test the API with the example receipts from the task description."""
    # Example 1
    example1_response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                },
                {
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                },
                {
                    "shortDescription": "Knorr Creamy Chicken",
                    "price": "1.26"
                },
                {
                    "shortDescription": "Doritos Nacho Cheese",
                    "price": "3.35"
                },
                {
                    "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                    "price": "12.00"
                }
            ],
            "total": "35.35"
        }
    )
    example1_id = example1_response.json()["id"]
    example1_points = client.get(f"/receipts/{example1_id}/points").json()["points"]
    assert example1_points == 28

    # Example 2
    example2_response = client.post(
        "/receipts/process",
        json={
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                }
            ],
            "total": "9.00"
        }
    )
    example2_id = example2_response.json()["id"]
    example2_points = client.get(f"/receipts/{example2_id}/points").json()["points"]
    assert example2_points == 109
