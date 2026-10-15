# Jarvis (milestone 1)

A small, safe, explainable command pipeline:

    text -> intent.parse -> permissions.check -> skills.run -> response + log

## Run
    python main.py            # real mode (opens apps)
    python main.py --dry-run  # prints what it would do

## Test
    python -m unittest discover -s tests -v

## Commands (5)
open vscode / open browser / open calculator, what time is it, what's the date, help.
Anything else is rejected and logged.

## Safety rules
- Skills are ordinary Python functions; no free-form shell text.
- A skill must be in `permissions.ALLOWED`; apps must be in `config.APPS`.
- Logs store command, skill, result, error. No audio is stored.

## Limitations
Typed input only; rule-based intent; one OS command set per app (edit config.py).

## Next steps
1. Push-to-talk speech-to-text feeding `Jarvis.handle(text)`.
2. Spoken replies (text-to-speech).
3. Gesture input emitting the same commands (camera -> MediaPipe -> handle()).
4. Swap `intent.parse` for a local LLM, keeping `permissions.check` in front of every action.
