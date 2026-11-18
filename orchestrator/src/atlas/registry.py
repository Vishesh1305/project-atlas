# Basically registers and retrieves tools
import logging

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool_to_register: Tool) -> None:
        if tool_to_register.name in self._tools:
            raise ValueError(f"Tool {tool_to_register.name} already registered")
        self._tools[tool_to_register.name] = tool_to_register

    def retrieve(self, tool_name: str) -> Tool:
        return self._tools[tool_name]
