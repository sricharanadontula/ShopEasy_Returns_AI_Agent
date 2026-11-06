
import pandas as pd

from tools.action_tools import (
    issue_refund,
    send_customer_message
)


# Test 1: Card refund
card_result = issue_refund.invoke({
    "request_id": "TEST-CARD-001",
    "order_id": "TEST-ORDER-001",
    "amount_inr": 2499,
    "payment_mode": "Card"
})

print("\nCARD REFUND:")
print(card_result)


# Test 2: COD refund
cod_result = issue_refund.invoke({
    "request_id": "TEST-COD-001",
    "order_id": "TEST-ORDER-002",
    "amount_inr": 1500,
    "payment_mode": "COD"
})

print("\nCOD REFUND:")
print(cod_result)


# Test 3: Customer message
message_result = send_customer_message.invoke({
    "request_id": "TEST-CARD-001",
    "customer_id": "CUS201",
    "message": "Your return has been approved. Your mock refund has been recorded."
})

print("\nCUSTOMER MESSAGE:")
print(message_result)


# Test 4: Verify duplicate prevention
duplicate_result = issue_refund.invoke({
    "request_id": "TEST-CARD-001",
    "order_id": "TEST-ORDER-001",
    "amount_inr": 2499,
    "payment_mode": "Card"
})

print("\nDUPLICATE REFUND:")
print(duplicate_result)


# Verify CSV files
refunds = pd.read_csv("outputs/refunds.csv")
outbox = pd.read_csv("outputs/outbox.csv")

print("\nREFUND RECORDS:")
print(refunds)

print("\nOUTBOX RECORDS:")
print(outbox)
