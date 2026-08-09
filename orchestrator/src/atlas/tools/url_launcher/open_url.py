import logging

from pydantic import BaseModel, HttpUrl

from atlas.tools.base import Tool

logger = logging.getLogger(__name__)


class OpenUrlInput(BaseModel):
    url: HttpUrl


class OpenUrlTool(Tool):
    @property
    def name(self) -> str:
        return "open_url"

    @property
    def description(self) -> str:
        return "Opens a specified URL"

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return OpenUrlInput

    def _execute(self, validated_input: BaseModel) -> str:
        assert isinstance(validated_input, OpenUrlInput)
        logger.info("OpenUrlTool would open URL: %s", validated_input.url)
        return f"[Stub] would open: {validated_input.url}"
