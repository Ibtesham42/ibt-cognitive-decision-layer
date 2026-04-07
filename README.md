# Ibtcode Cognitive Engine

A production-grade, modular AI decision architecture — state-aware, interpretable, and emotion-integrated.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run interactive CLI
python main.py

# 4. Run tests
pytest tests/ -v
```

## Architecture

```
User Input
    ↓ encoder.py        Algorithm 1 — Ibtcode Encoder
    ↓ state_engine.py   Algorithm 2 — State Update Engine
    ↓ reasoning.py      Algorithm 3 — Reasoning Engine
    ↓ decision.py       Algorithm 4 — Decision Engine
    ↓ response.py       Algorithm 5 — Response Generator
    ↑ system.py         Algorithm 6 — Orchestrator
```

## Project Structure

```
ibtcode_project/
├── main.py               # Entry point (interactive CLI)
├── requirements.txt
├── .env.example
├── README.md
├── ibtcode/
│   ├── __init__.py
│   ├── models.py         # Pydantic data models
│   ├── config.py         # Environment-driven config
│   ├── encoder.py        # Algorithm 1
│   ├── state_engine.py   # Algorithm 2
│   ├── reasoning.py      # Algorithm 3
│   ├── decision.py       # Algorithm 4
│   ├── response.py       # Algorithm 5
│   ├── system.py         # Algorithm 6 (orchestrator)
│   ├── memory.py         # Sliding window memory
│   └── logger.py         # Loguru logging setup
└── tests/
    ├── test_encoder.py
    └── test_system.py
```
