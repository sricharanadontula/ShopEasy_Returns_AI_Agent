# ShopEasy – AI-Powered Returns and Refund Agent

An intelligent customer returns and refund processing agent built using **LangGraph, LangChain, and NVIDIA Nemotron**. The system retrieves customer and order information, classifies return reasons using an LLM, applies business rules, processes mock refunds, and generates customer notifications.

## Project Overview

ShopEasy automates the return and refund decision-making process while following predefined business policies.

The agent processes return requests through a structured workflow and makes decisions such as:

- Approve refund
- Reject return
- Request additional product photos
- Suggest order cancellation
- Escalate suspicious requests for human review

The system also provides execution tracing and monitoring through LangSmith.

## Tech Stack

- **Programming Language:** Python
- **Agent Framework:** LangGraph
- **LLM Integration:** LangChain
- **LLM Provider:** NVIDIA Nemotron
- **Observability:** LangSmith
- **Data Processing:** Pandas
- **Data Storage:** CSV files

## Architecture and Workflow

1. Receive a return request ID.
2. Retrieve return request, order, and customer information.
3. Classify the customer's return reason using NVIDIA Nemotron.
4. Apply six predefined business rules using Python.
5. Determine the appropriate return decision.
6. Process a mock refund when approved.
7. Generate and record a customer notification.
8. Record execution traces through LangSmith.

## Business Rules

The agent follows these rules in priority order:

1. **Order not delivered:** Suggest cancellation instead of processing a return.
2. **Grocery items:** Reject returns unless the item is damaged or incorrect and photo evidence is provided.
3. **Frequent returns:** Escalate customers with five or more returns in the last 90 days for abuse review.
4. **Return window:** Check category-specific return windows. Platinum customers receive an additional five days.
5. **Photo verification:** Request a photo for damaged or incorrect items when evidence is missing.
6. **Default approval:** Approve requests that satisfy all applicable conditions.

### Return Windows

| Category | Return window |
|---|---:|
| Electronics | 7 days |
| Fashion | 15 days |
| Home | 10 days |
| Beauty | 7 days |
| Grocery | Not returnable, subject to the exception above |

## Project Structure

```text
ShopEasy/
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── return_requests.csv
│
├── tools/
│   ├── data_tools.py
│   ├── reason_classifier.py
│   ├── business_rules.py
│   └── action_tools.py
│
├── agent/
│   ├── state.py
│   └── graph.py
│
├── tests/
│   ├── test_data_tools.py
│   ├── test_classifier.py
│   ├── test_rules.py
│   └── test_action_tools.py
│
├── outputs/
│   ├── results.csv
│   ├── refunds.csv
│   ├── outbox.csv
│   ├── decision_summary.csv
│   └── monitoring_report.txt
│
├── main.py
├── process_all.py
├── generate_metrics.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ShopEasy
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=shopeasy-returns-agent
```

Never commit your actual `.env` file or API keys to GitHub.

### 5. Run an individual return request

```bash
python main.py
```

### 6. Process all 40 return requests

```bash
python process_all.py
```

### 7. Generate monitoring metrics

```bash
python generate_metrics.py
```

## Output Files

| File | Description |
|---|---|
| `results.csv` | Decisions and processing results for all requests |
| `refunds.csv` | Mock refund transaction records |
| `outbox.csv` | Customer notification records |
| `decision_summary.csv` | Decision distribution and percentages |
| `monitoring_report.txt` | Overall system monitoring report |

The refund and notification actions are simulated using CSV files. No actual money transfers or customer messages are sent.

## Monitoring and Observability

LangSmith is integrated to monitor:

- Agent execution traces
- LLM latency
- Token usage
- Tool execution
- Errors and failures

The monitoring report summarizes request completion, decision distribution, refund records, customer communication, and errors.

## Project Results

The system was tested on **40 return requests**.

| Metric | Result |
|---|---:|
| Total requests processed | 40 |
| Successfully completed | 40 |
| Completion rate | 100% |
| Customer messages recorded | 40 |
| Assignment refund records | 5 |
| Processing errors | 0 |

### Decision Distribution

| Decision | Requests |
|---|---:|
| Reject – Window expired | 16 |
| Cancel instead | 8 |
| Escalate for abuse review | 5 |
| Reject – Grocery | 5 |
| Approve refund | 5 |
| Request photo | 1 |

## Safety and Reliability

- Business rules are evaluated in Python rather than delegated to the LLM.
- Missing or invalid data is routed for human review.
- Refund records have duplicate-prevention checks.
- Customer notifications have duplicate-prevention checks.
- COD refunds require bank details through an official secure channel.
- Customers are never asked to share card numbers, CVVs, or OTPs.
- Submitted code or customer-provided text is not executed as code.

## Future Enhancements

- Integration with real e-commerce order management systems.
- Secure database storage instead of CSV files.
- Customer support dashboard.
- Real payment gateway integration.
- Advanced fraud detection and analytics.

## Author

**Sricharana Dontula**

B.Tech – Computer Science and Engineering (AI & ML)

Hyderabad, India