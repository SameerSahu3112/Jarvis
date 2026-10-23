import ollama
from logger import log
from Hand import handle_command, open_website
from Stomach import memorize_text, show_memorized_texts
from Muscles import (
    battery_info, cpu_info, ram_info, disk_info,
    volume_command, mute, unmute, brightness_command,
    take_screenshot, create_folder, find_file,
    set_reminder,
)
from Eyes import list_folders, look_in_folder, read_file, look_at_screen, show_folder

MODEL = "qwen3:4b"      # must be a model that supports tools

client = ollama.Client()


def save_note(text=""):
    memorize_text(text)


def read_notes(text=""):
    show_memorized_texts()


# The allow-list. name -> (function, description the AI reads)
# ACTION tools speak for themselves. INFORMATION tools return text for the AI to read.
TOOL_LIST = {
    # actions
    "open_app": (handle_command, "Open an app on the laptop. text = app name, like calculator or vs code"),
    "open_website": (open_website, "Open a website. text = site name, like youtube or gmail"),
    "show_folder": (show_folder, "Open any folder in Finder. text = the folder name"),
    "battery": (battery_info, "Say the battery level"),
    "cpu": (cpu_info, "Say the CPU usage"),
    "ram": (ram_info, "Say the memory usage"),
    "disk": (disk_info, "Say the free disk space"),
    "volume": (volume_command, "Change the volume. text = up, down, or a number like 30"),
    "mute": (mute, "Mute the sound"),
    "unmute": (unmute, "Unmute the sound"),
    "brightness": (brightness_command, "Change screen brightness. text = up or down"),
    "screenshot": (take_screenshot, "Save a screenshot file on the desktop"),
    "new_folder": (create_folder, "Create a folder on the desktop. text = the folder name"),
    "find_file": (find_file, "Find a file by name and show it in Finder. text = the file name"),
    "reminder": (set_reminder, "Set a reminder. text = like: in 10 minutes to drink water"),
    "save_note": (save_note, "Save a note to memory. text = the note"),
    "read_notes": (read_notes, "Read the saved notes aloud"),

    # information
    "list_folders": (list_folders, "List the folders in the home folder, or inside a folder you name. text = folder name, or empty for all"),
    "look_in_folder": (look_in_folder, "Get the list of files inside a folder. text = the folder name"),
    "read_file": (read_file, "Read a text file so you can answer questions about it. text = the file name"),
    "look_at_screen": (look_at_screen, "Look at the screen and answer a question about it. text = the question"),
}

# Turn the list above into the format the model understands
TOOLS = []
for name, (function, description) in TOOL_LIST.items():
    TOOLS.append({
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "the request in a few words"}
                },
                "required": [],
            },
        },
    })

SYSTEM_PROMPT = (
    "You are Jarvis, a voice assistant on a Mac. "
    "Use the tools to do things on the laptop. "
    "Action tools speak for themselves, so after using only action tools just say Done. "
    "Information tools return text. Read that text carefully, then answer the user's question "
    "in two or three short sentences. If you need more information, call another tool. "
    "Never say you cannot see files or the screen, use the tools instead. "
    "Do not use bullet points or symbols."
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def trim_history():
    # keep the system prompt plus the latest messages
    while len(history) > 13:
        del history[1]
    while len(history) > 1 and history[1]["role"] != "user":
        del history[1]


def clean(answer):
    if "</think>" in answer:
        answer = answer.split("</think>")[-1]
    answer = answer.replace("*", "").replace("#", "").strip()
    return answer or "Done."


def ask_jarvis(question):
    trim_history()
    start = len(history)
    history.append({"role": "user", "content": question})

    try:
        for _ in range(5):                      # at most 5 steps per request
            response = client.chat(
                model=MODEL,
                messages=history,
                tools=TOOLS,
                options={"num_ctx": 8192},      # room for folder and file text
            )
            msg = response["message"]
            history.append(msg)

            if not msg.get("tool_calls"):       # no tool needed, so this is the answer
                return clean(msg["content"])

            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = call["function"]["arguments"] or {}
                text = str(args.get("text", ""))

                if name in TOOL_LIST:
                    function = TOOL_LIST[name][0]
                    try:
                        output = function(text)
                        result = str(output)[:3000] if output is not None else "Done."
                    except Exception as e:
                        result = f"Failed: {e}"
                else:
                    result = "Failed: unknown tool"

                log(f"AGENT | {name}('{text}') -> {result[:80]}")
                history.append({"role": "tool", "tool_name": name, "content": result})

    except Exception as e:
        log(f"BRAIN | FAILED: {e}")
        del history[start:]                     # forget the broken turn
        return "Sorry, my brain is not responding."

    return "Sorry, I couldn't finish that."