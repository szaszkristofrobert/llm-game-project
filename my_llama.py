from ollama import chat

messages = []

def send_message(user_prompt: str):
    # Add user message to the history
    messages.append({"role": "user", "content": user_prompt})

    # Send whole history to Ollama
    response = chat(
        model="llama3.1",
        messages=messages
    )

    # Extract and print assistant reply
    assistant_msg = response["message"]["content"]

    # Append assistant reply to the history
    messages.append({"role": "assistant", "content": assistant_msg})

    return response

# Start the conversation
#send_message("Hello!")
# Continue the same conversation
#send_message("What did I just say?")