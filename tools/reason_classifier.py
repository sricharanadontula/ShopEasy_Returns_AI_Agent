
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Load environment variables
load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")
BASE_URL = os.getenv("NVIDIA_BASE_URL")

if not API_KEY:
    raise ValueError("NVIDIA_API_KEY is missing from .env")

# Initialize NVIDIA LLM through OpenAI-compatible API
llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0
)

# Allowed reason categories
VALID_CATEGORIES = {
    "damaged",
    "wrong_item",
    "size_fit",
    "change_of_mind",
    "quality_mismatch",
    "defect_after_use",
    "late_delivery"
}


@tool
def classify_reason(reason_text: str) -> str:
    """
    Classify a customer's return reason into one of seven
    predefined categories using an LLM.
    """

    prompt = f"""
    You are a return-reason classification assistant
    for ShopEasy, an online shopping platform.

    Analyze the customer's return reason and classify it
    into exactly ONE of these categories:

    1. damaged
    2. wrong_item
    3. size_fit
    4. change_of_mind
    5. quality_mismatch
    6. defect_after_use
    7. late_delivery

    Classification guidelines:

    damaged:
    Product arrived physically damaged or broken.

    wrong_item:
    Customer received a different product from what
    they ordered.

    size_fit:
    Product does not fit or has an unsuitable size.

    change_of_mind:
    Customer no longer wants the product.

    quality_mismatch:
    Product quality does not match the description
    or customer's expectations.

    defect_after_use:
    Product stopped working or developed a defect
    after being used.

    late_delivery:
    Product arrived later than the promised date.

    Customer's reason:
    {reason_text}

    Return ONLY the category name.
    Do not provide explanations.
    """

    response = llm.invoke(prompt)

    category = response.content.strip().lower()

    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid classification returned by LLM: {category}"
        )

    return category


# Export tool
classifier_tools = [classify_reason]
