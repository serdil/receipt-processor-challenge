# Receipt Processor Challenge

A simple receipt processor API that calculates points based on receipt data.

## Requirements

### For Docker (Recommended)
- Docker / Docker Compose

### For Direct Execution (Optional)
- Python 3.12 or higher
- uv (for dependency management)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd receipt-processor-challenge
   ```

### Using Docker (Recommended)
No additional installation steps required beyond having Docker / Docker Compose installed.

### Direct Installation (Optional)
1. Install uv by following the instructions at https://docs.astral.sh/uv/getting-started/installation/

2. Initialize uv virtual environment:
   ```
   uv venv
   ```

3. Install dependencies using uv:
   ```
   uv pip install -e .
   ```

## Running the Application

### Using Docker Compose (Recommended)
Run the application using Docker Compose:

```
docker compose up
```

This will build the Docker image and start the server on `http://0.0.0.0:8000`.

To run in detached mode:

```
docker compose up -d
```

To stop the application:

```
docker compose down
```

### Direct Execution (Optional)
Run the application directly using the provided entrypoint:

```
uv run src/main.py
```

This will start the server on `http://0.0.0.0:8000`.

## Running the Tests

### Using Docker Compose (Recommended)

Run the tests using Docker Compose:

```
docker compose run --rm receipt-processor pytest
```

This will run all the tests in the `tests` directory. You can also run specific test files or test functions:

```
# Run only the unit tests
docker compose run --rm receipt-processor pytest tests/unit

# Run only the API tests
docker compose run --rm receipt-processor pytest tests/api

# Run a specific test file
docker compose run --rm receipt-processor pytest tests/unit/test_calculate_points.py

# Run a specific test function
docker compose run --rm receipt-processor pytest tests/unit/test_calculate_points.py::test_retailer_name_points
```

### Direct Execution (Optional)

Install the test dependencies:

```
uv pip install ".[test]"
```

Run the tests using pytest:

```
uv run -m pytest
```

This will run all the tests in the `tests` directory. You can also run specific test files or test functions:

```
# Run only the unit tests
uv run -m pytest tests/unit

# Run only the API tests
uv run -m pytest tests/api

# Run a specific test file
uv run -m pytest tests/unit/test_calculate_points.py

# Run a specific test function
uv run -m pytest tests/unit/test_calculate_points.py::test_retailer_name_points
```

## API Endpoints

### Process Receipt

- **URL**: `/receipts/process`
- **Method**: `POST`
- **Request Body**: Receipt JSON
- **Response**: JSON containing an ID for the receipt

Example Request:
```json
{
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
```

Example Response:
```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### Get Points

- **URL**: `/receipts/{id}/points`
- **Method**: `GET`
- **Response**: JSON containing the number of points awarded

Example Response:
```json
{
  "points": 32
}
```

## Points Calculation Rules

Points are calculated based on the following rules:

1. One point for every alphanumeric character in the retailer name.
2. 50 points if the total is a round dollar amount with no cents.
3. 25 points if the total is a multiple of 0.25.
4. 5 points for every two items on the receipt.
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
6. 6 points if the day in the purchase date is odd.
7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.

## Implementation Notes

The pydantic models have been generated using fastapi-code-generator (https://github.com/koxudaxi/fastapi-code-generator) and the provided openapi specification.
