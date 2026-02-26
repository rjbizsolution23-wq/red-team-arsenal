"""
🔴💀 HuggingFace Client — Inference API + local pipeline support
"""
import os
from typing import Any, Dict, List, Optional, Union
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HF_API_BASE = "https://api-inference.huggingface.co/models"


class HuggingFaceClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or HF_TOKEN
        self._headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        self._client = httpx.Client(headers=self._headers, timeout=120)

    def embed(self, texts: Union[str, List[str]], model: str = "sentence-transformers/all-mpnet-base-v2") -> List[List[float]]:
        if isinstance(texts, str):
            texts = [texts]
        payload = {"inputs": texts, "options": {"wait_for_model": True}}
        try:
            resp = self._client.post(f"{HF_API_BASE}/{model}", json=payload)
            resp.raise_for_status()
            result = resp.json()
            if isinstance(result, list) and result and isinstance(result[0], float):
                return [result]
            return result
        except Exception as e:
            logger.error(f"[HuggingFace] Embed error ({model}): {e}")
            return [[0.0] * 768] * len(texts)

    def classify(self, text: str, model: str = "distilbert-base-uncased") -> List[Dict]:
        try:
            resp = self._client.post(f"{HF_API_BASE}/{model}", json={"inputs": text, "options": {"wait_for_model": True}})
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"[HuggingFace] Classify error ({model}): {e}")
            return []

    def ner(self, text: str, model: str = "dslim/bert-base-NER") -> List[Dict]:
        try:
            resp = self._client.post(f"{HF_API_BASE}/{model}", json={"inputs": text, "options": {"wait_for_model": True}})
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"[HuggingFace] NER error ({model}): {e}")
            return []

    def text_generation(self, prompt: str, model: str = "bigcode/starcoder2-15b", max_new_tokens: int = 2048, temperature: float = 0.2) -> str:
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens, "temperature": temperature, "do_sample": temperature > 0}, "options": {"wait_for_model": True}}
        try:
            resp = self._client.post(f"{HF_API_BASE}/{model}", json=payload)
            resp.raise_for_status()
            result = resp.json()
            if isinstance(result, list):
                return result[0].get("generated_text", "")
            return result.get("generated_text", "")
        except Exception as e:
            logger.error(f"[HuggingFace] TextGen error ({model}): {e}")
            return f"[ERROR] {e}"

    def security_classify(self, text: str) -> Dict[str, Any]:
        return {"raw": self.classify(text, model="jackaduma/SecBERT"), "text": text}

    def close(self):
        self._client.close()
