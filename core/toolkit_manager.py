"""
🔴💀 Toolkit Manager — Handles installation and health checks for elite red team tools
"""
import os
import shutil
import subprocess
from typing import Dict, List, Any
from loguru import logger

class ToolkitManager:
    def __init__(self, install_dir: str = "./bin"):
        self.install_dir = os.path.abspath(install_dir)
        os.makedirs(self.install_dir, exist_ok=True)
        self.tools = {
            "sliver": {"type": "binary", "url": "https://sliver.sh/install"},
            "nuclei": {"type": "go", "pkg": "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"},
            "subfinder": {"type": "go", "pkg": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"},
            "metasploit": {"type": "system", "cmd": "msfconsole"},
            "impacket": {"type": "pip", "pkg": "impacket"},
        }

    def check_health(self) -> Dict[str, bool]:
        """Check if tools are installed and accessible."""
        health = {}
        for name, info in self.tools.items():
            if info["type"] == "system":
                health[name] = shutil.which(info["cmd"]) is not None
            elif info["type"] == "pip":
                try:
                    __import__(info["pkg"])
                    health[name] = True
                except ImportError:
                    health[name] = False
            else:
                health[name] = shutil.which(name) is not None
        return health

    def install_tool(self, name: str) -> bool:
        """Attempt to install a tool based on its type."""
        if name not in self.tools:
            return False
            
        info = self.tools[name]
        logger.info(f"[ToolkitManager] Installing {name}...")
        
        try:
            if info["type"] == "pip":
                subprocess.run(["pip", "install", info["pkg"]], check=True)
                return True
            elif info["type"] == "go":
                # Requires GO to be installed
                subprocess.run(["go", "install", info["pkg"]], check=True)
                return True
            # Other types would require more complex logic (curl | bash, etc.)
            return False
        except Exception as e:
            logger.error(f"[ToolkitManager] Failed to install {name}: {e}")
            return False
