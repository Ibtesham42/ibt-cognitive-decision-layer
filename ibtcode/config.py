"""Centralised config – reads from env / .env file."""

import os
from dataclasses import dataclass, field
from typing import Optional


def _str(key: str, default: str) -> str:
    """Get string from environment"""
    return os.getenv(key, default)


def _float(key: str, default: float) -> float:
    """Get float from environment"""
    try:
        return float(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def _int(key: str, default: int) -> int:
    """Get integer from environment"""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def _bool(key: str, default: bool) -> bool:
    """Get boolean from environment"""
    val = os.getenv(key, str(default)).lower()
    return val in ('true', '1', 'yes', 'on')


@dataclass(frozen=True)
class Config:
    """Configuration settings for Ibtcode system"""
    
    # ========== Logging ==========
    log_level: str = _str("LOG_LEVEL", "INFO")
    log_file: str = _str("LOG_FILE", "ibtcode.log")
    log_rotation: str = _str("LOG_ROTATION", "500 MB")
    log_retention: str = _str("LOG_RETENTION", "10 days")
    
    # ========== System Settings ==========
    memory_size: int = _int("MEMORY_SIZE", 10)
    max_history: int = _int("MAX_HISTORY", 50)
    processing_timeout: float = _float("PROCESSING_TIMEOUT", 5.0)
    enable_caching: bool = _bool("ENABLE_CACHING", True)
    
    # ========== Emotion Thresholds ==========
    angry_threshold: float = _float("ANGRY_THRESHOLD", 0.4)
    frustrated_threshold: float = _float("FRUSTRATED_THRESHOLD", 0.4)
    confused_threshold: float = _float("CONFUSED_THRESHOLD", 0.4)
    happy_threshold: float = _float("HAPPY_THRESHOLD", 0.6)
    sad_threshold: float = _float("SAD_THRESHOLD", 0.4)
    anxious_threshold: float = _float("ANXIOUS_THRESHOLD", 0.4)
    excited_threshold: float = _float("EXCITED_THRESHOLD", 0.6)
    disappointed_threshold: float = _float("DISAPPOINTED_THRESHOLD", 0.4)
    neutral_threshold: float = _float("NEUTRAL_THRESHOLD", 0.5)
    
    # ========== Priority Weights ==========
    alpha_emotion: float = _float("ALPHA_EMOTION", 0.7)
    priority_w_urgency: float = _float("PRIORITY_W_URGENCY", 0.4)
    priority_w_risk: float = _float("PRIORITY_W_RISK", 0.3)
    priority_w_emotion: float = _float("PRIORITY_W_EMOTION", 0.3)
    priority_w_intent: float = _float("PRIORITY_W_INTENT", 0.2)
    
    # ========== Thresholds ==========
    uncertainty_threshold: float = _float("UNCERTAINTY_THRESHOLD", 0.5)
    priority_threshold: float = _float("PRIORITY_THRESHOLD", 0.6)
    risk_threshold: int = _int("RISK_THRESHOLD", 3)
    urgency_threshold: int = _int("URGENCY_THRESHOLD", 3)
    contradiction_threshold: float = _float("CONTRADICTION_THRESHOLD", 0.4)
    confidence_threshold: float = _float("CONFIDENCE_THRESHOLD", 0.6)
    
    # ========== Sarcasm Detection ==========
    sarcasm_threshold: float = _float("SARCASM_THRESHOLD", 0.6)
    enable_sarcasm_detection: bool = _bool("ENABLE_SARCASM", True)
    
    # ========== Risk Levels ==========
    high_risk_threshold: int = _int("HIGH_RISK_THRESHOLD", 4)
    medium_risk_threshold: int = _int("MEDIUM_RISK_THRESHOLD", 3)
    low_risk_threshold: int = _int("LOW_RISK_THRESHOLD", 2)
    
    # ========== Urgency Levels ==========
    high_urgency_threshold: int = _int("HIGH_URGENCY_THRESHOLD", 4)
    medium_urgency_threshold: int = _int("MEDIUM_URGENCY_THRESHOLD", 3)
    
    # ========== Clarity Levels ==========
    clear_clarity_threshold: int = _int("CLEAR_CLARITY_THRESHOLD", 5)  # words
    partial_clarity_threshold: int = _int("PARTIAL_CLARITY_THRESHOLD", 3)  # words
    
    # ========== Complexity Levels ==========
    simple_complexity_threshold: int = _int("SIMPLE_COMPLEXITY_THRESHOLD", 5)  # words
    medium_complexity_threshold: int = _int("MEDIUM_COMPLEXITY_THRESHOLD", 10)
    complex_complexity_threshold: int = _int("COMPLEX_COMPLEXITY_THRESHOLD", 20)
    
    # ========== Escalation ==========
    auto_escalate_on_high_risk: bool = _bool("AUTO_ESCALATE_ON_HIGH_RISK", True)
    auto_escalate_on_angry: bool = _bool("AUTO_ESCALATE_ON_ANGRY", True)
    escalation_threshold: int = _int("ESCALATION_THRESHOLD", 3)
    
    # ========== Response Settings ==========
    max_response_length: int = _int("MAX_RESPONSE_LENGTH", 500)
    enable_emojis: bool = _bool("ENABLE_EMOJIS", True)
    response_language: str = _str("RESPONSE_LANGUAGE", "en")
    
    # ========== Performance ==========
    enable_metrics: bool = _bool("ENABLE_METRICS", True)
    metrics_port: int = _int("METRICS_PORT", 9090)
    
    # ========== Security ==========
    enable_rate_limiting: bool = _bool("ENABLE_RATE_LIMITING", True)
    rate_limit_per_minute: int = _int("RATE_LIMIT_PER_MINUTE", 60)
    
    # ========== Experimental Features ==========
    enable_experimental: bool = _bool("ENABLE_EXPERIMENTAL", False)
    
    def __post_init__(self):
        """Validate config after initialization"""
        # Validate thresholds are within ranges
        if not 0 <= self.uncertainty_threshold <= 1:
            raise ValueError(f"uncertainty_threshold must be 0-1, got {self.uncertainty_threshold}")
        
        if not 0 <= self.priority_threshold <= 1:
            raise ValueError(f"priority_threshold must be 0-1, got {self.priority_threshold}")
        
        if not 1 <= self.risk_threshold <= 5:
            raise ValueError(f"risk_threshold must be 1-5, got {self.risk_threshold}")
        
        if not 1 <= self.urgency_threshold <= 5:
            raise ValueError(f"urgency_threshold must be 1-5, got {self.urgency_threshold}")
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            key: getattr(self, key)
            for key in dir(self)
            if not key.startswith('_') and not callable(getattr(self, key))
        }
    
    def get_thresholds(self) -> dict:
        """Get all threshold values"""
        return {
            "angry": self.angry_threshold,
            "frustrated": self.frustrated_threshold,
            "confused": self.confused_threshold,
            "happy": self.happy_threshold,
            "sad": self.sad_threshold,
            "anxious": self.anxious_threshold,
            "excited": self.excited_threshold,
            "disappointed": self.disappointed_threshold,
            "neutral": self.neutral_threshold,
            "uncertainty": self.uncertainty_threshold,
            "priority": self.priority_threshold,
            "risk": self.risk_threshold,
            "urgency": self.urgency_threshold,
            "contradiction": self.contradiction_threshold,
            "confidence": self.confidence_threshold,
            "sarcasm": self.sarcasm_threshold,
        }
    
    def get_priority_weights(self) -> dict:
        """Get priority calculation weights"""
        return {
            "urgency": self.priority_w_urgency,
            "risk": self.priority_w_risk,
            "emotion": self.priority_w_emotion,
            "intent": self.priority_w_intent,
            "alpha_emotion": self.alpha_emotion,
        }
    
    def is_high_risk(self, risk_value: int) -> bool:
        """Check if risk value is considered high"""
        return risk_value >= self.high_risk_threshold
    
    def is_medium_risk(self, risk_value: int) -> bool:
        """Check if risk value is considered medium"""
        return self.medium_risk_threshold <= risk_value < self.high_risk_threshold
    
    def is_high_urgency(self, urgency_value: int) -> bool:
        """Check if urgency value is considered high"""
        return urgency_value >= self.high_urgency_threshold
    
    def get_clarity_level(self, word_count: int) -> str:
        """Determine clarity level based on word count"""
        if word_count >= self.clear_clarity_threshold:
            return "clear"
        elif word_count >= self.partial_clarity_threshold:
            return "partial"
        return "unclear"
    
    def get_complexity_level(self, word_count: int) -> int:
        """Determine complexity level (1-5) based on word count"""
        if word_count < self.simple_complexity_threshold:
            return 1
        elif word_count < self.medium_complexity_threshold:
            return 2
        elif word_count < self.complex_complexity_threshold:
            return 3
        elif word_count < self.complex_complexity_threshold * 1.5:
            return 4
        return 5


# Create .env file template
def create_env_template():
    """Create a .env file template with default values"""
    env_template = """# Ibtcode Configuration File

# Logging
LOG_LEVEL=INFO
LOG_FILE=ibtcode.log
LOG_ROTATION=500 MB
LOG_RETENTION=10 days

# System Settings
MEMORY_SIZE=10
MAX_HISTORY=50
PROCESSING_TIMEOUT=5.0
ENABLE_CACHING=true

# Emotion Thresholds
ANGRY_THRESHOLD=0.4
FRUSTRATED_THRESHOLD=0.4
CONFUSED_THRESHOLD=0.4
HAPPY_THRESHOLD=0.6
SAD_THRESHOLD=0.4
ANXIOUS_THRESHOLD=0.4
EXCITED_THRESHOLD=0.6
DISAPPOINTED_THRESHOLD=0.4
NEUTRAL_THRESHOLD=0.5

# Priority Weights
ALPHA_EMOTION=0.7
PRIORITY_W_URGENCY=0.4
PRIORITY_W_RISK=0.3
PRIORITY_W_EMOTION=0.3
PRIORITY_W_INTENT=0.2

# Thresholds
UNCERTAINTY_THRESHOLD=0.5
PRIORITY_THRESHOLD=0.6
RISK_THRESHOLD=3
URGENCY_THRESHOLD=3
CONTRADICTION_THRESHOLD=0.4
CONFIDENCE_THRESHOLD=0.6

# Sarcasm Detection
SARCASM_THRESHOLD=0.6
ENABLE_SARCASM=true

# Risk Levels
HIGH_RISK_THRESHOLD=4
MEDIUM_RISK_THRESHOLD=3
LOW_RISK_THRESHOLD=2

# Urgency Levels
HIGH_URGENCY_THRESHOLD=4
MEDIUM_URGENCY_THRESHOLD=3

# Clarity Levels
CLEAR_CLARITY_THRESHOLD=5
PARTIAL_CLARITY_THRESHOLD=3

# Complexity Levels
SIMPLE_COMPLEXITY_THRESHOLD=5
MEDIUM_COMPLEXITY_THRESHOLD=10
COMPLEX_COMPLEXITY_THRESHOLD=20

# Escalation
AUTO_ESCALATE_ON_HIGH_RISK=true
AUTO_ESCALATE_ON_ANGRY=true
ESCALATION_THRESHOLD=3

# Response Settings
MAX_RESPONSE_LENGTH=500
ENABLE_EMOJIS=true
RESPONSE_LANGUAGE=en

# Performance
ENABLE_METRICS=true
METRICS_PORT=9090

# Security
ENABLE_RATE_LIMITING=true
RATE_LIMIT_PER_MINUTE=60

# Experimental
ENABLE_EXPERIMENTAL=false
"""
    with open(".env.template", "w") as f:
        f.write(env_template)
    print("Created .env.template file")


# Singleton instance
cfg = Config() 