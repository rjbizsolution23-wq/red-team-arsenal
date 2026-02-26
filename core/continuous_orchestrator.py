"""
🔴💀 Continuous Orchestrator — Recursive mission execution
"""
import time
from typing import Dict, List, Any
from loguru import logger
from core.orchestrator import Orchestrator

class ContinuousOrchestrator:
    """
    Manages recursive mission "cycles."
    Doesn't stop until the objective is reached or max_cycles is hit.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.max_cycles = 5
        self.cycle_count = 0
        self.is_infinite = False

    async def run_mission(self, request: str, target: str, infinite: bool = False, authorized: bool = False):
        self.is_infinite = infinite
        self.cycle_count = 0
        
        logger.info(f"🔴💀 [LEGENDARY MODE] Starting Infinite Execution Loop for: {request}")
        
        while self.cycle_count < self.max_cycles:
            self.cycle_count += 1
            logger.info(f"== CYCLE {self.cycle_count} / {self.max_cycles if not self.is_infinite else '∞'} ==")
            
            # Execute one full orchestration cycle
            result = self.orchestrator.run(request, target, authorized=authorized)
            
            # Check for "Mission Accomplished" signal in results
            findings = result.get("findings", [])
            is_done = any(f.get("status") == "mission_accomplished" for f in findings)
            
            if is_done:
                logger.success(f"🎯 Objective reached in cycle {self.cycle_count}!")
                break
                
            if self.cycle_count < self.max_cycles:
                logger.info(f"Cycle {self.cycle_count} complete. Re-evaluating strategy for next loop...")
                # In the next loop, the task_planner will ingest the findings from this cycle
                # to create a more advanced plan.
                time.sleep(5) # Stealth cooldown
            
        logger.info("🔴💀 Infinite Execution Finished.")
        return result
