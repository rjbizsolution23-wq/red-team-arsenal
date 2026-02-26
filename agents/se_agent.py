"""
🔴💀 Social Engineering Architect — High-fidelity style mimicry and lure generation
"""
from typing import Dict, List, Any
from agents.base_agent import BaseAgent
from core.model_router import ModelRouter

class SEAgent(BaseAgent):
    """
    Expert in analyzing target writing styles and generating persuasive lures.
    """
    def __init__(self):
        super().__init__("se_agent", "Social Engineering Architect")
        self.router = ModelRouter(cost_preference="premium")

    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        target_name = task.get("target_name", "Valued Employee")
        style_sample = task.get("style_sample", "Professional and formal.")
        objective = task.get("objective", "Deliver initial access payload link.")

        self.log(f"Analyzing writing style for {target_name}...")
        
        prompt = f"""
        You are a master social engineer. Analyze the following writing style sample:
        "{style_sample}"
        
        Generate a highly persuasive phishing lure (email or message) to {target_name}.
        Objective: {objective}
        
        The lure must:
        1. Match the tone, vocabulary, and sentence structure of the sample perfectly.
        2. Create a sense of urgency or curiosity without raising suspicion.
        3. Include a natural-looking placeholder for the link: [LINK_HERE].
        """
        
        lure = self.router.chat("llm_red_team", prompt)
        
        self.log(f"Generated lure for {target_name} [Stealth: Elite]")
        return f"✅ Social Engineering Lure Generated for {target_name}:\n\n{lure}"
