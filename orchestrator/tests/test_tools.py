import pytest
from pydantic import BaseModel

from atlas.error import ToolError
from atlas.tools.calculator.calculate import CalculateTool


def test_run_invalid_input_returns_error_not_raises() -> None:
    tool = CalculateTool()
    result = tool.run({})
    assert "Invalid input" in result


class FailingCalculateTool(CalculateTool):
    """CalculateTool whose execution always raises ToolError."""

    def _execute(self, validated_input: BaseModel) -> str:
        raise ToolError("provider unavailable")


class BuggyCalculateTool(CalculateTool):
    """CalculateTool whose execution raises an unexpected exception (a bug)."""

    def _execute(self, validated_input: BaseModel) -> str:
        raise RuntimeError("programming error")


def test_run_tool_error_returns_message_not_raises() -> None:
    tool = FailingCalculateTool()
    result = tool.run({"expression": "1 + 1"})
    assert result == "provider unavailable"


def test_run_unexpected_exception_propagates() -> None:
    tool = BuggyCalculateTool()
    with pytest.raises(RuntimeError, match="programming error"):
        tool.run({"expression": "1 + 1"})
