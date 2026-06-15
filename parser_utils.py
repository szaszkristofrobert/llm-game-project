import re


def parse_response(text: str) -> tuple[str, str]:
    response_match = re.search(r"<response>(.*?)</response>", text, re.DOTALL | re.IGNORECASE)

    response = response_match.group(1).strip() if response_match else "We continue the fight."

    return response
