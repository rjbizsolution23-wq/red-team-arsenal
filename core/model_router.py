"""
🔴💀 Model Router — Selects the best LLM for each task type
"""
import os
from typing import List, Optional, Tuple
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class ModelRouter:
    def __init__(self, cost_preference: str = "mid", preferred_model: Optional[str] = None):
        self.cost_preference = cost_preference
        self.preferred_model = preferred_model
        self._infermatic = None
        self._hf = None
        self._available_models: Optional[List[str]] = None

    def _get_infermatic(self):
        if self._infermatic is None:
            from models.infermatic_client import get_client
            self._infermatic = get_client()
        return self._infermatic

    def _get_hf(self):
        if self._hf is None:
            from models.hf_client import HuggingFaceClient
            self._hf = HuggingFaceClient()
        return self._hf

    def _get_available(self) -> List[str]:
        if self._available_models is None:
            try:
                self._available_models = self._get_infermatic().list_models()
                logger.info(f"[Router] {len(self._available_models)} models available on Infermatic")
            except Exception:
                from models.model_catalog import INFERMATIC_MODELS
                self._available_models = [m.model_id for m in INFERMATIC_MODELS]
        return self._available_models

    def select_model(self, task_type: str) -> Tuple[str, str]:
        from models.model_catalog import TASK_MODEL_MAP, MODEL_INDEX

        if self.preferred_model:
            spec = MODEL_INDEX.get(self.preferred_model)
            return self.preferred_model, (spec.provider if spec else "infermatic")

        candidates = TASK_MODEL_MAP.get(task_type, TASK_MODEL_MAP.get("analysis", ["Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic"]))
        available = set(self._get_available())

        tier_order = {"cheap": ["cheap"], "mid": ["mid", "cheap"], "premium": ["premium", "mid", "cheap"]}
        allowed_tiers = tier_order.get(self.cost_preference, ["mid", "cheap"])

        for model_id in candidates:
            spec = MODEL_INDEX.get(model_id)
            if spec is None:
                continue
            if spec.provider == "huggingface":
                return model_id, "huggingface"
            if model_id in available and spec.cost_tier in allowed_tiers:
                return model_id, spec.provider

        for model_id in candidates:
            spec = MODEL_INDEX.get(model_id)
            if spec and model_id in available:
                return model_id, spec.provider if spec else "infermatic"

        return "Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic", "infermatic"

    def chat(self, messages: list, task_type: str = "analysis", temperature: float = 0.7, max_tokens: int = 4096, stream: bool = False, tools: Optional[list] = None):
        model_id, provider = self.select_model(task_type)
        logger.info(f"[Router] {task_type} → {model_id} ({provider})")

        if provider == "infermatic":
            return self._get_infermatic().chat(messages=messages, model=model_id, temperature=temperature, max_tokens=max_tokens, stream=stream, tools=tools)
        elif provider == "huggingface":
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
            return self._get_hf().text_generation(prompt, model=model_id)
        else:
            return self._get_infermatic().chat(messages=messages, model=model_id)

    def embed(self, texts, model: Optional[str] = None):
        m = model or "sentence-transformers/all-mpnet-base-v2"
        return self._get_hf().embed(texts, model=m)
