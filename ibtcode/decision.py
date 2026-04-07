"""
Algorithm 4 – Decision Engine
Maps state signals → (Strategy, Action).
"""

from __future__ import annotations
from loguru import logger
from ibtcode.models import IbtcodeState, Decision, Strategy, Action, Emotion
from ibtcode.config import cfg


def _p(state: IbtcodeState, emotion: Emotion) -> float:
    """
    Get probability for specific emotion from emotion vector.
    Fix: EmotionVector is a Pydantic model, not a dict.
    """
    try:
        emotion_str = emotion.value
        return getattr(state.emotion_vector, emotion_str, 0.0)
    except AttributeError:
        try:
            return state.emotion_vector.to_dict().get(emotion.value, 0.0)
        except:
            logger.warning(f"Could not get probability for {emotion}")
            return 0.0


def _get_effective_emotion(state: IbtcodeState) -> Emotion:
    """
    Get effective emotion considering sarcasm.
    If sarcasm, use hidden emotion; otherwise use detected emotion.
    Handles both Emotion enum and string types.
    """
    # Handle detected emotion
    detected_emotion = state.emotion
    if isinstance(detected_emotion, str):
        try:
            detected_emotion = Emotion(detected_emotion)
        except ValueError:
            detected_emotion = Emotion.NEUTRAL
    
    # Handle hidden emotion
    hidden_emotion = state.hidden_emotion
    if isinstance(hidden_emotion, str):
        try:
            hidden_emotion = Emotion(hidden_emotion)
        except ValueError:
            hidden_emotion = Emotion.NEUTRAL
    
    if state.sarcasm and hidden_emotion != Emotion.NEUTRAL:
        return hidden_emotion
    return detected_emotion


def _get_emotion_string(emotion: Emotion) -> str:
    """Safely get emotion string value from Emotion enum or string."""
    if hasattr(emotion, 'value'):
        return emotion.value
    return str(emotion)


def _is_high_priority(state: IbtcodeState) -> bool:
    """Check if state requires immediate attention"""
    return (
        state.escalate_flag or
        state.priority >= cfg.priority_threshold or
        state.risk >= cfg.risk_threshold or
        state.urgency >= cfg.urgency_threshold
    )


def _should_de_escalate(state: IbtcodeState, angry: float, frustrated: float, effective_emotion: Emotion) -> bool:
    """Determine if de-escalation is needed"""
    return (
        _is_high_priority(state) and
        (angry > cfg.angry_threshold or 
         frustrated > cfg.frustrated_threshold or 
         effective_emotion in (Emotion.ANGRY, Emotion.FRUSTRATED))
    )


def _should_clarify(state: IbtcodeState, confused: float, effective_emotion: Emotion) -> bool:
    """Determine if clarification is needed"""
    return (
        state.uncertainty > cfg.uncertainty_threshold or
        confused > cfg.confused_threshold or
        effective_emotion == Emotion.CONFUSED or
        state.clarity == "unclear"
    )


def _should_provide_support(state: IbtcodeState, frustrated: float) -> bool:
    """Determine if support is needed"""
    return (
        frustrated > cfg.frustrated_threshold or
        state.intent == "complaint" or
        state.contradiction_score > cfg.contradiction_threshold or
        state.risk >= cfg.risk_threshold
    )


def decide(state: IbtcodeState) -> Decision:
    """
    Main decision function - maps state to appropriate strategy and action.
    
    Args:
        state: Encoded IbtcodeState
        
    Returns:
        Decision with strategy and action
    """
    
    # Handle invalid state
    if not state:
        logger.warning("Received invalid state, returning default decision")
        return Decision(strategy=Strategy.NORMAL, action=Action.RESPOND)
    
    # Extract emotion probabilities
    angry = _p(state, Emotion.ANGRY)
    frustrated = _p(state, Emotion.FRUSTRATED)
    confused = _p(state, Emotion.CONFUSED)
    happy = _p(state, Emotion.HAPPY)
    sad = _p(state, Emotion.SAD)
    anxious = _p(state, Emotion.ANXIOUS)
    
    # Get effective emotion (considering sarcasm)
    effective_emotion = _get_effective_emotion(state)
    emotion_display = _get_emotion_string(effective_emotion)
    
    # Decision logic with priority order
    decision = None
    
    # 1. HIGHEST PRIORITY: De-escalation for angry/frustrated high-risk cases
    if _should_de_escalate(state, angry, frustrated, effective_emotion):
        if state.urgency >= 4:
            action = Action.FIX_FAST
        elif state.risk >= 4:
            action = Action.ESCALATE_TO_HUMAN
        else:
            action = Action.GIVE_SOLUTION
        
        decision = Decision(
            strategy=Strategy.DE_ESCALATE,
            action=action,
            confidence=min(0.9, max(angry, frustrated)),
            reasoning=f"High risk or priority with {emotion_display} emotion"
        )
    
    # 2. HIGH PRIORITY: Clarify when confused or uncertain
    elif _should_clarify(state, confused, effective_emotion):
        if state.clarity == "unclear":
            action = Action.ASK_QUESTION
        elif confused > 0.6:
            action = Action.STEP_BY_STEP
        else:
            action = Action.ASK_QUESTION
        
        decision = Decision(
            strategy=Strategy.CLARIFY,
            action=action,
            confidence=min(0.85, max(state.uncertainty, confused)),
            reasoning=f"Uncertainty: {state.uncertainty:.2f}, confused: {confused:.2f}"
        )
    
    # 3. MEDIUM PRIORITY: Support for frustrated/complaint cases
    elif _should_provide_support(state, frustrated):
        if state.intent == "complaint":
            action = Action.GIVE_SOLUTION
        elif state.contradiction_score > 0.6:
            action = Action.CLARIFY
        else:
            action = Action.GIVE_SOLUTION
        
        decision = Decision(
            strategy=Strategy.SUPPORT,
            action=action,
            confidence=min(0.8, frustrated),
            reasoning=f"Support needed: frustration={frustrated:.2f}, intent={state.intent}"
        )
    
    # 4. MEDIUM PRIORITY: Explain for questions
    elif state.intent == "question" or effective_emotion == Emotion.CONFUSED:
        decision = Decision(
            strategy=Strategy.EXPLAIN,
            action=Action.STEP_BY_STEP,
            confidence=0.75,
            reasoning="User asked a question or seems confused"
        )
    
    # 5. LOW PRIORITY: Empathize for sad/anxious users
    elif sad > cfg.sad_threshold or anxious > cfg.anxious_threshold:
        decision = Decision(
            strategy=Strategy.EMPATHIZE,
            action=Action.EMPATHIZE,
            confidence=max(sad, anxious),
            reasoning=f"User showing distress or {emotion_display} emotion"
        )
    
    # 6. LOW PRIORITY: Apologize for errors
    elif state.context in ["payment_failed", "technical_error"]:
        decision = Decision(
            strategy=Strategy.APOLOGIZE,
            action=Action.APOLOGIZE,
            confidence=0.7,
            reasoning=f"Context requires apology: {state.context}"
        )
    
    # 7. DEFAULT: Normal response
    else:
        if happy > 0.6:
            action = Action.RESPOND
        elif state.intent == "greeting":
            action = Action.RESPOND
        elif state.intent == "farewell":
            action = Action.RESPOND
        else:
            action = Action.RESPOND
        
        decision = Decision(
            strategy=Strategy.NORMAL,
            action=action,
            confidence=0.6,
            reasoning="Default response"
        )
    
    # Add emotion context to reasoning
    if decision and state.emotion_vector:
        dominant_emotion = state.emotion_vector.get_dominant()
        dominant_display = _get_emotion_string(dominant_emotion)
        if dominant_emotion != Emotion.NEUTRAL and dominant_display not in decision.reasoning:
            decision.reasoning += f", dominant emotion: {dominant_display}"
    
    # Log decision
    logger.debug(
        f"Decision made: {decision.strategy.value} -> {decision.action.value} "
        f"(conf: {decision.confidence:.2f}) - {decision.reasoning}"
    )
    
    return decision


def decide_batch(states: list[IbtcodeState]) -> list[Decision]:
    """
    Make decisions for multiple states.
    
    Args:
        states: List of encoded states
        
    Returns:
        List of decisions
    """
    return [decide(state) for state in states]


def validate_decision(decision: Decision) -> bool:
    """
    Validate if decision is valid and actionable.
    
    Args:
        decision: Decision to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not decision:
        return False
    
    if not decision.strategy or not decision.action:
        return False
    
    if decision.confidence < 0:
        return False
    
    invalid_combinations = [
        (Strategy.DE_ESCALATE, Action.RESPOND),
        (Strategy.CLARIFY, Action.ESCALATE_TO_HUMAN),
    ]
    
    if (decision.strategy, decision.action) in invalid_combinations:
        logger.warning(f"Invalid decision combination: {decision.strategy} -> {decision.action}")
        return False
    
    return True