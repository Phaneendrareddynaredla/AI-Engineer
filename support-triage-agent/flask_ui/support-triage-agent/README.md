# Support Triage Agent (Submission)
## Structure
support-triage-agent/
├─ app/
│  ├─ main.py
│  ├─ models.py
│  ├─ agent/
│  │  ├─ triage_agent.py
│  │  ├─ llm_client.py
│  │  └─ kb_search.py
├─ data/
│  └─ kb.json
├─ tests/
│  └─ test_api.py
├─ Dockerfile
├─ requirements.txt

##Introduction
This project implements a Support Ticket Triage System using FastAPI, a custom LLM-powered agent, a Knowledge Base (KB) search tool, and an optional Flask-based user interface. The goal of this system is to automatically classify incoming customer support tickets, estimate their severity, retrieve related known issues, and recommend the next action for support teams.
The notebook demonstrates the complete workflow: installation of dependencies, creation of project structure, implementation of agent logic, testing with PyTest, OpenAI integration upgrades, and running a web UI with ngrok exposure.
2. Environment Setup & Dependencies
The first part of your notebook installs all required libraries including:
FastAPI + Uvicorn for backend API
Pydantic for request/response models
Requests for API calls
PyTest for testing
OpenAI Python SDK
Flask for UI
pyngrok for exposing local apps
matplotlib, seaborn, scikit-learn (not heavily used, but included)
This ensures the environment is consistent and reproducible.

## Run (development)
1. Install requirements: `pip install -r requirements.txt`
2. Start server: `uvicorn app.main:app --reload --port 8000`
3. POST to /triage with JSON `{"description": "..."}`

## OpenAI integration (optional)
Set environment variable `OPENAI_API_KEY`. The app will use OpenAI for summarization if the key is present.

## 
- Clean separation of concerns, test coverage for API endpoints, optional LLM integration.
- KB stored as JSON for simplicity; replace with vector DB for production (FAISS/Pinecone).
