import ollama

def ask_jarvis(question):
    client = ollama.Client()

    response = client.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]