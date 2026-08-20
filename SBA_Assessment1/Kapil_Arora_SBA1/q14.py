# Question 14: Parse a Mocked LLM Response
# Difficulty: Medium
# Topic: Mocked LLM Output Parsing
#
# Problem Statement:
# A support workflow sends a ticket description to a mocked LLM and expects
# JSON back. Complete the function so it parses the JSON and formats the
# label and tone in the required output style.
#
# Expected Output:
# billing | urgent

import json


def mock_llm(prompt):
    if "refund" in prompt.lower():
        return '{"label": "billing", "tone": "urgent"}'
    return '{"label": "general", "tone": "neutral"}'


def categorize_ticket(text):
    prompt = (
        "Classify the support ticket.\n"
        f"Ticket: {text}\n"
        "Return JSON with keys: label and tone."
    )
    raw = mock_llm(prompt)
    parsed = json.loads(raw)
    return f"{parsed['label']} | {parsed['tone']}"


print(categorize_ticket("Customer requested a refund for a duplicate charge"))
