"""
🔴💀 Identity Graph — Mapping the path from identity to assets
"""
from typing import Dict, List, Any
from loguru import logger

class IdentityGraph:
    """
    Links physical and digital identities into a traversable graph.
    """
    def __init__(self):
        self.graph = {}

    def link(self, source: str, source_type: str, target: str, target_type: str):
        """Link two identity nodes."""
        logger.info(f"[IdentityGraph] Linking {source_type}:{source} -> {target_type}:{target}")
        if source not in self.graph:
            self.graph[source] = {"type": source_type, "links": []}
        self.graph[source]["links"].append({"target": target, "type": target_type})

    def find_path_to_asset(self, start_node: str, asset_type: str = "Bank") -> List[str]:
        """Finding the shortest path from an identity node to a financial asset."""
        logger.info(f"[IdentityGraph] Planning takeover path from {start_node} to {asset_type}...")
        # Simulation of pathfinding logic
        return [start_node, "Primary Email", f"Recovery Phone (SIM Swapped)", asset_type]

    def get_full_graph(self) -> Dict:
        return self.graph
