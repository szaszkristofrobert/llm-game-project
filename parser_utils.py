import re

def parse_response(text: str) -> tuple[str, str]:
    decision_match = re.search(r"<decision>(.*?)</decision>", text, re.DOTALL | re.IGNORECASE)
    response_match = re.search(r"<response>(.*?)</response>", text, re.DOTALL | re.IGNORECASE)

    decision = decision_match.group(1).strip() if decision_match else "tamadas"
    response = response_match.group(1).strip() if response_match else "Folytatjuk a harcot."

    decision = decision.lower()
    if decision not in {"tamadas", "feladas"}:
        decision = "tamadas"

    return decision, response
