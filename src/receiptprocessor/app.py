from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_CEILING
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import constr

from .models import Receipt, ReceiptsIdPointsGetResponse, ReceiptsProcessPostResponse

app = FastAPI(
    title='Receipt Processor',
    description='A simple receipt processor',
    version='0.1.0',
)

# In-memory storage for receipts
receipts_db: Dict[str, Receipt] = {}

def calculate_points(receipt: Receipt) -> int:
    """
    Calculate points for a receipt based on the rules:
    1. One point for every alphanumeric character in the retailer name.
    2. 50 points if the total is a round dollar amount with no cents.
    3. 25 points if the total is a multiple of 0.25.
    4. 5 points for every two items on the receipt.
    5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
    6. 6 points if the day in the purchase date is odd.
    7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    """
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_points = sum(1 for char in receipt.retailer if char.isalnum())
    points += retailer_points

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total_decimal = Decimal(receipt.total)
    round_dollar_points = 50 if total_decimal % Decimal('1.00') == Decimal('0.00') else 0
    points += round_dollar_points

    # Rule 3: 25 points if the total is a multiple of 0.25
    quarter_multiple_points = 25 if total_decimal % Decimal('0.25') == Decimal('0.00') else 0
    points += quarter_multiple_points

    # Rule 4: 5 points for every two items on the receipt
    items_points = (len(receipt.items) // 2) * 5
    points += items_points

    # Rule 5: Points for item descriptions with length multiple of 3
    item_desc_points = 0
    for item in receipt.items:
        trimmed_desc = item.shortDescription.strip()
        if len(trimmed_desc) % 3 == 0:
            price_decimal = Decimal(item.price)
            item_point = (price_decimal * Decimal('0.2')).quantize(Decimal('1'), rounding=ROUND_CEILING)
            item_desc_points += item_point
    points += item_desc_points

    # Rule 6: 6 points if the day in the purchase date is odd
    odd_day_points = 6 if receipt.purchaseDate.day % 2 == 1 else 0
    points += odd_day_points

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_hour = receipt.purchaseTime.hour
    purchase_minute = receipt.purchaseTime.minute
    time_points = 10 if (purchase_hour == 14 and purchase_minute > 0) or (purchase_hour == 15) else 0
    points += time_points

    return points


@app.post(
    '/receipts/process',
    response_model=ReceiptsProcessPostResponse,
    responses={'200': {'model': ReceiptsProcessPostResponse}},
)
def post_receipts_process(body: Receipt) -> ReceiptsProcessPostResponse:
    """
    Submits a receipt for processing.
    """
    # Generate a unique ID for the receipt
    receipt_id = str(uuid.uuid4())

    # Store the receipt in memory
    receipts_db[receipt_id] = body

    # Return the ID
    return ReceiptsProcessPostResponse(id=receipt_id)


@app.get(
    '/receipts/{id}/points',
    response_model=ReceiptsIdPointsGetResponse,
    responses={'200': {'model': ReceiptsIdPointsGetResponse}},
)
def get_receipts_id_points(
    id: constr(pattern=r'^\S+$'),
) -> ReceiptsIdPointsGetResponse:
    """
    Returns the points awarded for the receipt.
    """
    # Check if the receipt exists
    if id not in receipts_db:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")

    # Get the receipt
    receipt = receipts_db[id]

    # Calculate the points
    points = calculate_points(receipt)

    # Return the points
    return ReceiptsIdPointsGetResponse(points=points)
