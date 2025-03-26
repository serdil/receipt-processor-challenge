from datetime import date, time
from receiptprocessor.app import calculate_points
from receiptprocessor.models import Receipt, Item

def test_retailer_name_points():
    """Test rule 1: One point for every alphanumeric character in the retailer name."""
    receipt = Receipt(
        retailer="Target",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    assert calculate_points(receipt) == 88  # "Target" has 6 alphanumeric characters + other rules

    receipt = Receipt(
        retailer="M&M Corner Market",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    # "M&M Corner Market" has 14 alphanumeric characters (& is not alphanumeric) + other rules
    assert calculate_points(receipt) == 96

def test_round_dollar_amount_points():
    """Test rule 2: 50 points if the total is a round dollar amount with no cents."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="10.00")],
        total="10.00"
    )
    assert calculate_points(receipt) == 87  # 4 for retailer + 50 for round dollar + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="10.50")],
        total="10.50"
    )
    assert calculate_points(receipt) == 38  # 4 for retailer + other rules, no points for non-round dollar

def test_multiple_of_quarter_points():
    """Test rule 3: 25 points if the total is a multiple of 0.25."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="10.25")],
        total="10.25"
    )
    assert calculate_points(receipt) == 38  # 4 for retailer + 25 for multiple of 0.25 + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="10.10")],
        total="10.10"
    )
    assert calculate_points(receipt) == 13  # 4 for retailer + other rules, no points for non-multiple of 0.25

def test_items_count_points():
    """Test rule 4: 5 points for every two items on the receipt."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[
            Item(shortDescription="Item 1", price="1.00"),
            Item(shortDescription="Item 2", price="2.00"),
        ],
        total="3.00"
    )
    assert calculate_points(receipt) == 92  # 4 for retailer + 5 for 2 items + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[
            Item(shortDescription="Item 1", price="1.00"),
            Item(shortDescription="Item 2", price="2.00"),
            Item(shortDescription="Item 3", price="3.00"),
            Item(shortDescription="Item 4", price="4.00"),
            Item(shortDescription="Item 5", price="5.00"),
        ],
        total="15.00"
    )
    assert calculate_points(receipt) == 100  # 4 for retailer + 10 for 5 items (2 pairs) + other rules

def test_item_description_points():
    """Test rule 5: If the trimmed length of the item description is a multiple of 3, 
    multiply the price by 0.2 and round up to the nearest integer."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="ABC", price="10.00")],  # Length 3
        total="10.00"
    )
    assert calculate_points(receipt) == 87  # 4 for retailer + 2 for item (10.00 * 0.2 = 2) + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="ABCD", price="10.00")],  # Length 4
        total="10.00"
    )
    assert calculate_points(receipt) == 85  # 4 for retailer + other rules, no points for non-multiple of 3

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="   ABC   ", price="10.00")],  # Trimmed length 3
        total="10.00"
    )
    assert calculate_points(receipt) == 87  # 4 for retailer + 2 for item (10.00 * 0.2 = 2) + other rules

def test_odd_day_points():
    """Test rule 6: 6 points if the day in the purchase date is odd."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),  # Odd day
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    assert calculate_points(receipt) == 86  # 4 for retailer + 6 for odd day + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 2),  # Even day
        purchaseTime=time(13, 1),
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    assert calculate_points(receipt) == 80  # 4 for retailer + other rules, no points for even day

def test_purchase_time_points():
    """Test rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm."""
    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(14, 30),  # 2:30 PM
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    assert calculate_points(receipt) == 96  # 4 for retailer + 6 for odd day + 10 for time + other rules

    receipt = Receipt(
        retailer="Test",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 30),  # 1:30 PM
        items=[Item(shortDescription="Test Item", price="1.00")],
        total="1.00"
    )
    assert calculate_points(receipt) == 86  # 4 for retailer + 6 for odd day + other rules, no points for time

def test_combined_rules():
    """Test all rules combined with the examples from the task description."""
    # Example 1
    receipt = Receipt(
        retailer="Target",
        purchaseDate=date(2022, 1, 1),
        purchaseTime=time(13, 1),
        items=[
            Item(shortDescription="Mountain Dew 12PK", price="6.49"),
            Item(shortDescription="Emils Cheese Pizza", price="12.25"),
            Item(shortDescription="Knorr Creamy Chicken", price="1.26"),
            Item(shortDescription="Doritos Nacho Cheese", price="3.35"),
            Item(shortDescription="   Klarbrunn 12-PK 12 FL OZ  ", price="12.00"),
        ],
        total="35.35"
    )
    assert calculate_points(receipt) == 28

    # Example 2
    receipt = Receipt(
        retailer="M&M Corner Market",
        purchaseDate=date(2022, 3, 20),
        purchaseTime=time(14, 33),
        items=[
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
        ],
        total="9.00"
    )
    assert calculate_points(receipt) == 109
