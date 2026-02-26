"""
🔴💀 Hyperbrowser Client — Headless Browser Automation
"""
import os
import httpx
from typing import Dict, Any, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

HYPERBROWSER_API_KEY = os.getenv("HYPERBROWSER_API_KEY", "")

class HyperbrowserClient:
    def __init__(self):
        self._key = HYPERBROWSER_API_KEY
        self._base = "https://api.hyperbrowser.io/v1" # Hypothetical production endpoint
        self._headers = {"Authorization": f"Bearer {self._key}", "Content-Type": "application/json"}
        self._client = httpx.Client(headers=self._headers, timeout=60)

    def launch_session(self, url: str, options: Optional[Dict] = None) -> Optional[Dict]:
        """Launch a headless browser session to a target URL."""
        try:
            payload = {"url": url, "options": options or {}}
            resp = self._client.post(f"{self._base}/sessions", json=payload)
            resp.raise_for_status()
            session = resp.json()
            logger.info(f"[Hyperbrowser] Launched session for: {url}")
            return session
        except Exception as e:
            logger.error(f"[Hyperbrowser] Session launch failed: {e}")
            return None

    def capture_screenshot(self, session_id: str) -> Optional[str]:
        """Capture a screenshot from an active session."""
        try:
            resp = self._client.post(f"{self._base}/sessions/{session_id}/screenshot")
            resp.raise_for_status()
            return resp.json().get("image_url")
        except Exception as e:
            logger.error(f"[Hyperbrowser] Screenshot failed: {e}")
            return None

    def close(self):
        self._client.close()
