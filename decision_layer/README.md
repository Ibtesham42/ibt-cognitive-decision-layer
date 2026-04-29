# Decision Layer AI - Universal Symbolic Reasoning System

A complete end-to-end decision layer for AI using symbolic language and deep reasoning.

## 🎯 Overview

This system extends beyond emotion detection to provide universal symbolic reasoning capabilities:

- **Phase 1**: Universal Symbolic Language Parser
- **Phase 2**: Deep Ground-Level Reasoning Engine  
- **Phase 3**: Full Frontend-Backend Integration
- **Phase 4**: Comprehensive Testing Suite
- **Phase 5**: Production Deployment Configuration
- **Phase 6**: Documentation & Workflow Diagrams

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
cd decision_layer
docker-compose up --build
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Running Components Separately

**Backend:**
```bash
cd decision_layer/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd decision_layer/frontend
npm install
npm run dev
```

## 📁 Project Structure

```
decision_layer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── symbolic_parser.py   # Phase 1: Symbolic Language
│   │   └── reasoning_engine.py  # Phase 2: Deep Reasoning
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Tailwind styles
│   ├── package.json
│   ├── vite.config.js
│   └── nginx.conf
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 🔧 API Endpoints

### POST /api/v1/parse
Parse natural language into symbolic representation

```json
{
  "text": "The robot moves quickly to the left",
  "output_format": "full"
}
```

### POST /api/v1/reason
Execute deep reasoning on a problem

```json
{
  "problem": "How to reduce system latency?",
  "depth": 5,
  "max_iterations": 5
}
```

### GET /health
Health check endpoint

## 🧪 Testing

```bash
# Run backend tests
cd decision_layer/backend
pytest

# Test symbolic parser
python -m app.symbolic_parser

# Test reasoning engine
python -m app.reasoning_engine
```

## 📊 Features

### Symbolic Language (Phase 1)
- 11 primitive types: ENTITY, ACTION, RELATION, ATTRIBUTE, TEMPORAL, SPATIAL, CAUSAL, MODALITY, QUANTIFIER, NEGATION, CONDITIONAL
- Universal ontology covering all domains
- Multiple output formats (string, dict, full)

### Deep Reasoning (Phase 2)
- 5-level decomposition (Surface → First Principles)
- Causal chain analysis
- Multi-strategy solution exploration
- Meta-reasoning evaluation
- Iterative convergence

### Web Interface (Phase 3)
- Real-time parsing visualization
- Interactive reasoning dashboard
- Solution comparison with scores
- Example queries included

## 🏭 Your Original Code

Your original code remains intact in `/workspace/ibtcode/`:
- encoder.py
- decision.py
- memory.py
- models.py
- config.py
- And all other original files

## 📝 License

MIT License
