
from tools.business_rules import apply_return_rules


test_cases = [

    # Rule 1: Not delivered
    {
        "category": "Fashion",
        "delivery_status": "Shipped",
        "days_since_delivery": 0,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "damaged",
        "has_photo": "Y",
        "expected": "CANCEL_INSTEAD"
    },

    # Rule 2: Grocery damaged with photo
    {
        "category": "Grocery",
        "delivery_status": "Delivered",
        "days_since_delivery": 2,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "damaged",
        "has_photo": "Y",
        "expected": "APPROVE_REFUND"
    },

    # Rule 2: Grocery without photo
    {
        "category": "Grocery",
        "delivery_status": "Delivered",
        "days_since_delivery": 2,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "damaged",
        "has_photo": "N",
        "expected": "REJECT_GROCERY"
    },

    # Rule 3: Frequent returns
    {
        "category": "Fashion",
        "delivery_status": "Delivered",
        "days_since_delivery": 5,
        "customer_tier": "Regular",
        "returns_last_90d": 5,
        "reason_category": "size_fit",
        "has_photo": "N",
        "expected": "ESCALATE_ABUSE_REVIEW"
    },

    # Rule 4: Regular customer, expired window
    {
        "category": "Fashion",
        "delivery_status": "Delivered",
        "days_since_delivery": 16,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "size_fit",
        "has_photo": "N",
        "expected": "REJECT_WINDOW_EXPIRED"
    },

    # Rule 4: Platinum exactly at extended limit
    {
        "category": "Fashion",
        "delivery_status": "Delivered",
        "days_since_delivery": 20,
        "customer_tier": "Platinum",
        "returns_last_90d": 0,
        "reason_category": "size_fit",
        "has_photo": "N",
        "expected": "APPROVE_REFUND"
    },

    # Rule 4: Platinum one day over limit
    {
        "category": "Fashion",
        "delivery_status": "Delivered",
        "days_since_delivery": 21,
        "customer_tier": "Platinum",
        "returns_last_90d": 0,
        "reason_category": "size_fit",
        "has_photo": "N",
        "expected": "REJECT_WINDOW_EXPIRED"
    },

    # Rule 5: Damaged without photo
    {
        "category": "Electronics",
        "delivery_status": "Delivered",
        "days_since_delivery": 3,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "damaged",
        "has_photo": "N",
        "expected": "REQUEST_PHOTO"
    },

    # Rule 6: Normal approval
    {
        "category": "Home",
        "delivery_status": "Delivered",
        "days_since_delivery": 5,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "change_of_mind",
        "has_photo": "N",
        "expected": "APPROVE_REFUND"
    },

    # Wrong item without photo
    {
        "category": "Fashion",
        "delivery_status": "Delivered",
        "days_since_delivery": 5,
        "customer_tier": "Regular",
        "returns_last_90d": 0,
        "reason_category": "wrong_item",
        "has_photo": "N",
        "expected": "REQUEST_PHOTO"
    }
]


passed = 0

for i, case in enumerate(test_cases, start=1):

    expected = case.pop("expected")

    result = apply_return_rules.invoke(case)

    actual = result["decision"]

    status = "PASSED" if actual == expected else "FAILED"

    print(f"\nTest {i}: {status}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")

    if actual == expected:
        passed += 1

print(f"\nFinal Result: {passed}/{len(test_cases)} tests passed.")
