from atlas.logging_config import setup_logging
from atlas.registry import ToolRegistry
from atlas.repl import AtlasRepl
from atlas.tools.app_launcher.open_app import OpenAppTool
from atlas.tools.calculator.calculate import CalculateTool
from atlas.tools.hourglass.clock import ClockTool
from atlas.tools.url_launcher.open_url import OpenUrlTool


def main() -> None:
    setup_logging()
    registry = ToolRegistry()

    registry.register(CalculateTool())
    registry.register(OpenAppTool())
    registry.register(OpenUrlTool())
    registry.register(ClockTool())

    AtlasRepl(registry).cmdloop()
