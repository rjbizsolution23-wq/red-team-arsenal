"""
🔴💀 Base Agent — Foundation for all Autonomous Red Team Agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger

class BaseAgent(ABC):
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.logger = logger.bind(agent=name)

    @abstractmethod
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Execute a specific red team task.
        :param task: The subtask definition from the planner.
        :param context: Session context (target, previous findings, etc.)
        :return: String result/report of the execution.
        """
        pass

    def log(self, message: str, level: str = "info"):
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "debug":
            self.logger.debug(message)
