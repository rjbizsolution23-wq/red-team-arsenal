"""
🔴💀 Apify Client — Elite Web Scraping & Recon
"""
import os
import httpx
from typing import Dict, Any, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY", "")

class ApifyClient:
    def __init__(self):
        self._key = APIFY_API_KEY
        self._base = "https://api.apify.com/v2"
        self._headers = {"Authorization": f"Bearer {self._key}"}
        self._client = httpx.Client(headers=self._headers, timeout=60)

    def run_actor(self, actor_id: str, input_data: Dict[str, Any]) -> Optional[Dict]:
        """Run an Apify actor and wait for completion."""
        try:
            # URL encode actor_id because it might contain slashes like 'apify/google-search-scraper'
            encoded_id = actor_id.replace("/", "~")
            url = f"{self._base}/acts/{encoded_id}/runs"
            resp = self._client.post(url, json=input_data)
            resp.raise_for_status()
            run_data = resp.json()["data"]
            run_id = run_data["id"]
            
            logger.info(f"[Apify] Actor {actor_id} started. Run ID: {run_id}")
            return run_data
        except Exception as e:
            logger.error(f"[Apify] Actor run failed: {e}")
            return None

    def get_dataset(self, dataset_id: str) -> list:
        """Retrieve results from an Apify dataset."""
        try:
            url = f"{self._base}/datasets/{dataset_id}/items"
            resp = self._client.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"[Apify] Dataset retrieval failed: {e}")
            return []
            
    def close(self):
        self._client.close()
