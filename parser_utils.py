import re


def parse_response(text: str) -> tuple[str, str]:
    decision_match = re.search(r"<decision>(.*?)</decision>", text, re.DOTALL | re.IGNORECASE)
    response_match = re.search(r"<response>(.*?)</response>", text, re.DOTALL | re.IGNORECASE)

    decision = decision_match.group(1).strip() if decision_match else "attack"
    response = response_match.group(1).strip() if response_match else "We continue the fight."

    decision = decision.lower()
    if decision not in {"attack", "surrender"}:
        decision = "attack"

    return decision, response
