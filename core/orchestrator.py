"""
🔴💀 MASTER ORCHESTRATOR — Brain of the Ultimate Red Team Arsenal
Accepts user request → plans → routes models → deploys agents → reports
"""
import asyncio
import json
import os
import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class Orchestrator:
    def __init__(self, cost_preference: str = "mid", preferred_model: Optional[str] = None, execution_mode: str = None, on_update: Optional[Callable] = None):
        self.cost_preference = cost_preference
        self.preferred_model = preferred_model
        self.execution_mode = execution_mode or os.getenv("AGENT_EXECUTION_MODE", "docker")
        self.on_update = on_update or self._default_update
        self._router = None
        self._planner = None
        self._selector = None
        from core.hive_mind import HiveMind
        self.hive_mind = HiveMind()
        from core.agent_controller import AgentController
        self.agent_controller = AgentController()
        from core.reasoning_verifier import ReasoningVerifier
        self.verifier = ReasoningVerifier(self._get_router())
        from core.identity_graph import IdentityGraph
        self.identity_graph = IdentityGraph()
        from core.bypass_engine import TwoFABypassEngine
        self.bypass_engine = TwoFABypassEngine()
        from core.exfil_engine import ExfilEngine
        self.exfil_engine = ExfilEngine()
        from core.ato_engine import ATOEngine
        self.ato_engine = ATOEngine()
        from core.mesh_manager import MeshManager
        self.mesh_manager = MeshManager()
        from core.opsec_manager import OPSECManager
        self.opsec_manager = OPSECManager()
        from core.model_hub import ModelHub
        self.model_hub = ModelHub()
        from core.vector_db.hub import IntelligenceHub
        self.intelligence_hub = IntelligenceHub()
        from core.research.hub import ResearchHub
        self.research_hub = ResearchHub()

    def _get_router(self):
        if self._router is None:
            from core.model_router import ModelRouter
            self._router = ModelRouter(cost_preference=self.cost_preference, preferred_model=self.preferred_model)
        return self._router

    def _get_planner(self):
        if self._planner is None:
            from core.task_planner import TaskPlanner
            self._planner = TaskPlanner(model_router=self._get_router())
        return self._planner

    def _get_selector(self):
        if self._selector is None:
            from core.team_selector import TeamSelector
            self._selector = TeamSelector()
        return self._selector

    def run(self, user_request: str, target: Optional[str] = None, session_id: Optional[str] = None, authorized: bool = False) -> Dict[str, Any]:
        """
        Master run loop for the orchestrator.
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        self._emit(f"🚀 Session {session_id} started", "system")
        self._emit(f"📥 Request: {user_request}", "system")

        from core.memory import AgentMemory
        memory = AgentMemory(session_id=session_id)
        memory.set_context("target", target or "Not specified")
        memory.set_context("request", user_request)
        memory.set_context("authorized", authorized)

        # 🛡️ OFFENSIVE GUARDRAILS (Zero-Tolerance Policy)
        if target:
            RESTRICTED_KEYWORDS = [".gov", ".mil", ".edu", "hospital", "police", "fbi", "cia", "localhost", "127.0.0.1"]
            if any(k in target.lower() for k in RESTRICTED_KEYWORDS) and not authorized:
                msg = f"🚫 [SECURITY BLOCK] Target '{target}' is in a restricted category. Execution denied."
                self._emit(msg, "security")
                return {"session_id": session_id, "error": msg, "status": "blocked"}
            
            if not authorized:
                self._emit(f"⚠️ [WARNING] Unauthorized mode: Offensive agents will be disabled.", "security")
            # Plan
            self._emit("🧠 Planning subtasks...", "planner")
            previous_findings = memory.get_findings()
            subtasks = self._get_planner().plan(user_request, memory.get_summary(), previous_findings=previous_findings) or []
            memory.set_subtasks(subtasks)
            self._emit(f"📋 Plan: {len(subtasks)} subtasks", "planner")

            # Select teams
            team_map = self._get_selector().select_for_plan(subtasks)
            self._emit("🎯 Teams assigned", "selector")

            # Execute
            for subtask in subtasks:
                agents = team_map.get(subtask["id"], [])
                memory.update_subtask_status(subtask["id"], "running")
                self._emit(f"⚡ [{subtask['id']}] {subtask['title']} → {agents}", "executor")
                result = self._execute_subtask(subtask, agents, memory, target)
                memory.update_subtask_status(subtask["id"], "done", result)
                subtask["agents_used"] = agents
                self._emit(f"✅ [{subtask['id']}] Complete", "executor")

            # Report
            self._emit("📝 Generating report & remediation patches...", "reporter")
            
            # Autonomous Remediation (Purple Team Protocol)
            from core.remediation_engine import RemediationEngine
            rem_engine = RemediationEngine()
            findings = memory.get_findings()
            repaired_findings = rem_engine.audit_and_repair(findings)
            # Update memory with repaired findings (containing remediation code)
            for rf in repaired_findings:
                memory.update_finding(rf)

            from core.reporter import Reporter
            reporter = Reporter()
            report = reporter.build_report(memory, self._get_router())
            memory.add_artifact("Final Report", f"./reports/report_{session_id}.md", "report")

            # Upload to Cloudflare
            self._emit("☁️ Uploading to Cloudflare R2...", "cloudflare")
            try:
                from integrations.cloudflare_client import CloudflareClient
                cf = CloudflareClient()
                cf.upload_report(session_id, report)
            except Exception as e:
                self._emit(f"⚠️ Cloudflare upload skipped: {e}", "cloudflare")

            self._emit(f"🏁 Session {session_id} COMPLETE", "system")
            return {"session_id": session_id, "report": report, "findings": memory.get_findings(), "knowledge": memory.get_knowledge(), "artifacts": memory.get_all().get("artifacts", []), "subtasks": subtasks}

        except Exception as e:
            logger.exception(f"[Orchestrator] Fatal error: {e}")
            return {"session_id": session_id, "error": str(e), "report": f"# Error\n\n{e}"}

    def _execute_subtask(self, subtask: Dict, agents: List[str], memory, target: Optional[str]) -> str:
        results = []
        for agent_key in agents:
            try:
                result = self._run_agent(agent_key, subtask, memory, target)
                if result:
                    results.append(f"[{agent_key}]: {result}")
                    memory.set_agent_result(agent_key, result)
            except Exception as e:
                logger.error(f"[Orchestrator] Agent {agent_key} error: {e}")
                results.append(f"[{agent_key}]: ERROR — {e}")

        if not results or all("ERROR" in r for r in results):
            self._emit(f"🤖 Using LLM for {subtask.get('task_type')}...", "orchestrator")
            llm_result = self._llm_execute(subtask, memory)
            results.append(f"[LLM]: {llm_result}")

        combined = "\n\n".join(results)
        memory.add_message("assistant", combined, agent="orchestrator")
        return combined

    def _run_agent(self, agent_key: str, subtask: Dict, memory, target: Optional[str]) -> str:
        agent_info = self._get_selector().get_agent_info(agent_key)
        if not agent_info:
            return ""
        execution = agent_info.get("execution", "pip")

        if execution == "internal":
            return self._run_internal_agent(agent_key, subtask, memory, target)
        if execution == "api":
            return self._run_api_agent(agent_key, subtask, memory, target)

        if subtask.get("requires_auth") and not memory.get_context("authorized"):
            self._emit(f"⚠️ {agent_key} requires target authorization — skipping offensive execution", "security")
            return f"[SKIPPED — Target authorization required for {agent_key}. Set authorized=True to enable.]"

        if execution == "docker":
            return self._run_docker_agent(agent_key, agent_info, subtask, target)

        return f"[{agent_key}] execution mode '{execution}' not yet handled"

    def _run_internal_agent(self, agent_key: str, subtask: Dict, memory, target: Optional[str]) -> str:
        if agent_key == "research_agent":
            from knowledge.research_agent import ResearchAgent
            ra = ResearchAgent()
            query = subtask.get("description", subtask.get("title", ""))
            results = ra.search_all(query, max_results=10)
            for r in results[:5]:
                memory.add_knowledge(r)
            return f"Found {len(results)} research items: " + "; ".join(r.get("title", "?")[:60] for r in results[:3])
        return ""

    def _run_api_agent(self, agent_key: str, subtask: Dict, memory, target: Optional[str]) -> str:
        if agent_key == "tavily":
            from integrations.tavily_client import TavilyClient
            tv = TavilyClient()
            query = f"{subtask.get('description', '')} {target or ''}"
            results = tv.search(query)
            return json.dumps(results, indent=2)[:2000]
        if agent_key == "apify":
            from integrations.apify_client import ApifyClient
            ap = ApifyClient()
            return str(ap.run_actor("apify/google-search-scraper", {"queries": subtask.get("description", "")}))
        return ""

    def _run_docker_agent(self, agent_key: str, agent_info: Dict, subtask: Dict, target: Optional[str]) -> str:
        if self.execution_mode != "docker":
            return f"[{agent_key}] execution_mode={self.execution_mode}, Docker not enabled"
        self._emit(f"🐳 Docker agent queued: {agent_key}", "docker")
        return f"[{agent_key}] Docker execution queued. Target: {target or 'N/A'}"

    def _llm_execute(self, subtask: Dict, memory) -> str:
        router = self._get_router()
        messages = [
            {"role": "system", "content": f"You are SUPREME META AGI — expert red team AI. Execute this task with maximum technical accuracy.\n\nSession Context:\n{memory.get_summary()}"},
            {"role": "user", "content": f"Task: {subtask.get('title')}\n\nDescription: {subtask.get('description')}\n\nTarget: {memory.get_context('target')}"},
        ]
        return router.chat(messages, task_type=subtask.get("task_type", "analysis"), max_tokens=4096)

    def _emit(self, message: str, source: str = "system"):
        logger.info(f"[{source.upper()}] {message}")
        if self.on_update:
            self.on_update({"ts": time.time(), "source": source, "message": message})

    def close(self):
        """Cleanup all integration clients."""
        try:
            from integrations.cloudflare_client import CloudflareClient
            from integrations.apify_client import ApifyClient
            from integrations.hyperbrowser_client import HyperbrowserClient
            # These are only closed if they were instantiated (which they are locally in methods currently)
            # Future-proofing: If we move them to self, we close them here.
            logger.info("[Orchestrator] Resource cleanup complete.")
        except Exception as e:
            logger.error(f"[Orchestrator] Cleanup error: {e}")

    @staticmethod
    def _default_update(event: Dict):
        pass
