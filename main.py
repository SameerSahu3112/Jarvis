"""Run Jarvis in the terminal. Typed input first; swap in push-to-talk later."""
import sys

from jarvis.core import Jarvis


def main():
    dry_run = "--dry-run" in sys.argv
    jarvis = Jarvis(dry_run=dry_run)
    print("Jarvis ready. Type a command ('help' for ideas, 'quit' to exit).")
    while True:
        try:
            text = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in {"quit", "exit", "bye"}:
            break
        if not text:
            continue
        print("Jarvis >", jarvis.handle(text).message)


if __name__ == "__main__":
    main()
