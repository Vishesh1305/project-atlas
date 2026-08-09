import logging
import tomllib
from pathlib import Path

from pydantic import BaseModel

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)

class OpenAppInput(BaseModel):
    app_name : str

class OpenAppTool(Tool):
    def __init__(self) -> None:
        super().__init__()
        toml_path = Path(__file__).parent.parent.parent.parent / "config" / "allowlist.toml"
        with open(toml_path, "rb") as f:
            self._allowlist = tomllib.load(f)['apps']

    @property
    def name(self) -> str:
        return "open_app"

    @property
    def description(self) -> str:
        return "Opens an App from the allowed apps."

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return OpenAppInput

    def _execute(self, validated_input: BaseModel) -> str:
        assert isinstance(validated_input, OpenAppInput)
        if validated_input.app_name not in self._allowlist:
            return f"App {validated_input.app_name} not in allowlist"
        logger.info(f"Opening app {validated_input.app_name}")
        return f"[Stub] App {validated_input.app_name} opened"

