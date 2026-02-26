"""
🔴💀 Model Catalog — Maps every available Infermatic & HuggingFace model to task types
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModelSpec:
    model_id: str
    provider: str
    context_length: int
    specialties: List[str]
    cost_tier: str
    supports_tools: bool = False
    supports_streaming: bool = True
    description: str = ""


INFERMATIC_MODELS: List[ModelSpec] = [
    ModelSpec("deepseek-r1", "infermatic", 128000, ["reasoning", "planning", "attack_planning", "analysis"], "premium", False, True, "Best reasoning — attack planning"),
    ModelSpec("deepseek-r1-distill-qwen-32b", "infermatic", 128000, ["reasoning", "planning", "exploit_dev"], "mid", False, True, "Fast reasoning distill"),
    ModelSpec("deepseek-v3", "infermatic", 128000, ["reasoning", "code", "analysis"], "premium", True, True, "DeepSeek V3 — tool-use capable"),
    ModelSpec("qwen3-235b-a22b", "infermatic", 128000, ["reasoning", "analysis", "planning", "recon"], "premium", True, True, "Qwen3 235B — massive reasoning powerhouse"),
    ModelSpec("qwen2.5-72b-instruct", "infermatic", 128000, ["analysis", "recon", "report_writing"], "mid", True, True, "Qwen2.5 72B — general purpose"),
    ModelSpec("qwen2.5-coder-32b-instruct", "infermatic", 32768, ["code", "exploit_dev", "script_writing", "payload_gen"], "mid", True, True, "Best open-source coder for exploit writing"),
    ModelSpec("deepseek-coder-v2-instruct", "infermatic", 128000, ["code", "exploit_dev", "reverse_engineering"], "mid", True, True, "DeepSeek Coder V2"),
    ModelSpec("codestral-22b", "infermatic", 32768, ["code", "exploit_dev", "script_writing"], "mid", False, True, "Mistral coder — fast and good"),
    ModelSpec("starcoder2-15b", "infermatic", 16384, ["code", "exploit_dev"], "cheap", False, True, "Star coder — lightweight"),
    ModelSpec("llama-3.1-405b-instruct", "infermatic", 128000, ["analysis", "recon", "osint", "report_writing", "planning"], "premium", True, True, "Llama 405B — best open large model"),
    ModelSpec("llama-3.3-70b-instruct", "infermatic", 128000, ["analysis", "recon", "report_writing"], "mid", True, True, "Llama 70B — workhorse"),
    ModelSpec("llama-3.1-70b-instruct", "infermatic", 128000, ["analysis", "recon"], "mid", True, True, "Llama 3.1 70B"),
    ModelSpec("mixtral-8x22b-instruct", "infermatic", 65536, ["analysis", "recon", "planning"], "mid", True, True, "Mixtral MoE — fast + capable"),
    ModelSpec("mixtral-8x7b-instruct", "infermatic", 32768, ["analysis", "quick_tasks"], "cheap", True, True, "Mixtral small — fast"),
    ModelSpec("gemma-3-27b-it", "infermatic", 128000, ["report_writing", "analysis", "summarization"], "mid", False, True, "Gemma 3 27B — great writer"),
    ModelSpec("phi-4", "infermatic", 16384, ["quick_tasks", "summarization", "report_writing"], "cheap", False, True, "Phi-4 — fast small model"),
    ModelSpec("mistral-nemo-12b", "infermatic", 128000, ["quick_tasks", "recon"], "cheap", True, True, "Mistral Nemo — efficient"),
    ModelSpec("llama-3.1-8b-instruct", "infermatic", 128000, ["quick_tasks", "payload_gen"], "cheap", True, True, "Llama 8B — fast iteration"),
    ModelSpec("nous-hermes-2-mixtral-8x7b", "infermatic", 32768, ["jailbreak", "llm_red_team", "uncensored_analysis"], "mid", False, True, "Nous Hermes — less restricted"),
    ModelSpec("dolphin-2.9-mixtral-8x7b", "infermatic", 32768, ["jailbreak", "llm_red_team", "uncensored_analysis"], "mid", False, True, "Dolphin — uncensored fine-tune"),
    ModelSpec("Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic", "infermatic", 128000, ["analysis", "recon", "report_writing", "reasoning"], "mid", True, True, "Llama 3.3 70B Euryale — Authorized"),
    ModelSpec("Qwen-Qwen3-235B-A22B-Thinking-2507", "infermatic", 128000, ["reasoning", "planning", "analysis"], "premium", True, True, "Qwen3 235B Thinking — Authorized"),
]

HUGGINGFACE_MODELS: List[ModelSpec] = [
    ModelSpec("sentence-transformers/all-mpnet-base-v2", "huggingface", 512, ["embeddings", "semantic_search", "rag"], "cheap", False, False, "Best general embeddings"),
    ModelSpec("BAAI/bge-large-en-v1.5", "huggingface", 512, ["embeddings", "semantic_search", "rag"], "cheap", False, False, "BGE embeddings — SOTA"),
    ModelSpec("intfloat/e5-large-v2", "huggingface", 512, ["embeddings", "semantic_search"], "cheap", False, False, "E5 embeddings"),
    ModelSpec("microsoft/codebert-base", "huggingface", 512, ["code_embeddings", "vulnerability_search"], "cheap", False, False, "Code embeddings"),
    ModelSpec("bigcode/starcoder2-15b", "huggingface", 16384, ["code", "exploit_dev", "vulnerability_analysis"], "mid", False, True, "Code analysis"),
    ModelSpec("distilbert-base-uncased", "huggingface", 512, ["classification", "intent_detection"], "cheap", False, False, "Fast classifier"),
    ModelSpec("dslim/bert-base-NER", "huggingface", 512, ["ner", "entity_extraction", "osint"], "cheap", False, False, "NER — extract IPs, domains, names"),
    ModelSpec("microsoft/Florence-2-large", "huggingface", 4096, ["vision", "screenshot_analysis", "ocr"], "mid", False, False, "Vision model for screenshots"),
    ModelSpec("jackaduma/SecBERT", "huggingface", 512, ["classification", "cve_analysis", "security_ner"], "cheap", False, False, "Security-specific BERT"),
    ModelSpec("CyberSecAI/CyberBERT-CVE", "huggingface", 512, ["cve_analysis", "vulnerability_classification"], "cheap", False, False, "CVE classification model"),
]

TASK_MODEL_MAP = {
    "attack_planning":        ["Qwen-Qwen3-235B-A22B-Thinking-2507", "deepseek-r1", "llama-3.1-405b-instruct"],
    "recon":                  ["llama-3.1-405b-instruct", "mixtral-8x22b-instruct", "qwen2.5-72b-instruct"],
    "osint":                  ["llama-3.1-405b-instruct", "Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic"],
    "exploit_dev":            ["qwen2.5-coder-32b-instruct", "deepseek-coder-v2-instruct", "codestral-22b"],
    "payload_gen":            ["qwen2.5-coder-32b-instruct", "dolphin-2.9-mixtral-8x7b"],
    "code":                   ["qwen2.5-coder-32b-instruct", "deepseek-coder-v2-instruct"],
    "script_writing":         ["qwen2.5-coder-32b-instruct", "codestral-22b"],
    "vulnerability_analysis": ["deepseek-r1", "llama-3.1-405b-instruct"],
    "report_writing":         ["gemma-3-27b-it", "Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic", "phi-4"],
    "summarization":          ["gemma-3-27b-it", "phi-4", "mistral-nemo-12b"],
    "analysis":               ["Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic", "Qwen-Qwen3-235B-A22B-Thinking-2507", "llama-3.1-405b-instruct"],
    "planning":               ["Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic", "Qwen-Qwen3-235B-A22B-Thinking-2507", "deepseek-v3"],
    "llm_red_team":           ["nous-hermes-2-mixtral-8x7b", "dolphin-2.9-mixtral-8x7b"],
    "jailbreak":              ["nous-hermes-2-mixtral-8x7b", "dolphin-2.9-mixtral-8x7b"],
    "quick_tasks":            ["mistral-nemo-12b", "phi-4", "llama-3.1-8b-instruct"],
    "embeddings":             ["sentence-transformers/all-mpnet-base-v2", "BAAI/bge-large-en-v1.5"],
    "semantic_search":        ["BAAI/bge-large-en-v1.5", "intfloat/e5-large-v2"],
    "cve_analysis":           ["jackaduma/SecBERT", "CyberSecAI/CyberBERT-CVE"],
    "research":               ["llama-3.1-405b-instruct", "deepseek-v3"],
    "web_app_attack":         ["deepseek-r1", "qwen2.5-coder-32b-instruct"],
    "network_attack":         ["llama-3.1-405b-instruct", "deepseek-r1"],
    "privesc":                ["deepseek-r1", "qwen2.5-coder-32b-instruct"],
}

ALL_MODELS = INFERMATIC_MODELS + HUGGINGFACE_MODELS
MODEL_INDEX = {m.model_id: m for m in ALL_MODELS}
