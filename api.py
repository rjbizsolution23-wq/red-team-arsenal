"""
🔴💀 FastAPI Server — REST API + WebSocket for the Red Team Dashboard
"""
import asyncio
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="🔴💀 Ultimate Autonomous Red Team Arsenal API",
    description="Autonomous multi-agent red team system — powered by Infermatic AI + HuggingFace + Cloudflare",
    version="1.0.0",
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Active WebSocket connections
_connections: Dict[str, WebSocket] = {}
# Session results store
_sessions: Dict[str, Any] = {}


class TaskRequest(BaseModel):
    request: str
    target: Optional[str] = None
    cost_preference: str = "mid"   # "cheap" | "mid" | "premium"
    preferred_model: Optional[str] = None
    authorized: bool = False        # User confirms they own/have permission on target


class TaskResponse(BaseModel):
    session_id: str
    status: str
    message: str


# ──────────────────────────────────────────────────────────────────────────────
# REST Endpoints
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "🔴💀 Red Team Arsenal ONLINE", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time()}


@app.get("/models")
def list_models():
    """List all available models."""
    from models.infermatic_client import get_client
    from models.model_catalog import ALL_MODELS
    try:
        live = get_client().list_models()
    except Exception:
        live = []
    return {
        "infermatic_live": live,
        "catalog": [
            {"id": m.model_id, "provider": m.provider, "specialties": m.specialties, "cost_tier": m.cost_tier}
            for m in ALL_MODELS
        ],
    }


@app.get("/agents")
def list_agents():
    """List all available red team agents."""
    from core.team_selector import TeamSelector
    return TeamSelector().get_all_agents()


@app.post("/task", response_model=TaskResponse)
async def submit_task(req: TaskRequest, background_tasks: BackgroundTasks):
    """Submit a red team task for autonomous execution."""
    session_id = str(uuid.uuid4())[:8]
    _sessions[session_id] = {"status": "running", "result": None}

    async def run_task():
        try:
            from core.orchestrator import Orchestrator

            def on_update(event):
                """Push updates to WebSocket clients."""
                asyncio.create_task(_broadcast(session_id, event))

            orc = Orchestrator(
                cost_preference=req.cost_preference,
                preferred_model=req.preferred_model,
                on_update=on_update,
            )

            # Set authorization flag in memory
            from core.memory import AgentMemory
            mem = AgentMemory(session_id=session_id)
            mem.set_context("authorized", req.authorized)
            
            result = await asyncio.to_thread(orc.run, req.request, req.target, session_id=session_id)
            _sessions[session_id] = {"status": "done", "result": result}
            await _broadcast(session_id, {"source": "system", "message": "✅ Task complete", "ts": time.time()})
        except Exception as e:
            logger.exception(f"[API] Task error: {e}")
            _sessions[session_id] = {"status": "error", "result": str(e)}

    background_tasks.add_task(run_task)
    return TaskResponse(session_id=session_id, status="running", message="Task started. Connect WebSocket for live updates.")


@app.get("/session/{session_id}")
def get_session(session_id: str):
    """Poll for session results."""
    if session_id not in _sessions:
        raise HTTPException(404, "Session not found")
    return _sessions[session_id]


@app.get("/sessions")
def list_sessions():
    return {sid: {"status": s["status"]} for sid, s in _sessions.items()}


@app.post("/research")
async def research(query: str, max_results: int = 20):
    """Direct research agent query."""
    from knowledge.research_agent import ResearchAgent
    ra = ResearchAgent()
    results = await asyncio.to_thread(ra.search_all, query, max_results)
    return {"query": query, "results": results}


@app.get("/reports")
def list_reports():
    """List reports from Cloudflare R2."""
    from integrations.cloudflare_client import CloudflareClient
    cf = CloudflareClient()
    return {"reports": cf.list_reports()}


@app.get("/report/{session_id}")
def get_report(session_id: str):
    """Fetch a specific report from Cloudflare R2."""
    from integrations.cloudflare_client import CloudflareClient
    cf = CloudflareClient()
    report = cf.download_report(session_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return {"session_id": session_id, "report": report}


# ──────────────────────────────────────────────────────────────────────────────
# WebSocket — Live Agent Feed
# ──────────────────────────────────────────────────────────────────────────────

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for live task updates."""
    await websocket.accept()
    _connections[session_id] = websocket
    logger.info(f"[WebSocket] Client connected: {session_id}")
    try:
        while True:
            # Keep connection alive, wait for server-push events
            await asyncio.sleep(0.5)
            # Check if session is done
            session = _sessions.get(session_id, {})
            if session.get("status") in ("done", "error"):
                await websocket.send_json({"type": "complete", "session": session})
                break
    except WebSocketDisconnect:
        pass
    finally:
        _connections.pop(session_id, None)
        logger.info(f"[WebSocket] Client disconnected: {session_id}")


async def _broadcast(session_id: str, event: Dict):
    """Send an event to the connected WebSocket client for a session."""
    ws = _connections.get(session_id)
    if ws:
        try:
            await ws.send_json(event)
        except Exception:
            pass


if __name__ == "__main__":
    import os
    port = int(os.getenv("API_PORT", 8888))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True, log_level="info")
