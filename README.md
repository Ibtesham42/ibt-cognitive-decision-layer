# Ibtcode Cognitive Decision Layer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![AI](https://img.shields.io/badge/AI-Decision%20Layer-purple.svg)]()

A production-grade, modular AI decision engine that adds reasoning, emotion awareness, and safe control on top of LLMs for reliable responses.

Turn any LLM into a reliable AI system with structured reasoning, emotional intelligence, and decision control.

---

## Why this project

Traditional LLM-based systems generate responses directly without control, leading to hallucinations, unsafe outputs, and inconsistent behavior.

This project introduces a structured decision layer that:

* Separates reasoning from generation
* Adds emotional intelligence and risk awareness
* Enables safe, controllable AI responses

---

## Use Cases

* Customer support automation
* AI chatbots with controlled behavior
* Safety-critical AI systems
* LLM-based assistants with decision logic
* Multi-turn conversational systems


## Features

* Emotion detection (9 emotions: angry, frustrated, happy, confused, sad, anxious, excited, disappointed, neutral)
* Intent classification (12 intents: question, command, complaint, help, greeting, farewell, gratitude, feedback, clarification, confirmation, request)
* Context detection (13 contexts: payment, login, performance, billing, technical, privacy, onboarding, etc.)
* Sarcasm detection with hidden emotion inference
* Risk scoring (1-5 scale)
* Priority calculation with configurable weights
* Conversation memory with sliding window
* Contradiction detection across turns
* Production-ready logging and error handling

---

## Installation

### From PyPI (Recommended)

```bash
pip install ibt-cognitive-decision-layer
```

### From GitHub

```bash
git clone https://github.com/Ibtesham42/ibt-cognitive-decision-layer.git
cd ibt-cognitive-decision-layer
pip install -e .
```

---

## Requirements

* Python >= 3.8
* pydantic >= 2.0
* loguru >= 0.7

---

## Quick Start

### Basic Usage

```python
from ibtcode import IbtcodeSystem

# Initialize the engine
engine = IbtcodeSystem()

# Process a user message
response, state, decision = engine.process("My payment failed!")

print(f"Response: {response}")
print(f"Emotion: {state.emotion}")
print(f"Intent: {state.intent}")
print(f"Context: {state.context}")
print(f"Strategy: {decision.strategy}")
print(f"Action: {decision.action}")
```

---

### Complete Example

```python
from ibtcode import IbtcodeSystem
from ibtcode.models import Emotion, Intent, Context

engine = IbtcodeSystem(memory_size=20)

messages = [
    "Hello, I need help",
    "My login is not working",
    "I've tried resetting password 3 times!",
    "This is really frustrating"
]

for msg in messages:
    response, state, decision = engine.process(msg)
    print(f"\nUser: {msg}")
    print(f"AI: {response}")
    print(f"  Emotion: {state.emotion} (level {state.emotion_level})")
    print(f"  Intent: {state.intent}")
    print(f"  Context: {state.context}")
    print(f"  Strategy: {decision.strategy}")
    print(f"  Priority: {state.priority:.2f}")
    print(f"  Risk: {state.risk}")

engine.reset()
```

---

## Using Individual Components

```python
from ibtcode.encoder import encode
from ibtcode.decision import decide

state = encode("Help me reset my password")
print(f"Intent: {state.intent}")
print(f"Emotion: {state.emotion}")

decision = decide(state)
print(f"Strategy: {decision.strategy}")
```

---

## Understanding the Output

### IbtcodeState Fields

| Field               | Type        | Description          |
| ------------------- | ----------- | -------------------- |
| intent              | Intent      | User's intent        |
| emotion             | Emotion     | Detected emotion     |
| emotion_level       | int (1-5)   | Emotion intensity    |
| context             | Context     | Conversation context |
| confidence          | float (0-1) | Confidence score     |
| uncertainty         | float (0-1) | Uncertainty          |
| risk                | int (1-5)   | Risk level           |
| priority            | float (0-1) | Priority score       |
| urgency             | int (1-5)   | Urgency              |
| escalate_flag       | bool        | Escalation needed    |
| clarity             | str         | Message clarity      |
| sarcasm             | bool        | Sarcasm detection    |
| contradiction_score | float (0-1) | Contradiction score  |

---




### Decision Fields

| Field      | Type        | Description       |
| ---------- | ----------- | ----------------- |
| strategy   | Strategy    | Response strategy |
| action     | Action      | Action to take    |
| confidence | float (0-1) | Confidence        |
| reasoning  | str         | Explanation       |

---

## Available Strategies

* DE_ESCALATE
* CLARIFY
* EXPLAIN
* SUPPORT
* EMPATHIZE
* APOLOGIZE
* NORMAL

---

## Configuration

Create a `.env` file:

```env
ANGRY_THRESHOLD=0.4
HAPPY_THRESHOLD=0.6

PRIORITY_W_URGENCY=0.4
PRIORITY_W_RISK=0.3
PRIORITY_W_EMOTION=0.3

MEMORY_SIZE=10
UNCERTAINTY_THRESHOLD=0.5
RISK_THRESHOLD=3
URGENCY_THRESHOLD=3

AUTO_ESCALATE_ON_HIGH_RISK=true
AUTO_ESCALATE_ON_ANGRY=true
```

---

## Integration Examples

### Flask API

```python
from flask import Flask, request, jsonify
from ibtcode import IbtcodeSystem

app = Flask(__name__)
engine = IbtcodeSystem()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    response, state, decision = engine.process(message)

    return jsonify({
        'response': response,
        'emotion': state.emotion,
        'intent': state.intent,
        'strategy': decision.strategy,
        'confidence': decision.confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Discord Bot

```python
import discord
from ibtcode import IbtcodeSystem

client = discord.Client()
engine = IbtcodeSystem()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response, state, decision = engine.process(message.content)

    if state.emotion == 'angry':
        await message.add_reaction('😠')
    elif state.emotion == 'happy':
        await message.add_reaction('😊')

    await message.channel.send(response)

client.run('YOUR_BOT_TOKEN')
```

---

### Custom LLM Integration

```python
from ibtcode import IbtcodeSystem
from ibtcode.models import Strategy

class CustomChatbot:
    def __init__(self):
        self.decision_engine = IbtcodeSystem()
        self.llm = YourLLM()

    def respond(self, user_message):
        _, state, decision = self.decision_engine.process(user_message)

        if decision.strategy == Strategy.DE_ESCALATE:
            prompt = f"User is angry. Be empathetic: {user_message}"
        elif decision.strategy == Strategy.CLARIFY:
            prompt = f"User is confused. Ask questions: {user_message}"
        else:
            prompt = f"Respond helpfully: {user_message}"

        return self.llm.generate(prompt)
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Architecture

```
User Input
    ↓ encoder.py
    ↓ state_engine.py
    ↓ reasoning.py
    ↓ decision.py
    ↓ response.py
    ↑ system.py
```

---

## Project Structure

```
ibt-cognitive-decision-layer/
├── ibtcode/
│   ├── __init__.py
│   ├── models.py
│   ├── config.py
│   ├── encoder.py
│   ├── state_engine.py
│   ├── reasoning.py
│   ├── decision.py
│   ├── response.py
│   ├── system.py
│   ├── memory.py
│   └── logger.py
├── tests/
├── main.py
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Interactive CLI

```bash
python main.py
```

Example:

```
You: My payment failed!
AI: I sincerely apologize...

Intent: complaint
Emotion: neutral (level 5)
Context: payment_failed
Strategy: de_escalate
Priority: 0.73
Risk: 4
```

---

## License

MIT License

---

## Author

Ibtesham Akhtar

---

## Contributing

* Fork the repository
* Create a feature branch
* Commit changes
* Push and open a Pull Request

---

## Support

https://github.com/Ibtesham42/ibt-cognitive-decision-layer/issues

---

## Usage Summary

### Installation

```bash
pip install ibt-cognitive-decision-layer
```

### Usage

```python
from ibtcode import IbtcodeSystem

engine = IbtcodeSystem()
response, state, decision = engine.process("Your message here")
```

