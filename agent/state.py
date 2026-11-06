
from typing import TypedDict, Optional


class ReturnAgentState(TypedDict, total=False):
    # Initial input
    request_id: str

    # Retrieved information
    request: dict
    order: dict
    customer: dict

    # LLM classification
    reason_category: str

    # Business rule result
    decision: str
    decision_reason: str

    # Action details
    action_result: dict
    customer_message: str

    # Execution status
    status: str
    error: Optional[str]
