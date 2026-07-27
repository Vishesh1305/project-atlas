import pytest
from pydantic import BaseModel

from atlas.registry import ToolRegistry
from atlas.tools.base import Tool


class FakeModel(BaseModel):
    exp: str

class FakeTool(Tool):
    @property
    def name(self) -> str:
        return "fake"
    @property
    def description(self) -> str:
        return "fake description"
    @property
    def sensitivity(self) -> str:
        return "fake sensitivity"
    @property
    def input_model(self) -> type[BaseModel]:
        return FakeModel

    def _execute(self, validated_input: BaseModel) -> str:
        assert isinstance(validated_input, FakeModel)
        return f"[Stub] would evaluate: {validated_input.exp}"

def test_registry() -> None:
    registry = ToolRegistry()
    tool = FakeTool()
    registry.register(tool)
    result = registry.retrieve("fake")
    assert result is tool

def test_register_duplicate_raises() -> None:
    registry = ToolRegistry()
    tool = FakeTool()
    registry.register(tool)
    with pytest.raises(ValueError):
        registry.register(tool)
