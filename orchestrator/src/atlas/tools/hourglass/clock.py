
from datetime import datetime

from pydantic import BaseModel

from atlas.tools.base import Tool


def _suffix(in_date: str) -> str:
    """
        :param in_date: Input date number
        :type in_date: str
        :return: the date with a proper ordinal suffix
        :rtype: str
    """
    if 10 <= int(in_date) % 100 <= 20:
        suffix_ = "th"
    else:
        suffix_ = {1: "st", 2: "nd", 3: "rd"}.get(int(in_date) % 10, "th")
    return f"{in_date}{suffix_}"

class ClockInput(BaseModel):
    pass

class ClockTool(Tool):

    @property
    def name(self) -> str:
        return "clock"

    @property
    def description(self) -> str:
        return "Displays time and date"

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return ClockInput

    def _execute(self, validated_input: BaseModel) -> str:
        """
        :return: It returns current time with proper day name, date and year
        :rtype: str
        """
        now = datetime.now()
        date = _suffix(now.strftime("%d"))
        result = f"{now.strftime('%a')} {date} {now.strftime('%b %Y, %I:%M %p')}"
        return result

if __name__ == "__main__":
    tool = ClockTool()
    print(tool.run({}))
