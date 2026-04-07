"""
Algorithm 1 – Ibtcode Encoder
Converts raw text → structured IbtcodeState.
"""

from __future__ import annotations
import re
import time
from typing import Dict, List, Tuple, Optional
from loguru import logger
from ibtcode.models import (
    IbtcodeState, Intent, Emotion, Context, EmotionVector, Metadata
)


def _normalize(text: str) -> str:
    """Enhanced normalization with production-level text cleaning"""
    original = text
    text = text.lower()

    # Common misspellings and slang
    replacements = {
        # Profanity normalization
        "fuk": "fuck", "fck": "fuck", "fucc": "fuck", "fukin": "fucking",
        "bich": "bitch", "b*tch": "bitch", "biatch": "bitch",
        "idi0t": "idiot", "id10t": "idiot",
        "stupd": "stupid", "stoopid": "stupid", "dum": "dumb",
        
        # Common abbreviations
        "wtf": "what the fuck", "omg": "oh my god", "lmao": "laughing",
        "pls": "please", "plz": "please", "thx": "thanks",
        "u": "you", "ur": "your", "u r": "you are",
        "yaar": "yar", "bro": "brother",
        
        # Indian English specific
        "kya": "what", "kaise": "how", "kyun": "why",
        "nahi": "no", "haan": "yes", "accha": "okay",
        
        # Text shortcuts
        "gr8": "great", "2day": "today", "2moro": "tomorrow",
        "b4": "before", "bcuz": "because", "cuz": "because",
        "ppl": "people", "msg": "message"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Remove excessive repeated characters
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    # Handle emojis
    emoji_map = {
        ":)": "happy", ":(": "sad", ":D": "happy", ";)": "wink",
        ":'(": "crying", ":/": "confused", ":|": "neutral",
        "<3": "love", "😂": "laughing", "😢": "sad", "😡": "angry"
    }
    for k, v in emoji_map.items():
        text = text.replace(k, f" {v} ")
    
    # Remove extra punctuation
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    
    logger.debug(f"Normalized: '{original}' → '{text}'")
    return text


# Intent rules with confidence scores (using only intents from models.py)
_INTENT_RULES: List[Tuple[List[str], Intent, float]] = [
    # Greeting
    (["hi", "hello", "hey", "namaste", "good morning", "good afternoon", "good evening"], Intent.GREETING, 0.95),
    
    # Farewell
    (["bye", "goodbye", "see you", "take care", "cya"], Intent.FAREWELL, 0.95),
    
    # Gratitude
    (["thanks", "thank you", "appreciate", "grateful", "thx", "ty", "much appreciated"], Intent.GRATITUDE, 0.9),
    
    # Question patterns
    (["why", "how", "what", "kya", "kaise", "when", "where", "who", 
      "explain", "tell me", "can you", "could you", "would you"], Intent.QUESTION, 0.9),
    
    # Command patterns
    (["fix", "solve", "repair", "resolve", "do it", "do this", "make it work", 
      "correct", "change", "update", "modify", "cancel", "stop", "undo", "remove", "delete"], Intent.COMMAND, 0.85),
    
    # Complaint patterns
    (["not working", "issue", "problem", "error", "fail", "broke", "delay", 
      "stuck", "glitch", "bug", "crash", "hang", "freeze"], Intent.COMPLAINT, 0.9),
    
    # Help patterns
    (["help", "assist", "support", "guide", "assistance", "help me", 
      "can you help", "need help"], Intent.HELP, 0.95),
    
    # Feedback
    (["feedback", "suggestion", "improvement", "review"], Intent.FEEDBACK, 0.85),
    
    # Clarification
    (["clarify", "elaborate", "explain more", "what do you mean"], Intent.CLARIFICATION, 0.85),
    
    # Confirmation
    (["yes", "no", "correct", "right", "wrong", "confirm"], Intent.CONFIRMATION, 0.8),
    
    # Request
    (["suggest", "recommend", "advice", "option", "alternative", 
      "what should i", "how to"], Intent.REQUEST, 0.85),
]

# Context rules
_CONTEXT_RULES: List[Tuple[List[str], Context, float]] = [
    # Payment/Financial
    (["payment", "charge", "refund", "invoice", "billing", "transaction", 
      "money", "paid", "credit card", "debit", "wallet"], Context.PAYMENT_FAILED, 0.9),
    
    # Login/Access
    (["login", "password", "sign in", "access", "account", "credential", 
      "username", "otp", "verification", "2fa"], Context.LOGIN_ERROR, 0.9),
    
    # Performance
    (["slow", "lag", "performance", "speed", "timeout", "crash", "freeze", 
      "hang", "unresponsive", "loading"], Context.PERFORMANCE_ISSUE, 0.9),
    
    # Billing
    (["subscription", "plan", "pricing", "cost", "price", "monthly", "annual"], Context.BILLING, 0.85),
    
    # Technical Error
    (["bug", "glitch", "error", "exception", "crash", "stack trace", 
      "debug", "technical"], Context.TECHNICAL_ERROR, 0.9),
    
    # Feature Request
    (["feature", "functionality", "capability", "does it do", "can it", 
      "add feature", "new feature"], Context.FEATURE_REQUEST, 0.85),
    
    # Privacy
    (["privacy", "data", "security", "personal info", "gdpr", "breach", 
      "hack", "compromised"], Context.PRIVACY_CONCERN, 0.9),
    
    # Onboarding
    (["sign up", "register", "create account", "welcome", "getting started"], Context.ONBOARDING, 0.85),
    
    # Account Management
    (["update profile", "change email", "reset password", "delete account"], Context.ACCOUNT_MANAGEMENT, 0.85),
    
    # Order Status
    (["order status", "track order", "where is my order"], Context.ORDER_STATUS, 0.9),
    
    # Delivery Issue
    (["delivery", "shipping", "courier", "package not received", "late delivery"], Context.DELIVERY_ISSUE, 0.9),
    
    # Product Inquiry
    (["product details", "specifications", "features", "compatible"], Context.PRODUCT_INQUIRY, 0.85),
]

# Urgency indicators
_URGENCY_HIGH = [
    "now", "immediately", "urgent", "asap", "right away", "emergency",
    "critical", "fast", "right now", "quick", "as soon as possible",
    "priority", "high priority", "blocker"
]

_URGENCY_MEDIUM = [
    "soon", "quickly", "today", "within hour", "please hurry"
]

# Emotion detection rules
_EMOTION_RULES: List[Tuple[List[str], Emotion, int, float]] = [
    # Anger
    (["fuck", "idiot", "stupid", "bitch", "damn", "hell", "bloody", 
      "hate", "worst", "terrible", "awful"], Emotion.ANGRY, 5, 0.9),
    (["shit", "crap", "sucks", "useless", "pathetic"], Emotion.ANGRY, 4, 0.7),
    
    # Frustration
    (["frustrated", "annoying", "tired of", "sick of", "fed up", 
      "exhausted", "done with"], Emotion.FRUSTRATED, 5, 0.85),
    (["waiting", "wasting time", "taking too long", "again", "still", 
      "repeatedly"], Emotion.FRUSTRATED, 4, 0.75),
    
    # Confusion
    (["confused", "unclear", "don't understand", "what does this mean", 
      "huh", "what?"], Emotion.CONFUSED, 4, 0.85),
    (["maybe", "perhaps", "not sure", "unsure", "might be"], Emotion.CONFUSED, 3, 0.6),
    
    # Happiness
    (["happy", "great", "awesome", "fantastic", "wonderful", "perfect", 
      "excellent", "amazing", "love it"], Emotion.HAPPY, 5, 0.9),
    (["good", "nice", "cool", "satisfied", "pleased", "works well"], Emotion.HAPPY, 4, 0.7),
    
    # Sadness
    (["sad", "upset", "disappointed", "depressed", "unhappy"], Emotion.SAD, 4, 0.85),
    (["feeling down", "not good", "bad day"], Emotion.SAD, 3, 0.7),
    
    # Anxiety
    (["worried", "anxious", "nervous", "concerned", "stress"], Emotion.ANXIOUS, 4, 0.8),
    
    # Excitement
    (["excited", "thrilled", "can't wait", "looking forward"], Emotion.EXCITED, 4, 0.85),
    
    # Disappointment
    (["disappointed", "expected better", "let down", "not what i expected"], Emotion.DISAPPOINTED, 4, 0.8),
]


def _detect_sarcasm(text: str) -> Tuple[bool, float]:
    """Enhanced sarcasm detection with confidence scoring"""
    positive = ["wow", "great", "amazing", "nice", "perfect", "fantastic", 
                "brilliant", "excellent", "wonderful", "super", "awesome"]
    negative = ["problem", "issue", "again", "fail", "not working", "error", 
                "delay", "broken", "stuck", "another", "still"]
    
    confidence = 0.0
    is_sarcastic = False
    
    if any(p in text for p in positive) and any(n in text for n in negative):
        is_sarcastic = True
        confidence = 0.85
    
    sarcastic_phrases = [
        r"(yeah right|sure|as if|of course|totally|obviously)",
        r"(great|perfect|wonderful).*!(not|never)",
        r"that's (just )?great",
        r"just what I needed",
        r"brilliant idea"
    ]
    if any(re.search(phrase, text) for phrase in sarcastic_phrases):
        is_sarcastic = True
        confidence = max(confidence, 0.75)
    
    if re.search(r'[!?]{2,}', text) and any(p in text for p in positive):
        is_sarcastic = True
        confidence = max(confidence, 0.7)
    
    return is_sarcastic, confidence


def _infer_hidden_emotion(emotion: Emotion, sarcasm: bool, text: str = "") -> Emotion:
    """Infer hidden emotion with context awareness"""
    if not sarcasm:
        return emotion
    
    if emotion == Emotion.HAPPY:
        return Emotion.FRUSTRATED
    elif emotion == Emotion.NEUTRAL:
        if any(w in text.lower() for w in ["again", "still", "problem"]):
            return Emotion.ANGRY
        return Emotion.FRUSTRATED
    elif emotion == Emotion.CONFUSED:
        return Emotion.FRUSTRATED
    elif emotion == Emotion.EXCITED:
        return Emotion.ANXIOUS
    else:
        return emotion


def _detect_intent(text: str) -> Tuple[Intent, float]:
    """Enhanced intent detection with confidence scoring"""
    best_intent = Intent.UNKNOWN
    best_score = 0.0
    
    for keywords, intent, score in _INTENT_RULES:
        if any(k in text for k in keywords):
            if score > best_score:
                best_score = score
                best_intent = intent
    
    if "delay" in text or "not delivered" in text or "missing" in text:
        if best_score < 0.7:
            return Intent.COMPLAINT, 0.8
    
    return best_intent, best_score


def _detect_emotion_vector(text: str) -> Tuple[EmotionVector, Emotion, int, float]:
    """Enhanced emotion detection with vector and intensity"""
    vector = EmotionVector()
    
    if text.isupper() and len(text) > 5:
        vector.angry += 0.7
        vector.frustrated += 0.3
    
    exclamation_count = text.count("!")
    vector.angry += min(0.6, exclamation_count * 0.15)
    vector.frustrated += min(0.4, exclamation_count * 0.1)
    
    question_count = text.count("?")
    vector.confused += min(0.5, question_count * 0.15)
    vector.frustrated += min(0.3, question_count * 0.1)
    
    repeat_patterns = ["again", "still", "already", "many times", "multiple times", 
                       "repeated", "told you", "repeatedly", "yet again"]
    if any(p in text for p in repeat_patterns):
        vector.frustrated += 0.7
    
    if any(w in text for w in ["delay", "late", "not delivered", "pending", "waiting"]):
        vector.frustrated += 0.6
    
    if any(w in text for w in ["yar", "yaar", "bro", "dude", "man"]):
        vector.frustrated += 0.3
    
    profanity = ["fuck", "idiot", "stupid", "bitch", "damn", "hell"]
    if any(p in text for p in profanity):
        vector.angry += 0.9
    
    if "problem" in text or "issue" in text or "trouble" in text:
        vector.frustrated += 0.4
    
    if "?" in text or "confused" in text or "unclear" in text:
        vector.confused += 0.5
    
    for keywords, emotion, level, conf in _EMOTION_RULES:
        if any(k in text for k in keywords):
            if emotion == Emotion.ANGRY:
                vector.angry += conf
            elif emotion == Emotion.FRUSTRATED:
                vector.frustrated += conf
            elif emotion == Emotion.HAPPY:
                vector.happy += conf
            elif emotion == Emotion.CONFUSED:
                vector.confused += conf
            elif emotion == Emotion.SAD:
                vector.sad += conf
            elif emotion == Emotion.ANXIOUS:
                vector.anxious += conf
            elif emotion == Emotion.EXCITED:
                vector.excited += conf
            elif emotion == Emotion.DISAPPOINTED:
                vector.disappointed += conf
    
    total = sum([vector.angry, vector.frustrated, vector.happy, vector.confused,
                 vector.sad, vector.anxious, vector.excited, vector.disappointed, vector.neutral])
    
    if total > 0:
        vector.angry /= total
        vector.frustrated /= total
        vector.happy /= total
        vector.confused /= total
        vector.sad /= total
        vector.anxious /= total
        vector.excited /= total
        vector.disappointed /= total
        vector.neutral = max(0, 1 - total) if total < 1 else 0
    else:
        vector.neutral = 1.0
    
    dominant = vector.get_dominant()
    confidence = getattr(vector, dominant.value)
    
    if confidence > 0.7:
        level = 5
    elif confidence > 0.5:
        level = 4
    elif confidence > 0.3:
        level = 3
    elif confidence > 0.15:
        level = 2
    else:
        level = 1
    
    return vector, dominant, level, confidence


def _detect_context(text: str) -> Tuple[Context, float]:
    """Enhanced context detection with confidence scoring"""
    best_context = Context.UNKNOWN
    best_score = 0.0
    
    for keywords, context, score in _CONTEXT_RULES:
        if any(k in text for k in keywords):
            if score > best_score:
                best_score = score
                best_context = context
    
    return best_context, best_score


def _detect_urgency(text: str) -> int:
    """Enhanced urgency detection (1-5 scale)"""
    urgency = 1
    
    if any(w in text for w in _URGENCY_HIGH):
        urgency = 5
    elif any(w in text for w in _URGENCY_MEDIUM):
        urgency = 4
    
    exclamation_count = text.count("!")
    if exclamation_count >= 3:
        urgency = min(5, urgency + 1)
    
    if text.isupper() and len(text) > 5:
        urgency = min(5, urgency + 1)
    
    return urgency


def _detect_clarity(text: str) -> str:
    """Enhanced clarity detection"""
    words = text.split()
    
    if len(words) < 3:
        return "unclear"
    
    has_proper_sentence = bool(re.search(r'[.!?]', text))
    has_question_word = any(w in text for w in ["what", "how", "why", "when", "where"])
    
    if len(words) >= 5 and (has_proper_sentence or has_question_word):
        return "clear"
    elif len(words) >= 3:
        return "partial"
    
    return "unclear"


def _detect_complexity(text: str) -> int:
    """Detect message complexity (1-5)"""
    words = len(text.split())
    if words < 5:
        return 1
    elif words < 10:
        return 2
    elif words < 20:
        return 3
    elif words < 30:
        return 4
    else:
        return 5


def _extract_keywords(text: str) -> List[str]:
    """Extract important keywords"""
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "are"}
    words = text.split()
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    return list(set(keywords))[:10]


def _estimate_risk(context: Context, emotion: Emotion, urgency: int) -> int:
    """Enhanced risk estimation (1-5 scale)"""
    risk = 1
    
    high_risk_contexts = [Context.PAYMENT_FAILED, Context.PRIVACY_CONCERN]
    medium_risk_contexts = [Context.LOGIN_ERROR, Context.TECHNICAL_ERROR]
    
    if context in high_risk_contexts:
        risk += 3
    elif context in medium_risk_contexts:
        risk += 2
    
    if emotion in [Emotion.ANGRY, Emotion.FRUSTRATED]:
        risk += 2
    elif emotion == Emotion.ANXIOUS:
        risk += 1
    
    if urgency >= 4:
        risk += 2
    elif urgency >= 3:
        risk += 1
    
    return min(5, risk)


def _compute_priority(intent: Intent, urgency: int, risk: int, emotion_level: int) -> float:
    """Compute priority score (0-1 range)"""
    priority = 0.0
    
    # Intent weight (0-0.4)
    intent_weights = {
        Intent.COMPLAINT: 0.4,
        Intent.HELP: 0.35,
        Intent.COMMAND: 0.3,
        Intent.QUESTION: 0.2,
        Intent.UNKNOWN: 0.15
    }
    priority += intent_weights.get(intent, 0.15)
    
    # Urgency weight (urgency 1-5 → 0-0.2)
    priority += ((urgency - 1) / 4) * 0.2
    
    # Risk weight (risk 1-5 → 0-0.3)
    priority += ((risk - 1) / 4) * 0.3
    
    # Emotion level weight (level 1-5 → 0-0.1)
    priority += ((emotion_level - 1) / 4) * 0.1
    
    # Ensure range 0-1
    return round(min(1.0, max(0.0, priority)), 3)


def encode(text: str) -> IbtcodeState:
    """Main encoding function - converts raw text to IbtcodeState"""
    start_time = time.time()
    
    if not text or not text.strip():
        logger.warning("Encoder received empty input")
        return IbtcodeState(raw_text=text or "")
    
    try:
        original_text = text
        normalized_text = _normalize(text)
        
        intent, intent_conf = _detect_intent(normalized_text)
        emotion_vector, emotion, emotion_level, emotion_conf = _detect_emotion_vector(normalized_text)
        
        sarcasm, sarcasm_conf = _detect_sarcasm(normalized_text)
        hidden_emotion = _infer_hidden_emotion(emotion, sarcasm, normalized_text)
        
        context, context_conf = _detect_context(normalized_text)
        urgency = _detect_urgency(normalized_text)
        clarity = _detect_clarity(normalized_text)
        complexity = _detect_complexity(normalized_text)
        
        risk = _estimate_risk(context, emotion, urgency)
        priority = _compute_priority(intent, urgency, risk, emotion_level)
        
        overall_conf = (intent_conf + emotion_conf + context_conf) / 3
        uncertainty = 1.0 - overall_conf
        
        keywords = _extract_keywords(normalized_text)
        
        processing_time = (time.time() - start_time) * 1000
        metadata = Metadata(
            processing_time_ms=processing_time,
            char_count=len(original_text),
            word_count=len(original_text.split()),
            tokens=normalized_text.split()
        )
        
        state = IbtcodeState(
            intent=intent,
            emotion=emotion,
            emotion_level=emotion_level,
            context=context,
            confidence=overall_conf,
            uncertainty=uncertainty,
            risk=risk,
            priority=priority,
            escalate_flag=risk >= 4 or emotion in [Emotion.ANGRY, Emotion.FRUSTRATED],
            clarity=clarity,
            urgency=urgency,
            complexity=complexity,
            trust=0.7,
            expectation="resolution" if intent in [Intent.COMPLAINT, Intent.HELP] else "information",
            emotion_vector=emotion_vector,
            sarcasm=sarcasm,
            sarcasm_confidence=sarcasm_conf,
            hidden_emotion=hidden_emotion,
            contradiction_score=0.0,
            raw_text=original_text,
            normalized_text=normalized_text,
            metadata=metadata,
            keywords=keywords
        )
        
        logger.debug(f"Encoded: I={intent.value} E={emotion.value} L={emotion_level} "
                    f"Context={context.value} Risk={risk} Priority={priority}")
        
        return state
        
    except Exception as e:
        logger.error(f"Encoding failed for '{text}': {e}")
        return IbtcodeState(
            raw_text=text,
            intent=Intent.UNKNOWN,
            emotion=Emotion.NEUTRAL,
            risk=1,
            urgency=1
        )