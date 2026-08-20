import pandas as pd
import json
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()


def load_transactions(csv_path: str):
    """
    Load fraud detection dataset file.
    """
    df = pd.read_csv(csv_path)

    return df.to_dict(orient="records")


def apply_rules(transaction: dict):
    """
    Apply rule-based fraud detection.
    """

    reasons = []

    # Rule 1
    if transaction["amount_inr"] > 100000:
        reasons.append("High Transaction Amount")

    # Rule 2
    if transaction["velocity_last_1hr"] > 5:
        reasons.append("High Transaction Velocity")

    # Rule 3
    if transaction["geo_distance_km"] > 500:
        reasons.append("Large Geo Distance")

    # Rule 4
    if transaction["behavioural_deviation_score"] > 0.80:
        reasons.append("Behavioural Anomaly")

    # Rule 5
    if transaction["num_alerts"] >= 3:
        reasons.append("Multiple Alerts")

    return reasons


SYSTEM_PROMPT = """
You are a Banking Transaction Monitoring Agent.
Role: Primary Surveillance
Responsibilities:Monitor banking transactions. Review rule-based alerts.
Analyze transaction behaviour. Determine whether the transaction should be:
LOW, MEDIUM, HIGH, CRITICAL. Always explain your reasoning. Return ONLY JSON.

# Example

# {
#     "risk_level":"HIGH",
#     "confidence":92,
#     "summary":"Large transfer from unusual location",
#     "recommendation":"Send to Investigation Agent"
# }
"""


transaction_agent = create_agent(model="openai:gpt-5.5", system_prompt=SYSTEM_PROMPT)


def monitor_transaction(transaction: dict):

    triggered_rules = apply_rules(transaction)

    prompt = f"""Transaction{json.dumps(transaction, indent=2)}
Triggered Rules {triggered_rules} Analyze this transaction.
Return JSON only.
"""
    response = transaction_agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )

    return response["messages"][-1].content


transactions = load_transactions("data/fraud_detection.csv")

for transaction in transactions[:2]:

    result = monitor_transaction(transaction)

    print("=" * 80)
    print(result)
