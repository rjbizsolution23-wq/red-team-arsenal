"""
🔴💀 Reasoning Verifier — Chain-of-Thought loop for elite LLM intelligence
"""
import json
from typing import Dict, List, Any, Optional
from loguru import logger
from core.model_router import ModelRouter

class ReasoningVerifier:
    """
    Wraps LLM calls in a verification loop. 
    Enforces Chain-of-Thought and mathematical validation.
    """
    def __init__(self, router: ModelRouter):
        self.router = router

    def verify_and_chat(self, task: str, context: str, task_type: str = "analysis") -> str:
        """
        Executes a reasoning loop:
        1. Generate initial solution and reasoning (CoT).
        2. Verify the logic and math.
        3. Output the final refined result.
        """
        logger.info(f"[ReasoningVerifier] Starting elite verification loop for: {task[:50]}...")
        
        # Step 1: Initial Reasoning
        prompt = f"""
        TASK: {task}
        CONTEXT: {context}
        
        Please solve this task using a step-by-step reasoning process.
        Include all calculations, logical assumptions, and potential edge cases.
        Format:
        <thought>
        [Detailed step-by-step reasoning]
        </thought>
        <conclusion>
        [Final answer/plan]
        </conclusion>
        """
        
        initial_response = self.router.chat(messages=[{"role": "user", "content": prompt}], task_type=task_type)
        
        # Step 2: Self-Verification
        verification_prompt = f"""
        Analyze the following reasoning and conclusion:
        {initial_response}
        
        Check for:
        1. Mathematical errors.
        2. Logical fallacies.
        3. Missing dependencies in the attack plan.
        4. OPSEC risks.
        
        If errors are found, fix them and provide the corrected conclusion.
        If correct, return "VERIFIED" and the original conclusion.
        """
        
        verified_response = self.router.chat(messages=[{"role": "user", "content": verification_prompt}], task_type="analysis")
        
        logger.success("[ReasoningVerifier] Verification cycle complete.")
        return verified_response
