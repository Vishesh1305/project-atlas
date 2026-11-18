import cmd

from atlas.registry import ToolRegistry
from atlas.tools.weather.geocode import geocode


class AtlasRepl(cmd.Cmd):
    intro = "Welcome to the Atlas Repl. Type help or ? to list commands.\n"
    prompt = "atlas> "

    def __init__(self, registry: ToolRegistry) -> None:
        super().__init__()
        self.registry = registry

    def do_calculate(self, arg: str) -> None:
        """Calculates any given mathematical expression

        Usage: calculate <expression>
        Example: calculate 2 + 3 * 4
        """
        if not arg:
            # print(
            #     f"Invalid Expression input in: {arg}. Make sure you are not leaving any "
            #     f" unnecessary whitespaces"
            # )
            print("No expression given. Type one, e.g. 'calculate 2 + 3 * 4'.")
            return
        tool = self.registry.retrieve("util.calculate")
        # assert calculate_tool is not None
        result = tool.run({"expression": arg})
        print(result)

    def do_open_app(self, arg: str) -> None:
        """Opens apps that are present in the allowlist

        Usage: open_app <app name>
        Example: open_app notepad
        """
        if not arg:
            # print(
            #     f"Invalid Expression input in = {arg}. Make sure you are not leaving "
            #     f" any unnecessary whitespaces"
            # )
            print("No app name given. Type one, e.g. 'open_app notepad'.")
            return
        tool = self.registry.retrieve("pc.open_app")
        # assert open_tool is not None
        result = tool.run({"app_name": arg})
        print(result)

    def do_open_url(self, arg: str) -> None:
        """Opens any given URL

        Usage: open_url <url>
        Example: open_url https://example.com
        """
        if not arg:
            # print(
            #     f"Invalid URL input in = {arg}. Make sure you are not leaving any unnecessary"
            #     f" whitespaces and also the URL is correct"
            # )
            print("No URL given. Type one, e.g. 'open_url https://example.com'.")
            return
        tool = self.registry.retrieve("pc.open_url")
        # assert open_url is not None
        result = tool.run({"url": arg})
        print(result)

    def do_clock(self, arg: str) -> None:
        """Shows the current local date and time

        Usage: clock
        Takes no arguments.
        """
        if arg:
            print("clock takes no arguments. Type just 'clock'.")
            return
        tool = self.registry.retrieve("util.clock")
        # assert clock_tool is not None
        result = tool.run({})
        print(result)

    def do_quit(self, arg: str) -> bool:
        """Quits the application"""
        print("Exiting the repl loop...")
        return True

    def do_weather(self, arg: str) -> None:
        """Prints weather data

        Usage: weather <place>
        Example: weather vancouver, canada
        """
        if not arg:
            print("No place name given. Type a place, e.g. 'weather Vancouver'.")
            return
        tool = self.registry.retrieve("info.weather")
        # assert weather_tool is not None
        place = geocode(arg)
        if place is None:
            print("No such place")
            return
        result = tool.run({"latitude": place.latitude, "longitude": place.longitude})

        parts = []
        if place.name:
            parts.append(place.name)
        if place.admin1:
            parts.append(place.admin1)
        if place.country:
            parts.append(place.country)
        location = ", ".join(parts)
        print(f"Weather data of: {location}")
        print(f"Latitude: {place.latitude}, Longitude: {place.longitude}")
        print(result)

    def do_news(self, arg: str) -> None:
        """Search recent news headlines by topic.

        Usage: news <topic>
        Example: news formula 1
        """
        if not arg:
            print("No topic given. Type a topic, e.g. 'news formula 1'.")
            return

        topic = arg

        tool = self.registry.retrieve("info.news")
        # if tool is None:
        #     print("News tool is not registered.")
        #     return

        result = tool.run({"topic": topic})
        print(result)

    def emptyline(self) -> bool:
        return False
