
import csv
from pathlib import Path
from datetime import datetime, timezone
from langchain.tools import tool


# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REFUNDS_FILE = OUTPUT_DIR / "refunds.csv"
OUTBOX_FILE = OUTPUT_DIR / "outbox.csv"


def initialize_csv(file_path, headers):
    """Create a CSV with headers or repair a file missing its header row."""

    if not file_path.exists() or file_path.stat().st_size == 0:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        return

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.reader(file))

    if not rows:
        rows = []

    if rows[0] != headers:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)


def append_csv(file_path, row):
    """Append one record to a CSV file."""
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)


initialize_csv(
    REFUNDS_FILE,
    [
        "refund_id",
        "request_id",
        "order_id",
        "amount_inr",
        "payment_mode",
        "refund_status",
        "timestamp"
    ]
)

initialize_csv(
    OUTBOX_FILE,
    [
        "request_id",
        "customer_id",
        "message",
        "timestamp"
    ]
)


@tool
def issue_refund(
    request_id: str,
    order_id: str,
    amount_inr: float,
    payment_mode: str
) -> dict:
    """
    Create a mock refund record for an approved return.
    COD orders require bank transfer details before processing.
    """

    # Prevent duplicate refund records
    with open(REFUNDS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if record["request_id"] == request_id:
                return {
                    "status": "ALREADY_RECORDED",
                    "refund_id": record["refund_id"],
                    "message": "A refund record already exists for this request."
                }

    timestamp = datetime.now(timezone.utc).isoformat()
    refund_id = f"REF-{request_id}"

    if payment_mode.strip().upper() == "COD":
        refund_status = "AWAITING_BANK_DETAILS"

        result_message = (
            "Refund is pending. Please provide bank account details "
            "through ShopEasy's secure official channel. "
            "Never share your card number, CVV or OTP."
        )

    else:
        refund_status = "MOCK_REFUND_ISSUED"

        result_message = (
            f"Mock refund of INR {amount_inr:.2f} "
            f"recorded against {payment_mode}."
        )

    append_csv(
        REFUNDS_FILE,
        [
            refund_id,
            request_id,
            order_id,
            amount_inr,
            payment_mode,
            refund_status,
            timestamp
        ]
    )

    return {
        "refund_id": refund_id,
        "status": refund_status,
        "message": result_message
    }


@tool
def send_customer_message(
    request_id: str,
    customer_id: str,
    message: str
) -> dict:
    """Record a customer notification in the mock outbox."""

    initialize_csv(
        OUTBOX_FILE,
        ["request_id", "customer_id", "message", "timestamp"]
    )

    with open(OUTBOX_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if record["request_id"] == request_id:
                return {
                    "status": "ALREADY_RECORDED",
                    "request_id": request_id,
                    "message": "A customer message already exists for this request."
                }

    timestamp = datetime.now(timezone.utc).isoformat()

    append_csv(
        OUTBOX_FILE,
        [
            request_id,
            customer_id,
            message,
            timestamp
        ]
    )

    return {
        "status": "MESSAGE_RECORDED",
        "request_id": request_id,
        "message": "Customer message successfully recorded in mock outbox."
    }



# Export action tools
action_tools = [
    issue_refund,
    send_customer_message
]
