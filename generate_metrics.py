
import pandas as pd
from pathlib import Path

# File paths
OUTPUT_DIR = Path("outputs")

results = pd.read_csv(OUTPUT_DIR / "results.csv")
requests = pd.read_csv("data/return_requests.csv")

refunds = pd.read_csv(OUTPUT_DIR / "refunds.csv")
outbox = pd.read_csv(OUTPUT_DIR / "outbox.csv")

# Keep only records belonging to the 40 assignment requests.
# This excludes earlier TEST records.
request_ids = set(requests["request_id"].astype(str))

refunds = refunds[
    refunds["request_id"].astype(str).isin(request_ids)
]

outbox = outbox[
    outbox["request_id"].astype(str).isin(request_ids)
]

# Basic metrics
total_requests = len(results)
completed = (results["status"] == "COMPLETED").sum()
failed = (results["status"] != "COMPLETED").sum()

decision_counts = results["decision"].value_counts()

# Build decision summary
decision_summary = decision_counts.reset_index()
decision_summary.columns = ["decision", "request_count"]

decision_summary["percentage"] = (
    decision_summary["request_count"] / total_requests * 100
).round(2)

decision_summary.to_csv(
    OUTPUT_DIR / "decision_summary.csv",
    index=False
)

# Refund metrics
refund_count = len(refunds)

refund_status_counts = (
    refunds["refund_status"].value_counts()
    if "refund_status" in refunds.columns
    else pd.Series(dtype=int)
)

# Message metrics
messages_sent = len(outbox)

# Error metrics
errors = (
    results["error"].astype("string").fillna("").str.strip().ne("").sum()
    if "error" in results.columns
    else 0
)

# Generate report
report = f"""
SHOPEASY RETURNS AI AGENT
MONITORING AND METRICS REPORT
========================================

1. REQUEST PROCESSING

Total requests: {total_requests}
Successfully completed: {completed}
Incomplete/failed: {failed}
Completion rate: {(completed / total_requests * 100) if total_requests else 0:.2f}%

2. DECISION DISTRIBUTION

{decision_summary.to_string(index=False)}

3. MOCK REFUND METRICS

Total refund records: {refund_count}

{refund_status_counts.to_string()}

4. CUSTOMER COMMUNICATION

Customer messages recorded: {messages_sent}

5. ERROR MONITORING

Errors recorded in results: {errors}

6. OBSERVABILITY

Tracing platform: LangSmith
LLM provider: NVIDIA Nemotron
Workflow framework: LangGraph

LangSmith traces should be used to inspect:
- Execution traces
- LLM latency
- Token usage
- Tool execution
- Errors and failures

========================================
END OF REPORT
"""

report_path = OUTPUT_DIR / "monitoring_report.txt"

report_path.write_text(report, encoding="utf-8")

print(report)
print(f"\nReport saved to: {report_path}")
print(f"Decision summary saved to: {OUTPUT_DIR / 'decision_summary.csv'}")
