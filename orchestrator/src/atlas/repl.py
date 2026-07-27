import cmd

from atlas.registry import ToolRegistry


class AtlasRepl(cmd.Cmd):
    intro = "Welcome to the Atlas Repl. Type help or ? to list commands.\n"
    prompt = "atlas> "

    def __init__(self, registry: ToolRegistry) -> None:
        super().__init__()
        self.registry = registry

    def do_calculate(self, arg: str) -> None:
        """Calculates any given mathematical expression"""
        if not arg:
            print(
                f"Invalid Expression input in: {arg}. Make sure you are not leaving any "
                f" unnecessary whitespaces")
            return
        calculate_tool = self.registry.retrieve("calculate")
        assert calculate_tool is not None
        result = calculate_tool.run({"expression": arg})
        print(result)

    def do_open_app(self, arg: str) -> None:
        """Opens apps that are present in the allowlist"""
        if not arg:
            print(
                f"Invalid Expression input in = {arg}. Make sure you are not leaving "
                f" any unnecessary whitespaces")
            return
        open_tool = self.registry.retrieve("open_app")
        assert open_tool is not None
        result = open_tool.run({"app_name": arg})
        print(result)

    def do_open_url(self, arg: str) -> None:
        """Opens any given URL"""
        if not arg:
            print(
                f"Invalid URL input in = {arg}. Make sure you are not leaving any unnecessary"
                f" whitespaces and also the URL is correct"
                )
            return
        open_url = self.registry.retrieve("open_url")
        assert open_url is not None
        result = open_url.run({"url": arg})
        print(result)

    def do_quit(self, arg: str) -> bool:
        """Quits the application"""
        print("Exiting the repl loop...")
        return True

    def emptyline(self) -> bool:
        return False
