import logging

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, tool_to_register):
        self.registry[tool_to_register.name] = tool_to_register

    def retrieve(self, tool_name : str) -> Tool | None:
        requested_tool = self.registry.get(tool_name, None)
        if requested_tool is None:
            logger.warning("Tool %s not found in registry", tool_name)
            return None
        return requested_tool
