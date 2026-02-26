"""
🔴💀 Infermatic Client — OpenAI-compatible client for api.totalgpt.ai
Supports: chat completions, streaming, function/tool calling, embeddings
"""
import os
import json
from typing import Any, Dict, Generator, List, Optional, Union
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

INFERMATIC_API_KEY = os.getenv("INFERMATIC_API_KEY", "")
INFERMATIC_API_URL = os.getenv("INFERMATIC_API_URL", "https://api.totalgpt.ai/v1")
CHUTES_API_KEY = os.getenv("CHUTES_API_KEY", "")
CHUTES_API_URL = "https://llm.chutes.ai/v1"


class InfermaticClient:
    """
    OpenAI-compatible client for Infermatic (totalgpt.ai).
    Falls back to Chutes AI if Infermatic fails.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 300,
        use_fallback: bool = True,
    ):
        self.api_key = api_key or INFERMATIC_API_KEY
        self.base_url = (base_url or INFERMATIC_API_URL).rstrip("/")
        self.timeout = timeout
        self.use_fallback = use_fallback
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
        self._async_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    # ──────────────────────────────────────────────────────────
    # Chat Completion (sync)
    # ──────────────────────────────────────────────────────────

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "Sao10K-L3.3-70B-Euryale-v2.3-FP8-Dynamic",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        stream: bool = False,
        **kwargs,
    ) -> Union[str, Generator]:
        """Send a chat completion request."""
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice
        payload.update(kwargs)

        if stream:
            return self._stream_chat(payload)
        return self._sync_chat(payload)

    def _sync_chat(self, payload: Dict) -> str:
        try:
            resp = self._client.post(
                f"{self.base_url}/chat/completions", json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"[Infermatic] Chat error: {e}")
            if self.use_fallback:
                return self._chutes_fallback(payload)
            raise

    def _stream_chat(self, payload: Dict) -> Generator[str, None, None]:
        """Yield text chunks as they stream."""
        try:
            with self._client.stream(
                "POST", f"{self.base_url}/chat/completions", json=payload
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk == "[DONE]":
                            break
                        try:
                            data = json.loads(chunk)
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            continue
        except Exception as e:
            logger.error(f"[Infermatic] Stream error: {e}")
            if self.use_fallback:
                yield self._chutes_fallback(payload)
            else:
                raise

    # ──────────────────────────────────────────────────────────
    # Chat with Tools / Function Calling
    # ──────────────────────────────────────────────────────────

    def chat_with_tools(
        self,
        messages: List[Dict],
        tools: List[Dict],
        model: str = "deepseek-v3",
        max_iterations: int = 10,
        tool_executor=None,
    ) -> str:
        """Agentic loop: chat + auto-execute tool calls until done."""
        iteration = 0
        current_messages = list(messages)

        while iteration < max_iterations:
            payload = {
                "model": model,
                "messages": current_messages,
                "tools": tools,
                "tool_choice": "auto",
                "stream": False,
            }
            try:
                resp = self._client.post(
                    f"{self.base_url}/chat/completions", json=payload
                )
                resp.raise_for_status()
                data = resp.json()
                choice = data["choices"][0]
                msg = choice["message"]
                current_messages.append(msg)

                if choice["finish_reason"] == "stop" or not msg.get("tool_calls"):
                    return msg.get("content", "")

                # Execute tool calls
                if tool_executor and msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        fn_name = tc["function"]["name"]
                        fn_args = json.loads(tc["function"]["arguments"])
                        logger.info(f"[Infermatic] Tool call: {fn_name}({fn_args})")
                        result = tool_executor(fn_name, fn_args)
                        current_messages.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": str(result),
                        })

            except Exception as e:
                logger.error(f"[Infermatic] Tool loop error: {e}")
                break
            iteration += 1

        return current_messages[-1].get("content", "Max iterations reached")

    # ──────────────────────────────────────────────────────────
    # Async Chat
    # ──────────────────────────────────────────────────────────

    async def achat(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.3-70b-instruct",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }
        try:
            resp = await self._async_client.post(
                f"{self.base_url}/chat/completions", json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"[Infermatic] Async chat error: {e}")
            raise

    # ──────────────────────────────────────────────────────────
    # List Available Models
    # ──────────────────────────────────────────────────────────

    def list_models(self) -> List[str]:
        try:
            resp = self._client.get(f"{self.base_url}/models")
            resp.raise_for_status()
            data = resp.json()
            return [m["id"] for m in data.get("data", [])]
        except Exception as e:
            logger.error(f"[Infermatic] list_models error: {e}")
            return []

    # ──────────────────────────────────────────────────────────
    # Chutes AI Fallback
    # ──────────────────────────────────────────────────────────

    def _chutes_fallback(self, payload: Dict) -> str:
        """Fall back to Chutes AI with same OpenAI-compatible payload."""
        logger.warning("[Infermatic] Falling back to Chutes AI...")
        
        # Adjust model for Chutes if necessary
        original_model = payload.get("model", "")
        # Safe fallback model on Chutes
        payload["model"] = "unsloth/Llama-3.2-3B-Instruct"
        
        try:
            resp = httpx.post(
                f"{CHUTES_API_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {CHUTES_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=300,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"[Chutes] Fallback also failed: {e}")
            return f"[ERROR] Both Infermatic and Chutes failed: {e}"

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# Singleton instance for convenience
_default_client: Optional[InfermaticClient] = None


def get_client() -> InfermaticClient:
    global _default_client
    if _default_client is None:
        _default_client = InfermaticClient()
    return _default_client
