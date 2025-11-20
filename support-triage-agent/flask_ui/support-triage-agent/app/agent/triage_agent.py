import os
from typing import List, Dict, Any
from app.agent.kb_search import KBSearchTool
from app.agent.llm_client import LLMClient

class TriageAgent:
    def __init__(self, kb_path=None, use_openai=False):
        # kb_path optional; default uses package data file path
        cwd = os.path.dirname(os.path.abspath(__file__))
        default_kb = os.path.join(cwd, "..", "..", "data", "kb.json")
        self.kb_path = kb_path or default_kb
        self.kb_tool = KBSearchTool(self.kb_path)
        self.llm = LLMClient(use_openai=use_openai)

    def handle_ticket(self, description: str) -> Dict[str, Any]:
        summary = self.llm.summarize(description)
        category = self.llm.classify_category(description)
        severity = self.llm.classify_severity(description)

        related = self.kb_tool.search(description, top_k=3)
        known_issue = len(related) > 0

        if known_issue:
            action = "Attach KB article and respond to user"
        else:
            if severity in ("Critical", "High"):
                action = "Escalate to backend on-call"
            else:
                action = "Request logs/screenshots from customer"

        return {
            "summary": summary,
            "category": category,
            "severity": severity,
            "likely": "known_issue" if known_issue else "new_issue",
            "related_issues": related,
            "suggested_action": action
        }
