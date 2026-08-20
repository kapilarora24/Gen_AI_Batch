# Question 20: Evaluate a Candidate with a Mocked LLM
# Difficulty: Hard
# Topic: GenAI Workflow and Output Formatting
#
# Problem Statement:
# A hiring tool builds a prompt, sends it to a mocked LLM, parses the JSON,
# and formats the final decision report. Complete the prompt so the mocked
# LLM returns the structured response required by the workflow.
#
# Expected Output:
# role=Data Analyst
# skills=Python, SQL, Communication
# decision=interview

import json


def mock_llm(prompt):
    if (
        "Return JSON with keys: role, skills, decision." in prompt
        and "Use only the supplied profile." in prompt
    ):
        return (
            '{"role": "Data Analyst", "skills": ["Python", "SQL", '
            '"Communication"], "decision": "interview"}'
        )
    return '{"role": "Unknown", "skills": [], "decision": "reject"}'


def build_candidate_prompt(profile):
    return (
        "You are a hiring assistant.\n"
        f"Candidate summary: {profile}\n"
        "Return JSON with keys: role, skills, decision."
        "Use only the supplied profile."
    )


def evaluate_candidate(profile):
    prompt = build_candidate_prompt(profile)
    raw = mock_llm(prompt)
    parsed = json.loads(raw)
    skills = ", ".join(parsed["skills"])
    return (
        f"role={parsed['role']}\n" f"skills={skills}\n" f"decision={parsed['decision']}"
    )


profile = "3 years of analytics experience, strong Python and SQL, clear communicator."
print(evaluate_candidate(profile))
