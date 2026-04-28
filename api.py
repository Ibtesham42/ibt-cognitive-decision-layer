from fastapi import FastAPI
from pydantic import BaseModel
from ibtcode import IbtcodeSystem

app = FastAPI()
engine = IbtcodeSystem()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Ibtcode API running"}

@app.post("/chat")
def chat(req: ChatRequest):
    response, state, decision = engine.process(req.message)

    return {
        "response": response,
        "emotion": state.emotion,
        "intent": state.intent,
        "strategy": decision.strategy,
        "priority": state.priority
    }