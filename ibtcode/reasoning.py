"""
Algorithm 3 – Reasoning Engine
Computes priority, adjusts uncertainty, sets escalation flags.
"""

from __future__ import annotations
from loguru import logger
from ibtcode.models import IbtcodeState
from ibtcode.config import cfg


def reasoning(state: IbtcodeState) -> IbtcodeState:
    """
    Algorithm 3: REASONING(S_t) → enhanced S_t
    """
    # Priority score
    wu = cfg.priority_w_urgency
    wr = cfg.priority_w_risk
    we = cfg.priority_w_emotion
    priority = wu * state.urgency + wr * state.risk + we * state.emotion_level

    # Uncertainty boost when contradiction is high
    uq = state.uncertainty
    if state.contradiction_score > 0.5:
        uq = min(1.0, uq + 0.3)
        logger.debug(f"High contradiction ({state.contradiction_score:.2f}) → UQ boosted to {uq:.2f}")

    # Escalation flag
    escalate = priority >= cfg.priority_threshold

    updated = state.model_copy(update={
        "priority"    : round(priority, 4),
        "uncertainty" : round(uq, 4),
        "escalate_flag": escalate,
    })

    logger.debug(
        f"Reasoning: priority={priority:.2f}  UQ={uq:.2f}  escalate={escalate}"
    )
    return updated
