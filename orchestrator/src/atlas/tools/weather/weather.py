import httpx
from pydantic import BaseModel, Field

from atlas.tools.base import Tool


class WeatherInput(BaseModel):

    latitude: float = Field(ge=-90, le=90)
    longitude: float= Field(ge=-180, le=180)

class WeatherTool(Tool):
    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Get current temperature and humidity for a latitude and longitude"

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return WeatherInput

    def _execute(self, validated_input: BaseModel) -> str:
        assert isinstance(validated_input, WeatherInput)

        url = "https://api.open-meteo.com/v1/forecast"
        params: dict[str, str | float] = {
            "latitude": validated_input.latitude,
            "longitude": validated_input.longitude,
            "current" : "temperature_2m,relative_humidity_2m",
        }

        response = httpx.get(url, params=params)
        result = response.json()
        return (f"Temperature: {result['current']['temperature_2m']}"
                f"{result['current_units']['temperature_2m']}\n"

                f"Relative Humidity: {result['current']['relative_humidity_2m']}"
                f"{result['current_units']['relative_humidity_2m']}")
