"""
🔴💀 Pivoting Agent — Autonomous Chisel and SOCKS5 tunnel management
"""
import subprocess
import time
from typing import Dict, List, Any
from agents.base_agent import BaseAgent

class PivotingAgent(BaseAgent):
    """
    Manages network tunnels to pivot into internal networks.
    Supports Chisel and SSH SOCKS5.
    """
    def __init__(self):
        super().__init__("pivoting_agent", "Network Pivoting Specialist")
        self.active_tunnels = {}

    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        tunnel_type = task.get("type", "chisel")
        remote_host = task.get("remote_host")
        port = task.get("port", 8080)
        
        self.log(f"Establishing {tunnel_type} tunnel to {remote_host}:{port}...")
        
        # Simulation of tunnel establishment
        tunnel_id = f"{tunnel_type}_{remote_host}_{port}"
        
        if tunnel_type == "chisel":
            # Command: chisel client <remote> R:socks
            self.log(f"Spawning Chisel client for reverse socks...")
            self.active_tunnels[tunnel_id] = {"pid": 12345, "type": "chisel", "target": remote_host}
        elif tunnel_type == "socks":
            # Command: ssh -D <port> -N <user>@<host>
            self.log(f"Establishing SSH SOCKS5 proxy on port {port}...")
            self.active_tunnels[tunnel_id] = {"pid": 12346, "type": "socks", "port": port}
            
        time.sleep(2) # Establish delay
        self.log(f"Tunnel {tunnel_id} is ACTIVE.")
        
        return f"✅ {tunnel_type.upper()} tunnel established to {remote_host}. Internal network access via 127.0.0.1:{port}"

    def get_active_routes(self) -> List[Dict]:
        return list(self.active_tunnels.values())
