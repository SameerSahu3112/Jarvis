import json
from urllib.request import Request, urlopen
from urllib.error import URLError


API_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"  # Change this if `ollama list` shows another name.


def ask_ai(question):
    request_body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a friendly personal assistant. "
                    "Answer clearly and briefly because your answer will be spoken aloud."
                ),
            },
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    request = Request(
        API_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["message"]["content"].strip()
    except URLError:
        return "I could not connect to Ollama. Make sure the Ollama app is running."
    except (KeyError, ValueError):
        return "I received a response I could not read. Please try again."