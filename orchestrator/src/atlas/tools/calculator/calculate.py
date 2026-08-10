import logging

from pydantic import BaseModel

from atlas.config import Settings
from atlas.tools.base import Tool

from .calc_engine import CalculatorError, safe_eval

logger = logging.getLogger(__name__)
configurations = Settings()

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
        logger.info("calculate evaluating: %s", validated_input.expression)
        try:
            if configurations.calc_round:
                result = safe_eval(validated_input.expression)
                round_result = round(result, configurations.calc_decimal_precision)
                return str(round_result)
            else:
                result = safe_eval(validated_input.expression)
                return str(result)
        except CalculatorError as e:
            logger.warning("calculate failed for %r: %s", validated_input.expression, e)
            return f"Could not evaluate: {validated_input.expression}"
