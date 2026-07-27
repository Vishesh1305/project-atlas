from atlas.logging_config import setup_logging
from atlas.registry import ToolRegistry
from atlas.repl import AtlasRepl
from atlas.tools.calculate import CalculateTool
from atlas.tools.open_app import OpenAppTool
from atlas.tools.open_url import OpenUrlTool


def main() -> None:
    setup_logging()
    registry = ToolRegistry()

    registry.register(CalculateTool())
    registry.register(OpenAppTool())
    registry.register(OpenUrlTool())

    AtlasRepl(registry).cmdloop()
