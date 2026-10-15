"""Gatekeeper. Every skill must be listed here before it can run."""

ALLOWED = {"open_app", "get_time", "get_date", "list_commands"}

# Skills that must ask "are you sure?" first. Empty for now; add skills like
# send_message or delete_file here BEFORE you write them.
NEEDS_CONFIRMATION: set = set()


def check(skill: str) -> str:
    """Return 'allow', 'confirm' or 'deny'."""
    if skill not in ALLOWED:
        return "deny"
    if skill in NEEDS_CONFIRMATION:
        return "confirm"
    return "allow"
