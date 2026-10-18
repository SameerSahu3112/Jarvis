import ollama
from Hand import run_app, run_website
from logger import log

client = ollama.Client()
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = (
    "You are Jarvis, a voice assistant. Reply in one or two short sentences. "
    "Use a tool when the user wants to open an app or a website. "
    "Otherwise answer normally."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application on the laptop",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string",
                             "description": "App name, e.g. calculator, vs code, whatsapp, safari"}
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Open a website in the browser",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string",
                             "description": "Website name, e.g. youtube, google, gmail"}
                },
                "required": ["name"],
            },
        },
    },
]

# The allow-list: the LLM can only trigger these functions
SKILLS = {"open_app": run_app, "open_website": run_website}

history = [{"role": "system", "content": SYSTEM_PROMPT}]

def ask_jarvis(user_text):
    history.append({"role": "user", "content": user_text})

    for _ in range(3):                      # at most 3 steps per request
        response = client.chat(model=MODEL, messages=history, tools=TOOLS)
        msg = response["message"]
        history.append(msg)

        if not msg.get("tool_calls"):       # no tool needed, so this is the answer
            return msg["content"]

        for call in msg["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            skill = SKILLS.get(name)
            if skill is None:
                result = f"Failed: unknown tool {name}"
            else:
                try:
                    result = skill(**args)
                except Exception as e:
                    result = f"Failed: {e}"
            log(f"TOOL | {name} {args} | {result}")
            history.append({"role": "tool", "tool_name": name, "content": result})

    return "Sorry, I couldn't finish that."