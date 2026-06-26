import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def sensitivity(self) -> str:
        pass

    @property
    @abstractmethod
    def input_model(self) -> type[BaseModel]:
        pass

    @abstractmethod
    def _execute(self, validated_input: BaseModel) -> str:
        pass

    def run(self, raw_input: dict[str, Any]) -> str:
        try:
            validated_input = self.input_model(**raw_input)
        except ValidationError as e:
            logger.warning("Validation failed for tool '%s' : %s", self.name, e)
            return f"Invalid input for '{self.name}' : {e}"
        return self._execute(validated_input)
