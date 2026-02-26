"""
🔴💀 ULTIMATE AUTONOMOUS RED TEAM ARSENAL
Memory module — Enhanced with SQLite + JSON Dual Layer
"""
import json
import time
import sqlite3
import threading
from typing import Any, Dict, List, Optional
from pathlib import Path
from loguru import logger


class AgentMemory:
    """Thread-safe shared memory context with SQLite + JSON persistence."""

    def __init__(self, session_id: str, db_path: str = "./sessions/red_team.db"):
        self.session_id = session_id
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        
        # Local cache for fast access
        self._store: Dict[str, Any] = {
            "session_id": session_id,
            "created_at": time.time(),
            "messages": [],
            "findings": [],
            "artifacts": [],
            "knowledge": [],
            "subtasks": [],
            "agent_results": {},
            "context": {},
        }
        
        self._init_db()
        self._load_session()

    def _init_db(self):
        """Initialize SQLite tables if they don't exist."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        data JSON,
                        updated_at REAL
                    )
                """)
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"[Memory] DB Init Error: {e}")

    # ──────────────────────────────────────────────────────────
    # Core R/W operations
    # ──────────────────────────────────────────────────────────

    def add_message(self, role: str, content: str, agent: Optional[str] = None):
        with self._lock:
            entry = {"ts": time.time(), "role": role, "content": content, "agent": agent}
            self._store["messages"].append(entry)
            self._save()

    def add_finding(self, finding: Dict[str, Any]):
        with self._lock:
            finding["ts"] = time.time()
            self._store["findings"].append(finding)
            self._save()
            logger.info(f"[Memory] New finding: {finding.get('title', 'Untitled')}")

    def add_artifact(self, name: str, path: str, artifact_type: str = "file"):
        with self._lock:
            self._store["artifacts"].append({
                "ts": time.time(), "name": name, "path": path, "type": artifact_type
            })
            self._save()

    def add_knowledge(self, item: Dict[str, Any]):
        with self._lock:
            item["ts"] = time.time()
            self._store["knowledge"].append(item)
            self._save()

    def set_subtasks(self, subtasks: List[Dict]):
        with self._lock:
            self._store["subtasks"] = subtasks
            self._save()

    def update_subtask_status(self, subtask_id: int, status: str, result: Any = None):
        with self._lock:
            for st in self._store["subtasks"]:
                if st.get("id") == subtask_id:
                    st["status"] = status
                    if result is not None:
                        st["result"] = result
                    break
            self._save()

    def set_agent_result(self, agent_name: str, result: Any):
        with self._lock:
            self._store["agent_results"][agent_name] = {"ts": time.time(), "result": result}
            self._save()

    def set_context(self, key: str, value: Any):
        with self._lock:
            self._store["context"][key] = value
            self._save()

    def get_context(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._store["context"].get(key, default)

    def get_findings(self) -> List[Dict]:
        with self._lock:
            return list(self._store["findings"])

    def get_knowledge(self) -> List[Dict]:
        with self._lock:
            return list(self._store["knowledge"])

    def get_messages(self) -> List[Dict]:
        with self._lock:
            return list(self._store["messages"])

    def get_all(self) -> Dict:
        with self._lock:
            return dict(self._store)

    def get_summary(self) -> str:
        with self._lock:
            lines = [
                f"Session: {self.session_id}",
                f"Status: {sum(1 for t in self._store['subtasks'] if t.get('status')=='done')}/{len(self._store['subtasks'])} tasks done",
                f"Findings: {len(self._store['findings'])}",
                f"Knowledge: {len(self._store['knowledge'])}",
            ]
            if self._store["findings"]:
                lines.append("\nKey Findings:")
                for f in self._store["findings"][-3:]:
                    lines.append(f"  - [{f.get('severity','?')}] {f.get('title','?')}")
            return "\n".join(lines)

    # ──────────────────────────────────────────────────────────
    # Persistence (SQLite)
    # ──────────────────────────────────────────────────────────

    def _save(self):
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                data_json = json.dumps(self._store, default=str)
                cursor.execute(
                    "INSERT OR REPLACE INTO sessions (session_id, data, updated_at) VALUES (?, ?, ?)",
                    (self.session_id, data_json, time.time())
                )
                conn.commit()
                conn.close()
                
                # Bonus: save a readable JSON for debugging
                json_path = self.db_path.parent / f"{self.session_id}.json"
                with open(json_path, "w") as f:
                    f.write(data_json)
            except Exception as e:
                logger.error(f"[Memory] Save Error: {e}")

    def _load_session(self):
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM sessions WHERE session_id = ?", (self.session_id,))
                row = cursor.fetchone()
                if row:
                    self._store = json.loads(row[0])
                    logger.info(f"[Memory] Restored session {self.session_id} from DB")
                conn.close()
            except Exception as e:
                logger.warning(f"[Memory] Restore Error: {e}")
