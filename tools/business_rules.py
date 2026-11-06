
from langchain.tools import tool


# Return windows for each product category
RETURN_WINDOWS = {
    "Electronics": 7,
    "Fashion": 15,
    "Home": 10,
    "Beauty": 7,
    "Grocery": 0
}


@tool
def apply_return_rules(
    category: str,
    delivery_status: str,
    days_since_delivery: int,
    customer_tier: str,
    returns_last_90d: int,
    reason_category: str,
    has_photo: str
) -> dict:
    """
    Apply ShopEasy's six business rules in order
    and return the final decision with an explanation.
    """

    category = category.strip().title()
    delivery_status = delivery_status.strip().title()
    customer_tier = customer_tier.strip().title()
    reason_category = reason_category.strip().lower()
    has_photo = has_photo.strip().upper()

    # RULE 1: Order not delivered
    if delivery_status != "Delivered":
        return {
            "decision": "CANCEL_INSTEAD",
            "reason": "Order has not been delivered. Customer should cancel the order instead of requesting a return."
        }

    # RULE 2: Grocery products
    if category == "Grocery":

        if reason_category in ["damaged", "wrong_item"] and has_photo == "Y":
            return {
                "decision": "APPROVE_REFUND",
                "reason": "Grocery item was damaged or incorrect and photo evidence is available."
            }

        return {
            "decision": "REJECT_GROCERY",
            "reason": "Grocery products are not eligible for returns unless damaged or incorrect with photo evidence."
        }

    # RULE 3: Frequent returns
    if returns_last_90d >= 5:
        return {
            "decision": "ESCALATE_ABUSE_REVIEW",
            "reason": "Customer has made five or more returns in the last 90 days. Human review is required."
        }

    # RULE 4: Return window
    allowed_days = RETURN_WINDOWS.get(category)

    if allowed_days is None:
        return {
            "decision": "MANUAL_REVIEW",
            "reason": f"Unknown product category: {category}."
        }

    if customer_tier == "Platinum":
        allowed_days += 5

    if days_since_delivery > allowed_days:
        return {
            "decision": "REJECT_WINDOW_EXPIRED",
            "reason": f"Return window expired. Allowed window is {allowed_days} days."
        }

    # RULE 5: Photo evidence
    if reason_category in ["damaged", "wrong_item"] and has_photo == "N":
        return {
            "decision": "REQUEST_PHOTO",
            "reason": "Photo evidence is required for damaged or incorrect items."
        }

    # RULE 6: Default approval
    return {
        "decision": "APPROVE_REFUND",
        "reason": "Return request satisfies all eligibility rules. Refund can be processed to the original payment mode."
    }


# Export business rule tool
business_rule_tools = [apply_return_rules]
