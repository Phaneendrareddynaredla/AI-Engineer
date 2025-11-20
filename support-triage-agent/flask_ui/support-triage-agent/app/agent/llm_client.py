import os
from typing import Optional
try:
    import openai
except Exception:
    openai = None

class LLMClient:
    def __init__(self, use_openai: bool = False, model_name: str = "gpt-3.5-turbo"):
        self.use_openai = use_openai and (openai is not None)
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.use_openai and not self.api_key:
            # fallback to mock if key missing
            self.use_openai = False

        if self.use_openai:
            openai.api_key = self.api_key

    def summarize(self, text: str) -> str:
        if self.use_openai:
            # inexpensive, short prompt - optional (calls OpenAI)
            prompt = f"Summarize the following support ticket in one short sentence:\n\n{text}"
            try:
                resp = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=50,
                    temperature=0.0
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                # graceful fallback to heuristic
                print("[LLM WARNING] OpenAI call failed, falling back to heuristic:", e)
        # heuristic summarization
        sentences = [s.strip() for s in text.replace('\n',' ').split('.') if s.strip()]
        return sentences[0][:250] if sentences else text[:250]

    def classify_severity(self, text: str) -> str:
        # simple heuristics; you can replace with LLM classification if desired
        t = text.lower()
        if any(k in t for k in ["data loss","payment","security","critical","outage","down","cannot login"]):
            return "Critical"
        if any(k in t for k in ["fails","failure","error","500","502","503","unavailable","crash"]):
            return "High"
        if any(k in t for k in ["slow","latency","delay","timeout"]):
            return "Medium"
        return "Low"

    def classify_category(self, text: str) -> str:
        t = text.lower()
        if any(k in t for k in ["billing","invoice","payment","refund"]):
            return "Billing"
        if any(k in t for k in ["login","signin","password","2fa"]):
            return "Login"
        if any(k in t for k in ["error","exception","stacktrace","crash"]):
            return "Bug"
        if any(k in t for k in ["slow","performance","latency","timeout"]):
            return "Performance"
        return "Question/How-To"
