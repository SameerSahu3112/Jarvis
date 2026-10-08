"""Send a text question to OpenAI and return Jarvis's answer."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.openai.com/v1/responses"
MODEL = "gpt-6-astra"


def ask_ai(question):
    """Return a short spoken-style answer to question, or an error message."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "The OpenAI API key is missing. Set OPENAI_API_KEY in the terminal first."

    request_body = {
        "model": MODEL,
        "instructions": (
            "You are Jarvis, a friendly personal assistant. "
            "Answer clearly and briefly because your answer will be spoken aloud. "
            "Never claim you performed an action on the computer."
        ),
        "input": question,
    }

    request = Request(
        API_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return f"OpenAI returned an error, HTTP {error.code}. Check the API key and account."
    except URLError:
        return "I could not connect to OpenAI. Check the internet connection and try again."
    except TimeoutError:
        return "OpenAI took too long to answer. Please try again."
    except (ValueError, KeyError):
        return "I received a response I could not read. Please try again."

    answer_parts = []
    for item in result.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                answer_parts.append(content.get("text", ""))

    answer = " ".join(part for part in answer_parts if part).strip()
    if not answer:
        return "I did not get a text answer. Please ask me again."
    return answer
