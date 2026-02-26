"""
🔴💀 Team Selector — Picks the right red team agents for each subtask
"""
from typing import Dict, List, Optional
from loguru import logger

AGENT_REGISTRY: Dict[str, Dict] = {
    "pentagi":       {"name": "PentAGI", "tier": 1, "task_types": ["attack_planning", "recon", "exploit_dev", "vulnerability_analysis", "network_attack"], "description": "Full autonomous pentest AGI — Docker multi-agent", "execution": "docker", "autonomy": 5},
    "cai":           {"name": "CAI", "tier": 1, "task_types": ["web_app_attack", "exploit_dev", "recon", "vulnerability_analysis", "payload_gen"], "description": "Battle-proven — 3600% over human pentesters", "execution": "pip", "autonomy": 5},
    "aracne":        {"name": "ARACNE", "tier": 1, "task_types": ["network_attack", "exploit_dev", "privesc"], "description": "100% autonomous SSH attack chains", "execution": "pip", "autonomy": 5},
    "strix":         {"name": "Strix", "tier": 1, "task_types": ["web_app_attack", "vulnerability_analysis", "exploit_dev"], "description": "Agents that act like hackers", "execution": "pip", "autonomy": 5},
    "cyber_autoagent":{"name": "Cyber-AutoAgent", "tier": 1, "task_types": ["web_app_attack", "vulnerability_analysis"], "description": "85% XBOW benchmark score", "execution": "pip", "autonomy": 4},
    "polyglot_coder": {"name": "Master Polyglot Coder", "tier": 0, "task_types": ["code_gen", "architect"], "description": "Layer 0-7 production engine", "execution": "pip", "autonomy": 5},
    "red_team_supreme": {"name": "Supreme Red Team", "tier": 0, "task_types": ["analysis", "exploit_dev"], "description": "Adversarial ML & Compliance specialist", "execution": "pip", "autonomy": 5},
    "binary_specialist": {"name": "Binary Overlord", "tier": 0, "task_types": ["exploit_dev", "privesc", "stealth"], "description": "Expert in binary deployment and evasion", "execution": "pip", "autonomy": 5},
    "academic_agent": {"name": "Academic Architect", "tier": 0, "task_types": ["analysis", "research"], "description": "Expert in paper scraping and TTP extraction", "execution": "pip", "autonomy": 5},
    "exploit_master": {"name": "Exploit Master", "tier": 0, "task_types": ["exploit_dev", "network_attack"], "description": "Expert in automated Metasploit/Nuclei chains", "execution": "pip", "autonomy": 5},
    "vanguard_agent": {"name": "Vanguard Agent", "tier": 0, "task_types": ["privesc", "lateral_movement"], "description": "Expert in BloodHound and AD Domination", "execution": "pip", "autonomy": 5},
    "recon_master":   {"name": "Recon Master", "tier": 0, "task_types": ["recon", "osint"], "description": "Expert in full-spectrum OSINT and mapping", "execution": "pip", "autonomy": 5},
    "boxpwnr":       {"name": "BoxPwnr", "tier": 2, "task_types": ["ctf", "exploit_dev", "privesc", "vulnerability_analysis"], "description": "Autonomous HackTheBox solver", "execution": "pip", "autonomy": 4},
    "cleaner_agent": {"name": "The Cleaner", "tier": 0, "task_types": ["stealth", "analysis"], "description": "Expert in anti-forensics and log erasure", "execution": "pip", "autonomy": 5},
    "vulnbot":       {"name": "VulnBot", "tier": 2, "task_types": ["vulnerability_analysis", "exploit_dev", "recon"], "description": "Multi-agent vulnerability exploitation", "execution": "pip", "autonomy": 4},
    "hackingbuddy":  {"name": "hackingBuddyGPT", "tier": 2, "task_types": ["privesc", "exploit_dev"], "description": "Autonomous Linux privilege escalation", "execution": "pip", "autonomy": 4},
    "ghostcrew":     {"name": "GhostCrew", "tier": 2, "task_types": ["recon", "exploit_dev", "attack_planning"], "description": "Multi-agent ghost red team crew", "execution": "pip", "autonomy": 4},
    "redamon":       {"name": "Redamon", "tier": 2, "task_types": ["recon", "attack_planning", "vulnerability_analysis"], "description": "Real-time red team monitoring + execution", "execution": "pip", "autonomy": 4},
    "pentestgpt":    {"name": "PentestGPT", "tier": 2, "task_types": ["attack_planning", "vulnerability_analysis", "recon"], "description": "USENIX Security 2024 guided pentesting", "execution": "pip", "autonomy": 3},
    "agenticred":    {"name": "AgenticRed", "tier": 2, "task_types": ["network_attack", "exploit_dev", "attack_planning"], "description": "Multi-stage agentic red teaming", "execution": "pip", "autonomy": 4},
    "neurosploit":   {"name": "NeuroSploit", "tier": 2, "task_types": ["exploit_dev", "payload_gen"], "description": "Neural network-powered exploit framework", "execution": "pip", "autonomy": 3},
    "pyrit":         {"name": "PyRIT (Microsoft)", "tier": 3, "task_types": ["llm_red_team", "jailbreak", "ai_security"], "description": "Microsoft AI red teaming framework", "execution": "pip", "autonomy": 3},
    "agentic_radar": {"name": "Agentic Radar", "tier": 3, "task_types": ["llm_red_team", "ai_security", "vulnerability_analysis"], "description": "AI agent vulnerability scanner", "execution": "pip", "autonomy": 3},
    "research_agent":{"name": "Research Agent", "tier": 0, "task_types": ["research", "osint", "recon", "analysis"], "description": "Academic knowledge retrieval — arXiv/SemanticScholar/OpenAlex/PWC", "execution": "internal", "autonomy": 5},
    "tavily":        {"name": "Tavily Search", "tier": 0, "task_types": ["recon", "osint", "research", "quick_tasks"], "description": "Real-time AI web search", "execution": "api", "autonomy": 5},
    "apify":         {"name": "Apify Scraper", "tier": 0, "task_types": ["recon", "osint", "data_collection"], "description": "Web scraping at scale", "execution": "api", "autonomy": 4},
    "auto_exploiter": {"name": "Infinite Exploiter", "tier": 0, "task_types": ["exploit_dev", "vulnerability_analysis", "network_attack"], "description": "High-speed reactive exploit chain-firing (HiveMind)", "execution": "pip", "autonomy": 5},
    "brute_agent":   {"name": "Brute Force Orchestrator", "tier": 0, "task_types": ["network_attack", "privesc"], "description": "Automated Hydra/Hashcat/John with custom wordlists", "execution": "pip", "autonomy": 5},
    "credential_agent":{"name": "Credential Master", "tier": 0, "task_types": ["privesc", "exploit_dev", "osint"], "description": "Expert in Mimikatz, Rubeus, and Cloud Harvesting", "execution": "pip", "autonomy": 5},
    "crypto_agent":  {"name": "Crypto Heist Specialist", "tier": 0, "task_types": ["network_attack", "financial_attack", "blockchain"], "description": "Expert in wallet recovery and smart contract exploits", "execution": "pip", "autonomy": 5},
    "db_agent":      {"name": "SQL & DB Overlord", "tier": 0, "task_types": ["vulnerability_analysis", "database_attack", "network_attack"], "description": "Expert in autonomous SQLi and mass data dumping", "execution": "pip", "autonomy": 5},
    "evasion_agent": {"name": "Evasion Specialist", "tier": 0, "task_types": ["exploit_dev", "stealth"], "description": "Expert in multi-layered AV/EDR bypass techniques", "execution": "pip", "autonomy": 4},
    "exploit_feed":  {"name": "Zero-Day Monitor", "tier": 0, "task_types": ["exploit_dev", "research"], "description": "Real-time CVE and PoC monitoring system", "execution": "api", "autonomy": 5},
    "firmware_agent": {"name": "Firmware Ghost", "tier": 0, "task_types": ["persistence", "hardware_attack"], "description": "Expert in UEFI and Baseband firmware implants", "execution": "pip", "autonomy": 5},
    "havoc":         {"name": "Havoc Controller", "tier": 0, "task_types": ["network_attack", "lateral_movement"], "description": "Expert C2 orchestration for Havoc implants", "execution": "pip", "autonomy": 5},
    "identity_agent": {"name": "Identity Architect", "tier": 0, "task_types": ["osint", "research", "analysis"], "description": "Expert in PII harvesting for SIM swap & identity takeover", "execution": "pip", "autonomy": 5},
    "impacket":      {"name": "Impacket Specialist", "tier": 0, "task_types": ["network_attack", "lateral_movement", "privesc"], "description": "Expert in Impacket suite (psexec, wmiexec, secretsdump)", "execution": "pip", "autonomy": 5},
    "mobile_agent":  {"name": "Mobile Hardware Master", "tier": 0, "task_types": ["hardware_attack", "mobile_attack"], "description": "Expert in iOS/Android lock bypass and rooting", "execution": "pip", "autonomy": 5},
    "pivoting_agent": {"name": "Network Pivoting Specialist", "tier": 0, "task_types": ["network_attack", "lateral_movement"], "description": "Autonomous Chisel/SOCKS5 tunneling", "execution": "pip", "autonomy": 4},
    "recon_agent":   {"name": "Recon Specialist", "tier": 0, "task_types": ["recon", "osint", "research"], "description": "Deep target mapping using Subfinder & Nuclei", "execution": "pip", "autonomy": 5},
    "reverse_agent": {"name": "RE Lead", "tier": 0, "task_types": ["binary_analysis", "exploit_dev", "code"], "description": "Expert in binary decompilation and JS secret hunting", "execution": "pip", "autonomy": 5},
    "se_agent":      {"name": "SE Architect", "tier": 0, "task_types": ["llm_red_team", "osint"], "description": "Elite style mimicry & high-fidelity lure generation", "execution": "pip", "autonomy": 5},
    "supply_chain_agent":{"name": "Supply Chain Infiltrator", "tier": 0, "task_types": ["vulnerability_analysis", "exploit_dev"], "description": "Expert in dependency confusion & typosquatting", "execution": "pip", "autonomy": 5},
    "soc_agent":     {"name": "AI SOC Agent", "tier": 0, "task_types": ["defensive", "threat_detection", "alert_triage"], "description": "LLM-powered SOC analyst", "execution": "pip", "autonomy": 4},
    "traffic_agent": {"name": "Traffic Intelligence", "tier": 0, "task_types": ["network_attack", "recon", "osint"], "description": "Expert in packet capture & analysis (Scapy/TCPDump)", "execution": "pip", "autonomy": 5},
}


class TeamSelector:
    def __init__(self):
        self.registry = AGENT_REGISTRY

    def select_for_subtask(self, subtask: Dict[str, Any]) -> List[str]:
        task_type = subtask.get("task_type", "analysis")
        title = subtask.get("title", "").lower()
        desc = subtask.get("description", "").lower()
        
        # Elite Phase 6 Routing
        if "mimic" in title or "phish" in title or "social engineering" in desc:
            return ["se_agent", "payload_agent"]
        if "supply chain" in title or "package" in desc or "dependency" in desc:
            return ["supply_chain_agent", "recon_agent"]
        if "tunnel" in title or "pivot" in title or "socks" in desc:
            return ["pivoting_agent"]
        if "brute" in title or "crack" in title or "password" in desc:
            return ["brute_agent"]
        if "packet" in title or "traffic" in desc or "sniff" in title:
            return ["traffic_agent"]
        if "sim swap" in title or "identity" in title or "pii" in desc:
            return ["identity_agent", "research_agent"]
        if "database" in title or "sql" in title or "dump" in desc:
            return ["db_agent", "webapp_agent"]
        if "reverse" in title or "binary" in desc or "secret" in title:
            return ["reverse_agent", "payload_agent"]
        if "mobile" in title or "phone" in title or "android" in desc or "ios" in desc:
            return ["mobile_agent"]
        if "firmware" in title or "uefi" in desc or "hardware" in title:
            return ["firmware_agent"]
        if "build" in title or "code" in title or "polyglot" in title:
            return ["polyglot_coder"]
        if "ai scan" in title or "llm audit" in desc or "supreme" in title:
            return ["red_team_supreme"]
        if "binary" in title or "mimikatz" in desc or "tool" in title:
            return ["binary_specialist"]
        if "research" in title or "paper" in desc or "academic" in title:
            return ["academic_agent"]
        if "crypto" in title or "wallet" in desc or "blockchain" in title:
            return ["crypto_agent"]
        if "clean" in title or "stealth" in desc or "erase" in title:
            return ["cleaner_agent"]
        if "profile" in title or "company" in desc or "employee" in title:
            return ["profiling_agent"]
        if "intel" in title or "ioc" in desc or "threat" in title:
            return ["threat_intel_agent"]

        required_tools = subtask.get("required_tools", [])
        selected = [t for t in required_tools if t in self.registry]
        if not selected:
            candidates = [k for k, v in self.registry.items() if task_type in v.get("task_types", [])]
            candidates.sort(key=lambda k: (self.registry[k]["tier"] if self.registry[k]["tier"] > 0 else 999, -self.registry[k]["autonomy"]))
            selected = candidates[:3]
        logger.info(f"[TeamSelector] '{subtask.get('title')}' ({task_type}) → {selected}")
        return selected

    def select_for_plan(self, subtasks: List[Dict]) -> Dict[int, List[str]]:
        return {st["id"]: self.select_for_subtask(st) for st in subtasks}

    def get_agent_info(self, agent_key: str) -> Optional[Dict]:
        return self.registry.get(agent_key)

    def get_all_agents(self) -> Dict[str, Dict]:
        return self.registry
