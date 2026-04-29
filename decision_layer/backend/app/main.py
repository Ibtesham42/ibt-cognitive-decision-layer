"""
FastAPI Backend for Decision Layer
Integrates Phase 1 (Symbolic Parser) and Phase 2 (Reasoning Engine)
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import asyncio

from .symbolic_parser import SymbolicParser, SymbolicExpression
from .reasoning_engine import DeepReasoningEngine, ReasoningTrace

app = FastAPI(
    title="Decision Layer API",
    description="Universal Symbolic Language & Deep Reasoning Engine",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
parser = SymbolicParser()
reasoning_engine = DeepReasoningEngine()


class ParseRequest(BaseModel):
    text: str
    output_format: str = "dict"  # dict, string, full


class ReasonRequest(BaseModel):
    problem: str
    symbolic_input: Optional[Dict[str, Any]] = None
    depth: int = 5  # 1-5
    max_iterations: int = 5


@app.get("/")
async def root():
    return {
        "message": "Decision Layer API - Phase 1 & 2 Complete",
        "endpoints": {
            "parse": "/api/v1/parse",
            "reason": "/api/v1/reason",
            "websocket": "/ws/reason",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "symbolic_parser": "operational",
            "reasoning_engine": "operational",
            "api": "operational"
        }
    }


@app.post("/api/v1/parse")
async def parse_text(request: ParseRequest):
    """Parse natural language into symbolic representation"""
    try:
        if request.output_format == "string":
            result = parser.parse_to_string(request.text)
            return {"result": result}
        elif request.output_format == "full":
            result = parser.parse(request.text)
            return result.to_dict()
        else:  # dict
            result = parser.parse_to_dict(request.text)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/reason")
async def reason_problem(request: ReasonRequest):
    """Execute deep reasoning on a problem"""
    try:
        # Update engine parameters if needed
        reasoning_engine.max_iterations = request.max_iterations
        
        # Execute reasoning
        trace = reasoning_engine.reason(
            problem=request.problem,
            symbolic_input=request.symbolic_input,
        )
        
        return trace.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/reason")
async def websocket_reason(websocket: WebSocket):
    """WebSocket endpoint for streaming reasoning steps"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            problem = request_data.get("problem", "")
            
            if not problem:
                await websocket.send_json({"error": "Problem statement required"})
                continue
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "started",
                "problem": problem,
                "message": "Starting reasoning process..."
            })
            
            # Execute reasoning with streaming
            reasoning_engine.max_iterations = request_data.get("max_iterations", 5)
            
            # Simulate streaming (in production, modify engine to yield steps)
            trace = reasoning_engine.reason(problem)
            
            # Send complete result
            await websocket.send_json({
                "type": "complete",
                "data": trace.to_dict()
            })
            
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()


@app.get("/api/v1/examples")
async def get_examples():
    """Return example queries"""
    return {
        "parsing_examples": [
            "The robot moves quickly to the left",
            "If temperature increases then pressure will rise",
            "All students must complete the assignment before tomorrow"
        ],
        "reasoning_examples": [
            "How to reduce system latency?",
            "Why is customer satisfaction declining?",
            "What is the optimal resource allocation strategy?",
            "How can we improve decision-making accuracy?"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
