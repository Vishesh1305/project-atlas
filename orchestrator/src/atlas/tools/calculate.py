import logging

from pydantic import BaseModel

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)


class CalculateInput(BaseModel):
    expression: str


class CalculateTool(Tool):
    @property
    def name(self) -> str:
        return "calculate"

    @property
    def description(self) -> str:
        return "Calculate expression"

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return CalculateInput

    def _execute(self, validated_input: BaseModel) -> str:
        assert isinstance(validated_input, CalculateInput)
        logger.info(f"Calculate tool would evaluate expression: {validated_input.expression}")
        return f"[Stub] would evaluate: {validated_input.expression}"
