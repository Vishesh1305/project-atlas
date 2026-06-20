from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, ValidationError
import logging

class Tool(ABC):
    _name : str = None
    _description : str = None
    _inputModel : int = None
    _outputModel : int = None

    @property
    @abstractmethod
    def name(self) -> str:
        pass