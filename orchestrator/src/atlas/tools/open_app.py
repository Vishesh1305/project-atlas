import logging
import tomllib
from pathlib import Path

from pydantic import BaseModel

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)

class OpenAppInput(BaseModel):
    pass

class OpenAppTool(Tool):
    def __init__(self):
        super().__init__()
        toml_path = Path(__file__).parent.parent.parent.parent / "config" / "allowlist.toml"
        with open(toml_path, "rb") as f:
            tomllib.load(f)
    @property
    def name(self) -> str:
        return "open_app"
    @property
    def description(self) -> str:
        return "Opens an App from the allowed apps."
    @property
    def sensitivity(self) -> str:
        return ""
    @property
    def input_model(self) -> type[BaseModel]:
        return OpenAppInput

    def _execute(self, validated_input: BaseModel) -> str:
        return "f"
