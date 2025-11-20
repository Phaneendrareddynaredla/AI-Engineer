from pydantic import BaseModel
from typing import List, Dict, Any

class TriageRequest(BaseModel):
    description: str

class KBItem(BaseModel):
    id: str
    title: str
    category: str
    symptoms: List[str]
    recommended_action: str

class TriageResponse(BaseModel):
    summary: str
    category: str
    severity: str
    likely: str
    related_issues: List[KBItem]
    suggested_action: str
