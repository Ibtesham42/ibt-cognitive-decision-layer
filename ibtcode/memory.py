"""
Conversation memory — sliding window with search utilities.
"""

from __future__ import annotations
from collections import deque
from loguru import logger
from ibtcode.models import IbtcodeState
from ibtcode.config import cfg


class Memory:
    """
    Fixed-size sliding window over IbtcodeState history.
    Provides utility methods used by reasoning and state engine.
    """

    def __init__(self, max_size: int | None = None) -> None:
        self._max = max_size or cfg.memory_size
        self._store: deque[IbtcodeState] = deque(maxlen=self._max)

    # ── Core API ──────────────────────────────────────────────────────────────

    def push(self, state: IbtcodeState) -> None:
        self._store.append(state)
        logger.debug(f"Memory: {len(self._store)}/{self._max} turns stored.")

    def recent(self, n: int = 5) -> list[IbtcodeState]:
        """Return the n most recent states (oldest first)."""
        items = list(self._store)
        return items[-n:]

    def last(self) -> IbtcodeState | None:
        return self._store[-1] if self._store else None

    def clear(self) -> None:
        self._store.clear()
        logger.info("Memory cleared.")

    def __len__(self) -> int:
        return len(self._store)

    # ── Analytics helpers ─────────────────────────────────────────────────────

    def dominant_emotion(self) -> str | None:
        """Most frequent emotion in memory window."""
        if not self._store:
            return None
        counts: dict[str, int] = {}
        for s in self._store:
            counts[s.emotion] = counts.get(s.emotion, 0) + 1
        return max(counts, key=counts.get)  # type: ignore

    def average_urgency(self) -> float:
        if not self._store:
            return 1.0
        return sum(s.urgency for s in self._store) / len(self._store)

    def to_list(self) -> list[IbtcodeState]:
        return list(self._store)
