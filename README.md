# AI-Engineer
Support Triage Agent

A small, production-minded support-ticket triage agent that ingests free-text tickets and returns a structured triage decision: a short summary, category, severity, related KB entries (if any), whether it's likely a known issue or new, and a suggested next action.

This README explains how to run the project locally, the architectural choices I made, key assumptions, and how I would take this to production. (This repo follows the requirements: HTTP endpoint POST /triage, a small JSON KB, and basic tests.) 

Assignment Screen for AI Engine…

 

Phaneendra_reddy_naredla-support-triage agent.ipynb - Colab

Quick highlights (elevator pitch)

Lightweight FastAPI service that accepts a free-text ticket and returns a structured triage response.

Clean separation: orchestration (TriageAgent), LLM client (swappable/mocked), and KB search tool.

Small sample KB (12 entries) included for demonstration and deterministic matching.

Dockerfile + tests included for easy demonstration and CI integration.

Repo structure
support-triage-agent/
├─ app/
│  ├─ main.py                # FastAPI app & /triage endpoint
│  ├─ models.py              # Pydantic request/response models
│  ├─ agent/
│  │  ├─ triage_agent.py     # Orchestration & decision logic
│  │  ├─ llm_client.py       # LLM wrapper (mockable / OpenAI client)
│  │  └─ kb_search.py        # Simple keyword-based KB search tool
├─ data/
│  └─ kb.json                # 12 sample KB entries
├─ tests/
│  └─ test_api.py            # smoke tests & edge-case tests
├─ Dockerfile
├─ requirements.txt
└─ README.md


Quickstart — run locally (development)

pip installed

An OpenAI API key is also used if you want to enable live LLM calls (optional). If we don't provide a key the code uses a deterministic heuristic/mock so the service still works for tests and demos. See app/agent/llm_client.py.

Installation
git clone <your-repo>
cd support-triage-agent
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
# or on Windows: .venv\Scripts\activate
pip install -r requirements.txt

Running
# development server with auto-reload
uvicorn app.main:app --reload --port 8000

Core components

TriageAgent — orchestrates: calls LLM client for summary & classification, calls KBSearchTool for related issues, then uses deterministic rules to produce suggested_action.

LLMClient — wrapper around OpenAI (modern API usage guarded by environment variable) with heuristic fallbacks when the API call fails or when OPENAI_API_KEY is missing.

KBSearchTool — loads data/kb.json and computes keyword overlap to find top matches.

FastAPI app serves /triage with Pydantic validation for robust request/response handling.

Assumptions

Tickets are English and reasonably concise .

KB contains curated, human-readable items (title, category, symptom list, recommended action).

For the take-home, a lightweight keyword search on KB is sufficient to demonstrate the idea; semantic search would be used in production.

LLM calls may fail or be rate-limited; system must work without them (hence heuristics/mock LLM).

No PII-sensitive processing is included; if tickets contain PII, a compliance strategy (redaction, secure processing) would be required.

Production deployment plan (how I would do it for real)

This is intentionally pragmatic and focuses on reliability, monitoring, cost, and safety.

1) Containerize & CI/CD

Built and published a Docker image (Dockerfile already included). Tag images with semantic versions.


2) Infrastructure & runtime

Kubernetes (EKS/GKE/AKS) or serverless containers (ECS Fargate, Cloud Run) depending on team preference:

For predictable, moderate traffic: GKE/EKS with HPA (horizontal pod autoscaler) based on CPU / request latency.

For bursty or pay-as-you-go use cases: Cloud Run or Fargate to minimize ops overhead.

Expose service via an API gateway (Cloud Load Balancer / AWS ALB / GCP API Gateway) for TLS termination, auth, and rate limiting.

3) Model/LLM considerations

Secret/config: Store API keys or model endpoints in Secrets Manager (AWS Secrets Manager, GCP Secret Manager) and reference via environment variables. No secrets in repo.

Model hosting:

Use managed LLM (OpenAI) or hosted model provider — route all LLM traffic through a centralized service layer that handles retries, rate-limits, caching, and cost accounting.

For latency-sensitive flows, precompute short summaries or use a smaller low-latency model. For high-cost transforms, consider asynchronous workflows (e.g., immediately classify using heuristics, and run full LLM processing in background).

Fallback: Always implement a deterministic fallback path (current heuristics) so service degrades gracefully if the LLM is unavailable.

4) Observability & alerts

Logging: Structured logs (JSON) sent to centralized logging (Cloud Logging / ELK). Include correlation IDs for each request.

Metrics: Expose Prometheus metrics (request latency, success/error rates, LLM call latency, KB match rate, cache hit rate).

Tracing: Distributed tracing (OpenTelemetry) to trace requests across API gateway → service → LLM / KB / DB.

Alerts: SLO/SLA with alerts for high error rates, increased latencies, or upstream model provider outages.

5) Data & storage

KB: Move from flat file to a managed DB for KB authoring (e.g., a simple CMS + JSON export) and vector store for semantic search (FAISS in a service, or managed Pinecone/Weaviate).

Audit & retention: Keep a secure, audit-log of ticket inputs (redact/obfuscate PII) for model improvement and compliance.

6) Reliability & scaling

Caching: Cache frequent KB search results and LLM summaries for repeated queries to reduce cost/latency.

Retries: Safe exponential backoff with circuit breaker for LLM requests.

Rate limiting & request validation: API gateway enforces per-API-key or per-client quotas; service validates payload size to protect downstream costs.

Testing: Add integration tests against a staging LLM endpoint and load tests (k6 / Locust) to validate scaling.

7) Security

TLS everywhere, private subnets for internal services, least privilege IAM for secrets and storage.

If processing PII, adopt redaction, encryption at rest, and strict access controls.

8) Cost controls

Use smaller models for routine tasks (heuristic classification) and larger ones sparingly (detailed summarization or escalation reasoning).

Monitor token usage and put budget alerts on LLM spending.

Example production deployment (stepwise)

Add multi-env config: config/dev.env, config/prod.env (do not store secrets in source).

Build and push Docker image in CI.

Deploy to staging on Cloud Run (fast), test end-to-end.

Promote to Kubernetes in prod when traffic/requirements justify it: create k8s Deployment + HPA, Service + Ingress, configure LB, secrets, and monitoring.

Migrate KB to vector store and update KBSearchTool to call vector DB endpoint.

Implement model/LLM proxy with quota enforcement and caching to control cost.

Trade-offs & open items (what I would improve next)

KB search: replace keyword-overlap with embeddings + vector similarity for better recall/precision.

LLM prompts: move prompts/config to a prompt-management layer and add prompt versioning.

Async flows: for high-latency expensive calls, consider asynchronous processing (webhook or job queue) to avoid blocking the API.

Human-in-loop: add an internal UI for agents to review triage decisions and feed corrections back into KB and model training.

Rate-limiting / billing: add token level accounting to track per-customer/tenant LLM costs.

Operational checklist before go-live

 Add authentication & API key management.

 Secrets in Secret Manager; read at startup.

 Add request size limits and schema validation.

 Add Prometheus metrics & alerts.

 Harden logging and PII redaction.

 Run load tests and SLO reports.



 Notes for reviewers 

Clean separation of concerns: orchestration, tools, and API layers are intentionally modular. This makes swapping in better KB search or alternate LLM providers straightforward. 


The sample KB and tests are included to show matching behavior and edge-case handling (empty descriptions, basic validation). 
