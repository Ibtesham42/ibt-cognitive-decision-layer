"""
Algorithm 2 – State Update Engine
Maintains dynamic memory + smooths signals across turns.
"""

from __future__ import annotations
from loguru import logger
from ibtcode.models import IbtcodeState
from ibtcode.config import cfg


def update_state(
    current: IbtcodeState,
    previous: IbtcodeState | None,
    memory: list[IbtcodeState],
) -> IbtcodeState:
    """
    Algorithm 2: UPDATE_STATE(S_current, S_prev, Memory) → S_t
    """
    if previous is None:
        logger.debug("First turn — no state smoothing applied.")
        return current

    a = cfg.alpha_emotion

    # Emotion level smoothing (exponential moving average)
    smoothed_level = int(a * current.emotion_level + (1 - a) * previous.emotion_level)

    # Trust averaging (conservative update)
    new_trust = round((current.trust + previous.trust) / 2, 4)

    # Context persistence: carry forward if current is unknown
    resolved_context = (
        current.context if current.context != "unknown"
        else previous.context
    )

    # Contradiction detection
    contradiction = _detect_contradiction(current, memory)

    updated = current.model_copy(update={
        "emotion_level"      : smoothed_level,
        "trust"              : new_trust,
        "context"            : resolved_context,
        "contradiction_score": contradiction,
    })

    logger.debug(
        f"StateUpdate: EL {current.emotion_level}→{smoothed_level}  "
        f"T {previous.trust:.2f}→{new_trust:.2f}  "
        f"K={contradiction:.2f}"
    )
    return updated


def _detect_contradiction(
    current: IbtcodeState,
    memory: list[IbtcodeState],
) -> float:
    """
    Returns a contradiction score in [0, 1].
    Checks for rapid context switches and emotion reversals.
    """
    if not memory:
        return 0.0

    last = memory[-1]
    score = 0.0

    # Context flip
    if last.context != current.context and last.context != "unknown":
        score += 0.4

    # Emotion reversal (happy → angry etc.)
    _positive = {"happy", "neutral"}
    _negative = {"angry", "frustrated", "confused"}
    if (last.emotion in _positive and current.emotion in _negative) or        (last.emotion in _negative and current.emotion in _positive):
        score += 0.3

    # Rapid urgency spike
    if current.urgency - last.urgency >= 2:
        score += 0.3

    return round(min(1.0, score), 4)
