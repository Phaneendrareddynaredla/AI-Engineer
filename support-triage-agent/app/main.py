from fastapi import FastAPI, HTTPException
from app.models import TriageRequest, TriageResponse
from app.agent.triage_agent import TriageAgent
import os

app = FastAPI(title="Support Triage Agent")

# Use real OpenAI if OPENAI_API_KEY provided, otherwise use mock LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
agent = TriageAgent(use_openai=bool(OPENAI_API_KEY))

@app.post("/triage", response_model=TriageResponse)
async def triage_endpoint(req: TriageRequest):
    desc = req.description.strip()
    if not desc:
        raise HTTPException(status_code=422, detail="description cannot be empty")
    return agent.handle_ticket(desc)
