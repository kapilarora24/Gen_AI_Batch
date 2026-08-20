from src.api.v1.tools.output_guardrail import (
    output_guardrail,
)

tests = [
    {"answer": "Customer mobile number is 9876543210"},
    {"answer": "Customer email is john.smith@gmail.com"},
    {"answer": "Customer mobile is +91 9876543210 and email is john@gmail.com"},
    {"answer": "Home loan tenure is 30 years"},
]


for item in tests:

    result = output_guardrail(item)

    print("\nINPUT:")
    print(item["answer"])

    print("OUTPUT:")
    print(result["answer"])

    print("STATUS:", result["output_guardrail_status"])

    print("PII:", result["detected_pii"])
