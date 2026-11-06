
import pandas as pd
from pathlib import Path

from agent.graph import return_agent


# Input and output files
REQUESTS_FILE = Path("data/return_requests.csv")
RESULTS_FILE = Path("outputs/results.csv")

RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)


def process_all_returns():

    requests_df = pd.read_csv(REQUESTS_FILE)

    results = []

    total = len(requests_df)

    print("\n" + "=" * 60)
    print("          SHOPEASY - BATCH RETURN PROCESSING")
    print("=" * 60)

    print(f"\nTotal requests to process: {total}\n")

    for index, row in requests_df.iterrows():

        request_id = str(row["request_id"])

        print("\n" + "-" * 50)
        print(f"Processing {index + 1}/{total}: {request_id}")
        print("-" * 50)

        try:

            result = return_agent.invoke({
                "request_id": request_id
            })

            results.append({
                "request_id": request_id,
                "decision": result.get("decision", "MANUAL_REVIEW"),
                "reason_category": result.get("reason_category", ""),
                "decision_reason": result.get("decision_reason", ""),
                "status": result.get("status", "UNKNOWN"),
                "customer_message": result.get("customer_message", ""),
                "action_status": result.get("action_result", {}).get(
                    "status", ""
                ),
                "error": result.get("error", "")
            })

            print("Decision:", result.get("decision", "UNKNOWN"))
            print("Status:", result.get("status", "UNKNOWN"))

        except Exception as e:

            print("Processing failed:", str(e))

            results.append({
                "request_id": request_id,
                "decision": "MANUAL_REVIEW",
                "reason_category": "",
                "decision_reason": "Unexpected processing error.",
                "status": "HUMAN_TAKEOVER",
                "customer_message": "",
                "action_status": "",
                "error": str(e)
            })

    # Save all results
    results_df = pd.DataFrame(results)

    results_df.to_csv(
        RESULTS_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\n" + "=" * 60)
    print("             BATCH PROCESSING SUMMARY")
    print("=" * 60)

    print(f"\nTotal requests: {len(results_df)}")

    print("\nDecision summary:")
    print(results_df["decision"].value_counts().to_string())

    print("\nProcessing status:")
    print(results_df["status"].value_counts().to_string())

    print(f"\nResults saved to: {RESULTS_FILE}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    process_all_returns()
