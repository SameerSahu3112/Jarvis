import ollama

def ask_jarvis(question):
    client = ollama.Client()

    response = client.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]