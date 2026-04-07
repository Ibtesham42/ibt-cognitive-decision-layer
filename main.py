#!/usr/bin/env python3
"""
Ibtcode – Interactive CLI
Run:  python main.py
Quit: type 'exit' or 'quit'
"""

import sys
from pathlib import Path

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel   import Panel
    from rich.table   import Table
    from rich import box as rbox
    RICH = True
except ImportError:
    RICH = False

from ibtcode.system import IbtcodeSystem
from ibtcode.logger import setup_logging


def _print_state(state, decision, console=None) -> None:
    """Pretty-print state + decision."""
    if RICH and console:
        t = Table(box=rbox.SIMPLE, show_header=False, padding=(0,1))
        t.add_column("Key",   style="bold cyan",  width=22)
        t.add_column("Value", style="white")
        rows = [
            ("Intent",        state.intent),
            ("Emotion",       f"{state.emotion}  (level {state.emotion_level})"),
            ("Context",       state.context),
            ("Urgency",       str(state.urgency)),
            ("Risk",          str(state.risk)),
            ("Uncertainty",   f"{state.uncertainty:.2f}"),
            ("Priority",      f"{state.priority:.2f}"),
            ("Contradiction", f"{state.contradiction_score:.2f}"),
            ("Escalate",      "YES \u26a0\ufe0f" if state.escalate_flag else "no"),
            ("Decision",      str(decision)),
        ]
        for k, v in rows:
            t.add_row(k, v)
        console.print(t)
    else:
        print(f"  intent={state.intent}  emotion={state.emotion}({state.emotion_level})"
              f"  ctx={state.context}  U={state.urgency}  UQ={state.uncertainty:.2f}"
              f"  priority={state.priority:.2f}  decision={decision}")


def main():
    setup_logging()
    engine  = IbtcodeSystem()
    console = Console() if RICH else None

    banner = (
        "[bold cyan]Ibtcode Cognitive Engine[/bold cyan]  v1.0\n"
        "[dim]Type your message · 'reset' to clear session · 'exit' to quit[/dim]"
    )
    if RICH and console:
        console.print(Panel(banner, border_style="cyan"))
    else:
        print("\n=== Ibtcode Cognitive Engine v1.0 ===")
        print("Type your message | 'reset' | 'exit'\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not text:
            continue

        if text.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if text.lower() == "reset":
            engine.reset()
            print("[Session reset]")
            continue

        response, state, decision = engine.process(text)

        if RICH and console:
            console.print(f"\n[bold green]AI:[/bold green] {response}\n")
            _print_state(state, decision, console)
            console.rule(style="dim")
        else:
            print(f"\nAI: {response}\n")
            _print_state(state, decision)
            print("-" * 50)


if __name__ == "__main__":
    main()
