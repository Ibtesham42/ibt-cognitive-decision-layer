import pytest
from ibtcode.encoder import encode
from ibtcode.models import Intent, Emotion, Context


def test_angry_payment():
    s = encode("My payment failed!! This is the worst!!")
    assert s.emotion == Emotion.ANGRY.value
    assert s.context == Context.PAYMENT_FAILED.value
    assert s.urgency >= 2


def test_happy():
    s = encode("Thanks for the help!")
    assert s.emotion == Emotion.HAPPY.value


def test_empty():
    s = encode("")
    assert s.intent == Intent.UNKNOWN.value


def test_question():
    s = encode("How do I reset my password?")
    assert s.intent == Intent.QUESTION.value
    assert s.context == Context.LOGIN_ERROR.value


def test_clarity_short():
    s = encode("help")
    assert s.clarity == "unclear"
