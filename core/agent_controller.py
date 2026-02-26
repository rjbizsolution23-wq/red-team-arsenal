"""
🔴💀 Agent Controller — Centralized management for remote C2 implants
"""
from typing import Dict, List, Any
from loguru import logger

class AgentController:
    """
    Manages active beacons and implants abroad (Sliver, Mythic, etc.)
    """
    def __init__(self):
        self.beacons: Dict[str, Dict] = {}

    def register_beacon(self, beacon_id: str, platform: str, target_info: Dict):
        """Register a new active check-in."""
        logger.info(f"[AgentController] New {platform} beacon: {beacon_id} from {target_info.get('hostname')}")
        self.beacons[beacon_id] = {
            "platform": platform,
            "info": target_info,
            "last_seen": "just now",
            "status": "active"
        }

    def send_command(self, beacon_id: str, command: str) -> str:
        """Send a command to a specific remote agent."""
        if beacon_id not in self.beacons:
            return f"Error: Beacon {beacon_id} not found."
            
        beacon = self.beacons[beacon_id]
        logger.info(f"[AgentController] Sending '{command}' to {beacon_id} ({beacon['platform']})")
        
        # In a real system, this would call the Sliver/Mythic RPC API
        return f"[{beacon_id}] Executed: {command}. Result: OK."

    def list_beacons(self) -> List[Dict]:
        return [{"id": k, **v} for k, v in self.beacons.items()]
