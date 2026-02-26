"""
Task Planner — Breaks a user request into structured subtasks
"""
import json, re
from typing import Any, Dict, List, Optional
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

PLANNING_SYSTEM_PROMPT = """You are SUPREME META AGI, master planner for the Ultimate Autonomous Red Team Arsenal.
Decompose the user request into a structured list of subtasks as JSON array.
Each subtask must have: id (int), title (str), description (str), task_type (str from: attack_planning,recon,osint,exploit_dev,payload_gen,code,script_writing,vulnerability_analysis,report_writing,llm_red_team,jailbreak,web_app_attack,network_attack,privesc,research,analysis,quick_tasks), required_tools (list), requires_auth (bool), depends_on (list of ids).
Return ONLY valid JSON array, no markdown."""

class TaskPlanner:
    def __init__(self, model_router=None):
        self._router = model_router

    def _get_router(self):
        if self._router is None:
            from core.model_router import ModelRouter
            self._router = ModelRouter(cost_preference="mid")
        return self._router

    def plan(self, user_request: str, context: str = "", previous_findings: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        findings_ctx = ""
        if previous_findings:
            findings_ctx = "\n\n### PREVIOUS FINDINGS (RECURSIVE CONTEXT):\n" + json.dumps(previous_findings, indent=2)
            findings_ctx += "\nAnalyze the findings above. If an objective (like Domain Admin) wasn't reached, suggest the NEXT MOST LOGICAL attack path. Avoid repeating failed tools."

        messages = [
            {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
            {"role": "user", "content": f"User Request:\n{user_request}\n\nContext:\n{context or 'None'}{findings_ctx}"},
        ]
        try:
            response = self._get_router().chat(messages=messages, task_type="planning", temperature=0.3, max_tokens=4096)
            logger.debug(f"[Planner] Raw response: {response[:200]}...")
            subtasks = self._parse_subtasks(response)
            logger.info(f"[Planner] {len(subtasks)} subtasks")
            for i, st in enumerate(subtasks):
                st["status"] = "pending"
                st.setdefault("id", i)
            return subtasks
        except Exception as e:
            logger.error(f"[Planner] Error: {e}")
            return self._fallback_plan(user_request)

    def _parse_subtasks(self, response: str) -> List[Dict]:
        # Remove thinking blocks if present
        cleaned = re.sub(r"<thought>.*?</thought>", "", response, flags=re.DOTALL)
        # Remove other common thought markers
        cleaned = re.sub(r"thought:.*?\n", "", cleaned, flags=re.IGNORECASE)
        # Remove markdown code blocks
        cleaned = re.sub(r"```(?:json)?", "", cleaned).strip().rstrip("`").strip()
        
        try:
            result = json.loads(cleaned)
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and "subtasks" in result:
                return result["subtasks"]
        except json.JSONDecodeError:
            # Try to find anything between the first [ and last ]
            match = re.search(r'(\[.*\])', cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
        return []

    def _fallback_plan(self, request: str) -> List[Dict]:
        return [
            {"id": 0, "title": "Research & Analysis", "description": f"Research: {request}", "task_type": "research", "required_tools": ["research_agent", "tavily"], "requires_auth": False, "depends_on": [], "status": "pending"},
            {"id": 1, "title": "Execute & Report", "description": "Execute and generate report", "task_type": "report_writing", "required_tools": [], "requires_auth": False, "depends_on": [0], "status": "pending"},
        ]
