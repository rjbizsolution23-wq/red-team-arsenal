"""
🔴💀 Nuclei Wrapper — Template-based vulnerability scanner
"""
import json
from typing import Any, Dict, List, Optional
from tools.base_tool import BaseTool

class NucleiWrapper(BaseTool):
    def __init__(self, binary_path: Optional[str] = None):
        super().__init__("nuclei", binary_path)

    def scan(self, target: str, templates: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Perform a nuclei scan on a target."""
        args = ["-u", target, "-json-export", "/tmp/nuclei_out.json"]
        if templates:
            args.extend(["-t", ",".join(templates)])
        
        # In a real system, we'd check if nuclei is installed
        # For now, we simulate or run if available
        res = self.execute(args)
        
        findings = []
        try:
            # Nuclei exports line-by-line JSON
            import os
            if os.path.exists("/tmp/nuclei_out.json"):
                with open("/tmp/nuclei_out.json", "r") as f:
                    for line in f:
                        findings.append(json.loads(line))
                os.remove("/tmp/nuclei_out.json")
        except Exception:
            pass
            
        return findings
