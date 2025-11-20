import json
import os
from typing import List, Dict, Any

class KBSearchTool:
    def __init__(self, kb_path: str):
        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"KB file not found: {kb_path}")
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q = query.lower()
        scored = []
        for entry in self.kb:
            text = ' '.join([entry.get('title',''), ' '.join(entry.get('symptoms',[])), entry.get('category','')]).lower()
            # keyword overlap score
            score = sum(1 for tok in q.split() if tok in text)
            scored.append((score, entry))
        # filter zeros and sort
        matches = [e for e in scored if e[0] > 0]
        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches[:top_k]]
