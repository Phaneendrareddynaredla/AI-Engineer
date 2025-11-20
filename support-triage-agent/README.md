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

## Run (development)
1. Install requirements: `pip install -r requirements.txt`
2. Start server: `uvicorn app.main:app --reload --port 8000`
3. POST to /triage with JSON `{"description": "..."}`

## OpenAI integration (optional)
Set environment variable `OPENAI_API_KEY`. The app will use OpenAI for summarization if the key is present.

## notes
- Clean separation of concerns, test coverage for API endpoints, optional LLM integration.
- KB stored as JSON for simplicity; replace with vector DB for production (FAISS/Pinecone).
