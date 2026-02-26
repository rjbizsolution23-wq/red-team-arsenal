"""Tavily + Apify integration clients"""
import os, time
from typing import Dict, List, Optional
import httpx
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
APIFY_API_KEY = os.getenv("APIFY_API_KEY", "")

class TavilyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or TAVILY_API_KEY
        self._client = httpx.Client(timeout=30)

    def search(self, query: str, max_results: int = 10, search_depth: str = "advanced") -> List[Dict]:
        try:
            resp = self._client.post("https://api.tavily.com/search", json={"api_key": self.api_key, "query": query, "max_results": max_results, "search_depth": search_depth, "include_answer": True})
            resp.raise_for_status()
            results = resp.json().get("results", [])
            logger.info(f"[Tavily] {len(results)} results for '{query}'")
            return results
        except Exception as e:
            logger.error(f"[Tavily] {e}"); return []

    def search_security(self, target: str, topic: str = "vulnerabilities") -> List[Dict]:
        return self.search(f"{target} {topic} CVE exploit")

    def close(self):
        self._client.close()

class ApifyClientWrapper:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or APIFY_API_KEY
        self._base = "https://api.apify.com/v2"
        self._client = httpx.Client(timeout=60)

    def run_actor(self, actor_id: str, input_data: Dict, wait_secs: int = 60) -> Dict:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            resp = self._client.post(f"{self._base}/acts/{actor_id}/runs", json={"input": input_data}, headers=headers)
            resp.raise_for_status()
            run_id = resp.json()["data"]["id"]
            for _ in range(wait_secs // 5):
                time.sleep(5)
                status = self._client.get(f"{self._base}/actor-runs/{run_id}", headers=headers).json()["data"]["status"]
                if status in ("SUCCEEDED", "FAILED", "ABORTED"):
                    break
            return self._client.get(f"{self._base}/actor-runs/{run_id}/dataset/items", headers=headers).json()
        except Exception as e:
            logger.error(f"[Apify] {e}"); return {}

    def search(self, query: str) -> str:
        return str(self.run_actor("apify/google-search-scraper", {"queries": query, "maxPagesPerQuery": 1}))[:2000]

    def close(self):
        self._client.close()
