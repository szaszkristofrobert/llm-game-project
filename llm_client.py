from config import OLLAMA_MODEL


def call_llm(system_prompt: str, user_prompt: str) -> str:
    import ollama

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0.7},
    )
    return response["message"]["content"]
