"""Research Agent — multi-source academic knowledge retrieval"""
import os
from typing import Dict, List, Optional
import httpx
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_API_KEY", "")
PWC_TOKEN = os.getenv("PAPERSWITHCODE_TOKEN", "")

class ResearchAgent:
    def __init__(self):
        self._client = httpx.Client(timeout=30)

    def search_all(self, query: str, max_results: int = 20) -> List[Dict]:
        results = []
        for fn in [self.search_arxiv, self.search_semantic_scholar, self.search_papers_with_code, self.search_tavily]:
            try:
                results += fn(query, max_results // 4)
            except Exception as e:
                logger.warning(f"[Research] {fn.__name__} failed: {e}")
        logger.info(f"[Research] {len(results)} items for '{query}'")
        return results

    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            import feedparser
            resp = self._client.get("http://export.arxiv.org/api/query", params={"search_query": f"all:{query}", "start": 0, "max_results": max_results, "sortBy": "submittedDate", "sortOrder": "descending"})
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)
            return [{"source": "arxiv", "title": e.get("title","").replace("\n"," ").strip(), "summary": e.get("summary","")[:500], "url": e.get("id",""), "published": e.get("published","")[:10]} for e in feed.entries]
        except Exception as e:
            logger.error(f"[Research/arXiv] {e}"); return []

    def search_semantic_scholar(self, query: str, limit: int = 10) -> List[Dict]:
        try:
            resp = self._client.get("https://api.semanticscholar.org/graph/v1/paper/search", params={"query": query, "limit": min(limit, 100), "fields": "title,abstract,authors,year,citationCount,url"})
            resp.raise_for_status()
            return [{"source": "semantic_scholar", "title": p.get("title",""), "summary": p.get("abstract","")[:500], "url": p.get("url",""), "year": p.get("year")} for p in resp.json().get("data",[])]
        except Exception as e:
            logger.error(f"[Research/SS] {e}"); return []

    def search_papers_with_code(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            headers = {"Authorization": f"Token {PWC_TOKEN}"} if PWC_TOKEN else {}
            resp = self._client.get("https://paperswithcode.com/api/v1/papers/", params={"q": query, "items_per_page": min(max_results, 50)}, headers=headers)
            resp.raise_for_status()
            return [{"source": "papers_with_code", "title": p.get("title",""), "summary": p.get("abstract","")[:500], "url": p.get("url_abs","")} for p in resp.json().get("results",[])]
        except Exception as e:
            logger.error(f"[Research/PWC] {e}"); return []

    def search_tavily(self, query: str, max_results: int = 5) -> List[Dict]:
        if not TAVILY_KEY:
            return []
        try:
            resp = self._client.post("https://api.tavily.com/search", json={"api_key": TAVILY_KEY, "query": query, "max_results": max_results, "search_depth": "advanced"})
            resp.raise_for_status()
            return [{"source": "tavily", "title": r.get("title",""), "summary": r.get("content","")[:500], "url": r.get("url","")} for r in resp.json().get("results",[])]
        except Exception as e:
            logger.error(f"[Research/Tavily] {e}"); return []

    def close(self):
        self._client.close()
