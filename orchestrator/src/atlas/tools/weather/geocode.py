import httpx
from pydantic import BaseModel


class GeocodeResult(BaseModel):
    name: str
    latitude: float
    longitude: float
    admin1: str | None = None
    country: str | None = None

def geocode(input_value : str) -> None | GeocodeResult:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params: dict[str , str | float] = {"name": input_value, "count" : 5}

    response = httpx.get(url, params=params)
    data = response.json()
    if not data.get("results"):
        return None
    geocode_result = GeocodeResult(**data["results"][0])
    return geocode_result

if __name__ == "__main__":
    txt = geocode(input("Enter your address: "))
    print(txt)
