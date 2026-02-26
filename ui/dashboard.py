"""
🔴💀 The Citadel — Command & Control Dashboard API
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import time

app = FastAPI(title="🔴💀 Arsenal - The Citadel")

# Simulation: Persistent Mission State
MISSIONS = [
    {"id": "0c8e2550", "target": "identity-trial.local", "status": "COMPLETED", "agents": ["identity_agent", "bypass_engine"]},
    {"id": "417df990", "target": "store.local", "status": "ACTIVE", "agents": ["db_agent", "webapp_agent"]}
]

@app.get("/api/missions")
def get_missions():
    return MISSIONS

@app.get("/api/logs")
def get_logs():
    return [
        {"timestamp": time.time(), "level": "INFO", "msg": "[Orchestrator] Launching Session 417df990"},
        {"timestamp": time.time() + 1, "level": "SUCCESS", "msg": "[DBAgent] SQLi success on store.local"}
    ]

# Serve static dashboard UI
app.mount("/", StaticFiles(directory="ui/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
