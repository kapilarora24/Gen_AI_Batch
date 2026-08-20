# Question 10: Build a Support Prompt
# Difficulty: Medium
# Topic: Prompt Engineering
#
# Problem Statement:
# A support assistant needs a clear prompt before sending a request to an LLM.
# Complete the function so the prompt includes the issue, the priority,
# and the exact response format instruction.
#
# Expected Output:
# You are a support assistant.
# Customer issue: Payment failed during checkout
# Priority: high
# Respond with: summary | next_step

ticket = {
    "issue": "Payment failed during checkout",
    "priority": "high",
}


def build_support_prompt(ticket):
    return (
        "You are a support assistant.\n"
        f"Customer issue: {ticket['issue']}\n"
        f"Priority: {ticket['priority']}\n"
        "provide resopnse"
    )


print(build_support_prompt(ticket))
