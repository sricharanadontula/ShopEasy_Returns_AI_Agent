
from langgraph.graph import StateGraph, START, END

from agent.state import ReturnAgentState

from tools.data_tools import (
    get_request,
    get_order,
    get_customer
)

from tools.reason_classifier import classify_reason

from tools.business_rules import apply_return_rules

from tools.action_tools import (
    issue_refund,
    send_customer_message
)


# --------------------------------------------------
# NODE 1: RETRIEVE REQUEST, ORDER AND CUSTOMER DATA
# --------------------------------------------------

def retrieve_data(state: ReturnAgentState):

    try:
        request = get_request.invoke({
            "request_id": state["request_id"]
        })

        order = get_order.invoke({
            "order_id": request["order_id"]
        })

        customer = get_customer.invoke({
            "customer_id": order["customer_id"]
        })

        print("\n--- CUSTOMER AND ORDER DETAILS ---")
        print("Request:", request)
        print("Order:", order)
        print("Customer:", customer)

        return {
            "request": request,
            "order": order,
            "customer": customer,
            "status": "DATA_RETRIEVED"
        }

    except Exception as e:
        return {
            "status": "HUMAN_TAKEOVER",
            "error": str(e),
            "decision": "MANUAL_REVIEW",
            "decision_reason": "Unable to retrieve complete customer or order data."
        }


# --------------------------------------------------
# NODE 2: CLASSIFY RETURN REASON USING LLM
# --------------------------------------------------

def classify_return_reason(state: ReturnAgentState):

    try:
        reason_category = classify_reason.invoke({
            "reason_text": state["request"]["reason_text"]
        })

        print("\n--- LLM CLASSIFICATION ---")
        print("Reason category:", reason_category)

        return {
            "reason_category": reason_category,
            "status": "REASON_CLASSIFIED"
        }

    except Exception as e:
        return {
            "status": "HUMAN_TAKEOVER",
            "error": str(e),
            "decision": "MANUAL_REVIEW",
            "decision_reason": "Return reason classification failed."
        }


# --------------------------------------------------
# NODE 3: APPLY SIX BUSINESS RULES
# --------------------------------------------------

def apply_business_rules(state: ReturnAgentState):

    try:
        request = state["request"]
        order = state["order"]
        customer = state["customer"]

        result = apply_return_rules.invoke({
            "category": order["category"],
            "delivery_status": order["delivery_status"],
            "days_since_delivery": int(order["days_since_delivery"]),
            "customer_tier": customer["tier"],
            "returns_last_90d": int(customer["returns_last_90d"]),
            "reason_category": state["reason_category"],
            "has_photo": request["has_photo"]
        }) 

        print("\n--- BUSINESS RULE RESULT ---")
        print("Decision:", result["decision"])
        print("Reason:", result["reason"])

        return {
            "decision": result["decision"],
            "decision_reason": result["reason"],
            "status": "RULES_APPLIED"
        }

    except Exception as e:
        return {
            "status": "HUMAN_TAKEOVER",
            "error": str(e),
            "decision": "MANUAL_REVIEW",
            "decision_reason": "Business rule evaluation failed."
        }


# --------------------------------------------------
# NODE 4: TAKE ACTION AND SEND CUSTOMER MESSAGE
# --------------------------------------------------

def take_action(state: ReturnAgentState):

    decision = state["decision"]
    request = state["request"]
    order = state["order"]
    customer = state["customer"]

    request_id = request["request_id"]
    customer_id = order["customer_id"]

    try:

        # APPROVED REFUND
        if decision == "APPROVE_REFUND":

            refund_result = issue_refund.invoke({
                "request_id": request_id,
                "order_id": order["order_id"],
                "amount_inr": float(order["price_inr"]),
                "payment_mode": order["payment_mode"]
            })

            print("\n--- REFUND RESULT ---")
            print(refund_result)

            if refund_result["status"] == "AWAITING_BANK_DETAILS":
                message = (
                    "Your return has been approved. "
                    "Since your original payment was Cash on Delivery, "
                    "please provide your bank transfer details through "
                    "ShopEasy's official secure channel. "
                    "Never share your card number, CVV or OTP."
                )

            elif refund_result["status"] == "ALREADY_RECORDED":
                message = (
                    "A refund record already exists for your return. "
                    "Please check your refund status through ShopEasy support."
                )

            else:
                message = (
                    f"Your return has been approved and a mock refund of "
                    f"INR {order['price_inr']} has been recorded."
                )

            action_result = refund_result

        # HUMAN REVIEW
        elif decision in ["ESCALATE_ABUSE_REVIEW", "MANUAL_REVIEW"]:

            message = (
                "Your return request requires additional review by "
                "our customer support team. We will update you after review."
            )

            action_result = {
                "status": "HUMAN_TAKEOVER",
                "decision": decision
            }

        # ALL OTHER DECISIONS
        else:

            message_templates = {
                "CANCEL_INSTEAD": (
                    "Your order has not been delivered yet. "
                    "Please contact ShopEasy support to request cancellation."
                ),
                "REJECT_GROCERY": (
                    "This grocery item is not eligible for a return "
                    "under our return policy."
                ),
                "REJECT_WINDOW_EXPIRED": (
                    "Your return request is outside the applicable "
                    "return window and cannot be approved."
                ),
                "REQUEST_PHOTO": (
                    "Please upload a clear photo of the damaged or "
                    "incorrect item so we can review your return request."
                )
            }

            message = message_templates.get(
                decision,
                "Your return request requires further review."
            )

            action_result = {
                "status": "NO_REFUND",
                "decision": decision
            }

        # SEND CUSTOMER MESSAGE
        message_result = send_customer_message.invoke({
            "request_id": request_id,
            "customer_id": customer_id,
            "message": message
        })

        print("\n--- CUSTOMER MESSAGE ---")
        print(message_result)

        return {
            "action_result": action_result,
            "customer_message": message,
            "status": "COMPLETED"
        }

    except Exception as e:

        return {
            "status": "HUMAN_TAKEOVER",
            "error": str(e),
            "decision_reason": "An error occurred while processing the return."
        }


# --------------------------------------------------
# CONDITIONAL ROUTING
# --------------------------------------------------

def check_status(state: ReturnAgentState):

    if state.get("status") == "HUMAN_TAKEOVER":
        return "end"

    return "continue"


# --------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

workflow = StateGraph(ReturnAgentState)

workflow.add_node("retrieve_data", retrieve_data)
workflow.add_node("classify_reason", classify_return_reason)
workflow.add_node("apply_business_rules", apply_business_rules)
workflow.add_node("take_action", take_action)

workflow.add_edge(START, "retrieve_data")

workflow.add_conditional_edges(
    "retrieve_data",
    check_status,
    {
        "continue": "classify_reason",
        "end": END
    }
)

workflow.add_conditional_edges(
    "classify_reason",
    check_status,
    {
        "continue": "apply_business_rules",
        "end": END
    }
)

workflow.add_conditional_edges(
    "apply_business_rules",
    check_status,
    {
        "continue": "take_action",
        "end": END
    }
)

workflow.add_edge("take_action", END)

# Compile the graph
return_agent = workflow.compile()
