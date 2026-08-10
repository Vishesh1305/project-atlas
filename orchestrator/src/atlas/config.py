from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT : Path = Path(__file__).parents[2]
ENV_PATH : Path = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")
    news_api_key : str | None = None
    #tool specific
    #calc tool
    calc_round: bool
    """This handles the rounding feature of the calculator."""
    calc_decimal_precision: int
    """This handles the decimal precision of the result driven by the rounding feature"""

settings = Settings()

#This is just for debugging and sanity purposes
if __name__ == "__main__":
    print(settings.news_api_key)
