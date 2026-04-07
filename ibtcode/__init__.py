"""
Ibtcode - Cognitive Decision Layer
Production-grade decision engine for AI systems
"""

from ibtcode.system import IbtcodeSystem
from ibtcode.models import IbtcodeState, Decision, Emotion, Intent, Context
from ibtcode.encoder import encode
from ibtcode.decision import decide

__version__ = "1.0.0"
__author__ = "Ibtesham Akhtar"

__all__ = [
    "IbtcodeSystem",
    "IbtcodeState", 
    "Decision",
    "Emotion",
    "Intent",
    "Context",
    "encode",
    "decide",
]