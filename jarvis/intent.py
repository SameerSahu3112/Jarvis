"""Turn raw text into an Intent. Rule-based for now; an LLM can replace parse()
later, but its output must still be validated by permissions.py."""
import re
from dataclasses import dataclass, field


@dataclass
class Intent:
    skill: str
    args: dict = field(default_factory=dict)


def _clean(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"^(hey |ok |okay )?jarvis[,:]?\s*", "", text)  # drop wake word
    text = re.sub(r"[?!.]+$", "", text)
    return re.sub(r"\s+", " ", text)


def parse(text: str):
    """Return an Intent, or None if the command is not recognised."""
    t = _clean(text)

    m = re.match(r"^(?:open|launch|start)\s+(?:my |the )?(?P<app>.+)$", t)
    if m:
        return Intent("open_app", {"app": m.group("app")})

    if t in {"what time is it", "time", "tell me the time", "what's the time"}:
        return Intent("get_time")

    if t in {"what's the date", "what is the date", "date", "today's date", "what day is it"}:
        return Intent("get_date")

    if t in {"help", "what can you do", "list commands", "commands"}:
        return Intent("list_commands")

    return None
