"""
Algorithm 5 – Response Generator
Converts Decision + State → natural language response.
"""

from __future__ import annotations
from loguru import logger
from ibtcode.models import IbtcodeState, Decision, Strategy, Context


# ── Response templates ────────────────────────────────────────────────────────

_TEMPLATES: dict[Strategy, str] = {
    Strategy.DE_ESCALATE: (
        "I sincerely apologize for the inconvenience this has caused. "
        "This is being treated as high priority — I will resolve it immediately. "
        "Could you confirm the details so I can act right away?"
    ),
    Strategy.CLARIFY: (
        "I want to make sure I help you correctly. "
        "Could you please provide a bit more detail about your issue?"
    ),
    Strategy.EXPLAIN: (
        "No worries — let me walk you through this step by step. "
        "I'll make it as clear as possible."
    ),
    Strategy.SUPPORT: (
        "I understand your frustration, and I'm here to help. "
        "Let me look into this and give you the best resolution."
    ),
    Strategy.NORMAL: (
        "Thank you for reaching out. "
        "Here is the information you need:"
    ),
}

_CONTEXT_SUFFIX: dict[str, str] = {
    Context.PAYMENT_FAILED.value:    " I'll check your payment status and ensure a resolution.",
    Context.LOGIN_ERROR.value:       " I'll guide you through account access recovery.",
    Context.PERFORMANCE_ISSUE.value: " I'll help diagnose and fix the performance issue.",
    Context.GENERAL.value:           "",
    Context.UNKNOWN.value:           "",
}


def generate_response(state: IbtcodeState, decision: Decision) -> str:
    """
    Algorithm 5: RESPONSE_GENERATE(S_t, D) → R_output
    """
    base   = _TEMPLATES.get(decision.strategy, _TEMPLATES[Strategy.NORMAL])
    suffix = _CONTEXT_SUFFIX.get(state.context, "")

    # Tone modifier for escalation
    if state.escalate_flag:
        base = "\u26a0\ufe0f  This has been escalated to our priority team. " + base

    response = (base + suffix).strip()
    logger.debug(f"Response generated ({decision.strategy})")
    return response
