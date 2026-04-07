"""Pydantic models – single source of truth for all data structures."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class Intent(str, Enum):
    """User intent classification"""
    QUESTION = "question"
    COMMAND = "command"
    COMPLAINT = "complaint"
    HELP = "help"
    GREETING = "greeting"
    FAREWELL = "farewell"
    GRATITUDE = "gratitude"
    FEEDBACK = "feedback"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    REQUEST = "request"
    UNKNOWN = "unknown"


class Emotion(str, Enum):
    """User emotion classification"""
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    HAPPY = "happy"
    CONFUSED = "confused"
    SAD = "sad"
    ANXIOUS = "anxious"
    EXCITED = "excited"
    DISAPPOINTED = "disappointed"
    NEUTRAL = "neutral"


class Context(str, Enum):
    """Conversation context classification"""
    PAYMENT_FAILED = "payment_failed"
    LOGIN_ERROR = "login_error"
    PERFORMANCE_ISSUE = "performance_issue"
    BILLING = "billing"
    TECHNICAL_ERROR = "technical_error"
    FEATURE_REQUEST = "feature_request"
    PRIVACY_CONCERN = "privacy_concern"
    ONBOARDING = "onboarding"
    ACCOUNT_MANAGEMENT = "account_management"
    ORDER_STATUS = "order_status"
    DELIVERY_ISSUE = "delivery_issue"
    PRODUCT_INQUIRY = "product_inquiry"
    GENERAL = "general"
    UNKNOWN = "unknown"


class Strategy(str, Enum):
    """Response strategy classification"""
    DE_ESCALATE = "de_escalate"
    CLARIFY = "clarify"
    EXPLAIN = "explain"
    SUPPORT = "support"
    APOLOGIZE = "apologize"
    EMPATHIZE = "empathize"
    ESCALATE = "escalate"
    NORMAL = "normal"


class Action(str, Enum):
    """Action to be taken"""
    ASK_QUESTION = "ask_question"
    FIX_FAST = "fix_fast"
    STEP_BY_STEP = "step_by_step_guidance"
    GIVE_SOLUTION = "give_solution"
    APOLOGIZE = "apologize"
    EMPATHIZE = "empathize"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    PROVIDE_LINK = "provide_link"
    SCHEDULE_CALLBACK = "schedule_callback"
    SEND_EMAIL = "send_email"
    RESPOND = "respond"


class ConfidenceScore(BaseModel):
    """Confidence score for predictions"""
    value: float = Field(ge=0.0, le=1.0)
    threshold: float = 0.6
    is_confident: bool = False
    
    def __post_init__(self):
        self.is_confident = self.value >= self.threshold


class EmotionVector(BaseModel):
    """Emotion vector with scores for all emotions"""
    angry: float = 0.0
    frustrated: float = 0.0
    happy: float = 0.0
    confused: float = 0.0
    sad: float = 0.0
    anxious: float = 0.0
    excited: float = 0.0
    disappointed: float = 0.0
    neutral: float = 0.0
    
    def get_dominant(self) -> Emotion:
        """Get dominant emotion"""
        emotions = {
            Emotion.ANGRY: self.angry,
            Emotion.FRUSTRATED: self.frustrated,
            Emotion.HAPPY: self.happy,
            Emotion.CONFUSED: self.confused,
            Emotion.SAD: self.sad,
            Emotion.ANXIOUS: self.anxious,
            Emotion.EXCITED: self.excited,
            Emotion.DISAPPOINTED: self.disappointed,
            Emotion.NEUTRAL: self.neutral
        }
        return max(emotions, key=emotions.get)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return self.model_dump()


class Metadata(BaseModel):
    """Metadata for the encoded state"""
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: float = 0.0
    version: str = "1.0.0"
    source: str = "encoder"
    language: str = "en"
    tokens: List[str] = Field(default_factory=list)
    char_count: int = 0
    word_count: int = 0


class Decision(BaseModel):
    """Decision output from decoder"""
    strategy: Strategy
    action: Action
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    reasoning: str = ""
    alternatives: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        return f"[{self.strategy.value} → {self.action.value}] (conf: {self.confidence:.2f})"


class IbtcodeState(BaseModel):
    """Main state object - single source of truth"""
    
    # Core fields
    intent: Intent = Intent.UNKNOWN
    emotion: Emotion = Emotion.NEUTRAL
    emotion_level: int = Field(default=1, ge=1, le=5)
    context: Context = Context.UNKNOWN
    
    # Confidence and certainty
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    uncertainty: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Risk and priority
    risk: int = Field(default=1, ge=1, le=5)
    priority: float = Field(default=0.0, ge=0.0, le=1.0)
    escalate_flag: bool = False
    
    # Communication quality
    clarity: str = "clear"
    urgency: int = Field(default=1, ge=1, le=5)
    complexity: int = Field(default=1, ge=1, le=5)
    
    # Trust and expectation
    trust: float = Field(default=0.5, ge=0.0, le=1.0)
    expectation: str = "unknown"
    
    # Advanced features
    emotion_vector: EmotionVector = Field(default_factory=EmotionVector)
    sarcasm: bool = False
    sarcasm_confidence: float = 0.0
    hidden_emotion: Emotion = Emotion.NEUTRAL
    
    # Contradictions and conflicts
    contradiction_score: float = Field(default=0.0, ge=0.0, le=1.0)
    conflict_type: Optional[str] = None
    
    # Input data
    raw_text: str = ""
    normalized_text: str = ""
    
    # Metadata
    metadata: Metadata = Field(default_factory=Metadata)
    
    # Additional context
    entities: Dict[str, Any] = Field(default_factory=dict)
    keywords: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True
        validate_assignment = True
    
    @validator('emotion_level')
    def validate_emotion_level(cls, v):
        if not 1 <= v <= 5:
            raise ValueError(f'emotion_level must be between 1 and 5, got {v}')
        return v
    
    @validator('urgency')
    def validate_urgency(cls, v):
        if not 1 <= v <= 5:
            raise ValueError(f'urgency must be between 1 and 5, got {v}')
        return v
    
    @validator('risk')
    def validate_risk(cls, v):
        if not 1 <= v <= 5:
            raise ValueError(f'risk must be between 1 and 5, got {v}')
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        if not 1 <= v <= 5:
            raise ValueError(f'complexity must be between 1 and 5, got {v}')
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self.model_dump(exclude={'metadata': {'tokens'}})
    
    def is_high_risk(self) -> bool:
        """Check if state is high risk"""
        return self.risk >= 4 or self.escalate_flag
    
    def requires_escalation(self) -> bool:
        """Check if state requires escalation"""
        return (self.risk >= 4 or 
                self.emotion in [Emotion.ANGRY, Emotion.FRUSTRATED] or
                self.urgency >= 4 or
                self.escalate_flag)
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        return (f"Intent: {self.intent.value}, Emotion: {self.emotion.value} (level {self.emotion_level}), "
                f"Context: {self.context.value}, Risk: {self.risk}, Urgency: {self.urgency}")
    
    def update_confidence(self, new_confidence: float):
        """Update confidence and related fields"""
        self.confidence = max(0.0, min(1.0, new_confidence))
        self.uncertainty = 1.0 - self.confidence


class ConversationTurn(BaseModel):
    """Single turn in conversation history"""
    state: IbtcodeState
    decision: Decision
    timestamp: datetime = Field(default_factory=datetime.now)
    response_time_ms: float = 0.0


class ConversationHistory(BaseModel):
    """Conversation history manager"""
    turns: List[ConversationTurn] = Field(default_factory=list)
    max_turns: int = 50
    
    def add_turn(self, state: IbtcodeState, decision: Decision):
        """Add a turn to history"""
        turn = ConversationTurn(state=state, decision=decision)
        self.turns.append(turn)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
    
    def get_last_turn(self) -> Optional[ConversationTurn]:
        """Get last turn"""
        return self.turns[-1] if self.turns else None
    
    def get_recent_context(self, n: int = 3) -> List[ConversationTurn]:
        """Get recent n turns"""
        return self.turns[-n:] if self.turns else []
    
    def get_emotion_trend(self) -> List[Emotion]:
        """Get emotion trend from recent turns"""
        return [turn.state.emotion for turn in self.turns[-5:]]
    
    def clear(self):
        """Clear history"""
        self.turns.clear()