
from agent.graph import return_agent


def process_return(request_id: str):
    """Process one customer return request using the ShopEasy agent."""

    print("\n" + "=" * 55)
    print("             SHOPEASY RETURNS AI AGENT")
    print("=" * 55)

    print(f"\nProcessing Return Request: {request_id}")

    initial_state = {
        "request_id": request_id
    }

    try:
        # Execute the LangGraph workflow
        result = return_agent.invoke(initial_state)

        print("\n" + "=" * 55)
        print("                 FINAL RESULT")
        print("=" * 55)

        print(f"\nRequest ID: {request_id}")
        print(f"Status: {result.get('status', 'UNKNOWN')}")
        print(f"Decision: {result.get('decision', 'NOT AVAILABLE')}")
        print(f"Reason: {result.get('decision_reason', 'Not available')}")

        if result.get("reason_category"):
            print(f"Classified Reason: {result['reason_category']}")

        if result.get("action_result"):
            print(f"Action Result: {result['action_result']}")

        if result.get("customer_message"):
            print("\nCustomer Message:")
            print(result["customer_message"])

        if result.get("error"):
            print("\nError:", result["error"])

        print("\n" + "=" * 55)

        return result

    except Exception as e:
        print("\nUnexpected processing error:", str(e))
        return {
            "request_id": request_id,
            "status": "HUMAN_TAKEOVER",
            "error": str(e)
        }


if __name__ == "__main__":

    request_id = input(
        "\nEnter Return Request ID (example: RET9001): "
    ).strip()

    if not request_id:
        print("Please enter a valid Return Request ID.")
    else:
        process_return(request_id)
