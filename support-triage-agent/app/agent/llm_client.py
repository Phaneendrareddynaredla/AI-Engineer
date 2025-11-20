
import os
from openai import OpenAI

class LLMClient:
    def __init__(self, use_openai: bool = False, model_name: str = "gpt-4.1-mini"):
        self.use_openai = use_openai
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.use_openai and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.use_openai = False
            self.client = None

    def summarize(self, text: str) -> str:
        if self.use_openai:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You summarize support tickets."},
                        {"role": "user", "content": f"Summarize this in one short sentence: {text}"}
                    ],
                    max_tokens=50,
                    temperature=0.0
                )
                return response.choices[0].message["content"].strip()
            except Exception as e:
                print("[OpenAI Error] Falling back to heuristic summary:", e)

        # fallback summarization
        sentences = [s.strip() for s in text.replace("\n"," ").split(".") if s.strip()]
        return sentences[0][:250] if sentences else text[:250]

    def classify_severity(self, text: str) -> str:
        t = text.lower()
        if any(k in t for k in ["outage","down","critical","data loss","security","payment failing"]):
            return "Critical"
        if any(k in t for k in ["error","500","503","failure","crash"]):
            return "High"
        if any(k in t for k in ["slow","latency","delay"]):
            return "Medium"
        return "Low"

    def classify_category(self, text: str) -> str:
        t = text.lower()
        if any(k in t for k in ["billing","payment","invoice","refund"]):
            return "Billing"
        if any(k in t for k in ["login","signin","password","2fa"]):
            return "Login"
        if any(k in t for k in ["error","exception","crash","bug"]):
            return "Bug"
        if any(k in t for k in ["slow","performance","latency","timeout"]):
            return "Performance"
        return "Question/How-To"
