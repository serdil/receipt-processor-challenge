import pytest
from fastapi.testclient import TestClient
from receiptprocessor.app import app, receipts_db

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_receipts_db():
    """
    Clear the receipts database before each test.
    This ensures that tests don't interfere with each other.
    """
    receipts_db.clear()
    yield
    receipts_db.clear()