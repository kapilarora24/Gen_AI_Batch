# Question 17: Force Structured LLM Output
# Difficulty: Hard
# Topic: Prompt Engineering and Structured Output
#
# Problem Statement:
# A mocked LLM returns structured JSON only when the prompt clearly asks for it.
# Complete the prompt builder so the bug report is turned into a reliable
# JSON-producing prompt, then parse the result.
#
# Expected Output:
# Login bug on mobile | high

import json


def mock_llm(prompt):
    if (
        "Return JSON with keys: summary and severity." in prompt
        and "Do not add extra text." in prompt
    ):
        return '{"summary": "Login bug on mobile", "severity": "high"}'
    return "The issue is a login bug."


def build_bug_prompt(report):
    return (
        "You are a release triage assistant.\n"
        f"Bug report: {report}\n"
        "Return JSON with keys: summary and severity."
        "Do not add extra text."
    )


def triage_bug(report):
    prompt = build_bug_prompt(report)
    raw = mock_llm(prompt)
    parsed = json.loads(raw)
    return f"{parsed['summary']} | {parsed['severity']}"


print(triage_bug("Users cannot log in on mobile after the latest release."))
