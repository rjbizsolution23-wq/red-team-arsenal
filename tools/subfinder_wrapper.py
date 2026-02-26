"""
🔴💀 Subfinder Wrapper — Passive subdomain discovery
"""
from typing import List, Optional
from tools.base_tool import BaseTool

class SubfinderWrapper(BaseTool):
    def __init__(self, binary_path: Optional[str] = None):
        super().__init__("subfinder", binary_path)

    def discover(self, domain: str) -> List[str]:
        """Discover subdomains for a domain."""
        args = ["-d", domain, "-silent"]
        res = self.execute(args)
        
        if res["exit_code"] == 0:
            return [line.strip() for line in res["stdout"].split("\n") if line.strip()]
        return []
