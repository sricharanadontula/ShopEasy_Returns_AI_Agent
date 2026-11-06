
from tools.reason_classifier import classify_reason

test_reasons = [
    "Product is damaged on arrival",
    "I received a different item",
    "The shoes are too tight for me",
    "I changed my mind and don't need it",
    "The quality is not as advertised",
    "The device stopped working after one week",
    "My order arrived three days late"
]

for reason in test_reasons:

    result = classify_reason.invoke({
        "reason_text": reason
    })

    print(f"\nReason: {reason}")
    print(f"Classification: {result}")
