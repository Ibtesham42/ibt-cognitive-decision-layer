import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from ibtcode.system import IbtcodeSystem
from ibtcode.models import Strategy


def test_single_turn():
    engine = IbtcodeSystem()
    response, state, decision = engine.process("My payment failed!!")
    assert isinstance(response, str)
    assert len(response) > 0
    assert state.context == "payment_failed"


def test_multi_turn_memory():
    engine = IbtcodeSystem()
    engine.process("My login is broken")
    engine.process("Still not working!!")
    assert engine.turn == 2
    assert len(engine.memory) == 2


def test_reset():
    engine = IbtcodeSystem()
    engine.process("test")
    engine.reset()
    assert engine.turn == 0
    assert len(engine.memory) == 0


def test_clarification_boundary():
    # Very short input should produce a high uncertainty state.
    engine = IbtcodeSystem()
    _, state, _ = engine.process("?")
    # UQ >= 0.6 for a single-char unclear message
    assert state.uncertainty >= 0.6


def test_angry_escalation():
    # High-urgency angry message must escalate.
    engine = IbtcodeSystem()
    _, state, decision = engine.process("My payment failed!! Fix it now immediately!!")
    assert state.escalate_flag is True
    assert decision.strategy == "de_escalate"


def test_decision_values_valid():
    # Every decision strategy must be a valid Strategy enum value.
    engine = IbtcodeSystem()
    valid = {s.value for s in Strategy}
    for msg in ["hello", "?", "payment issue!!", "Thanks so much!"]:
        _, _, d = engine.process(msg)
        assert d.strategy in valid
