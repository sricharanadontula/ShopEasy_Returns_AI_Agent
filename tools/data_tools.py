
import pandas as pd
from pathlib import Path
from langchain.tools import tool

# Locate project data directory
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# Load CSV files
customers_df = pd.read_csv(DATA_DIR / "customers.csv")
orders_df = pd.read_csv(DATA_DIR / "orders.csv")
requests_df = pd.read_csv(DATA_DIR / "return_requests.csv")


@tool
def get_request(request_id: str) -> dict:
    """Retrieve return request details using a request ID."""
    result = requests_df[requests_df["request_id"] == request_id]

    if result.empty:
        raise ValueError(f"Return request {request_id} not found.")

    return result.iloc[0].to_dict()


@tool
def get_order(order_id: str) -> dict:
    """Retrieve order information using an order ID."""
    result = orders_df[orders_df["order_id"] == order_id]

    if result.empty:
        raise ValueError(f"Order {order_id} not found.")

    return result.iloc[0].to_dict()


@tool
def get_customer(customer_id: str) -> dict:
    """Retrieve customer information using a customer ID."""

    result = customers_df[
        customers_df["customer_id"] == customer_id
    ]

    if result.empty:
        raise ValueError(f"Customer {customer_id} not found.")

    customer = result.iloc[0].to_dict()

    # Trainer-confirmed mapping: Gold means Platinum
    if customer["tier"] == "Gold":
        customer["tier"] = "Platinum"

    return customer


# Collection of retrieval tools
data_tools = [
    get_request,
    get_order,
    get_customer
]
