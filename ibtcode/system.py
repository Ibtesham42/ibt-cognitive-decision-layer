"""
Algorithm 6 – IbtcodeSystem
Orchestrates all components into a single clean interface.
"""

from __future__ import annotations
from loguru import logger
from ibtcode.models import IbtcodeState, Decision
from ibtcode.encoder     import encode
from ibtcode.state_engine import update_state
from ibtcode.reasoning   import reasoning
from ibtcode.decision    import decide
from ibtcode.response    import generate_response
from ibtcode.memory      import Memory


class IbtcodeSystem:
    """
    Production-ready cognitive engine.

    Usage:
        engine = IbtcodeSystem()
        response, state = engine.process("My payment failed!")
    """

    def __init__(self, memory_size: int | None = None) -> None:
        self.memory   = Memory(max_size=memory_size)
        self._prev    : IbtcodeState | None = None
        self._turn    : int = 0
        logger.info("IbtcodeSystem initialised.")

    # ── Main entry point ──────────────────────────────────────────────────────

    def process(self, text: str) -> tuple[str, IbtcodeState, Decision]:
        """
        Algorithm 6: IBTCODE_SYSTEM(text, S_prev, Memory)
        Returns (response_text, final_state, decision).
        """
        self._turn += 1
        logger.info(f"── Turn {self._turn} ──────────────────────────────────")

        # Step 1: Encode
        s_current = encode(text)

        # Step 2: State update
        s_t = update_state(s_current, self._prev, self.memory.to_list())

        # Step 3: Reasoning
        s_t = reasoning(s_t)

        # Step 4: Decision
        decision = decide(s_t)

        # Step 5: Response
        response = generate_response(s_t, decision)

        # Step 6: Persist
        self.memory.push(s_t)
        self._prev = s_t

        return response, s_t, decision

    # ── Utility ───────────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Reset conversation state (new session)."""
        self.memory.clear()
        self._prev = None
        self._turn = 0
        logger.info("Session reset.")

    @property
    def turn(self) -> int:
        return self._turn
