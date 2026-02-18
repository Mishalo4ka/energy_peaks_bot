from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., validation_alias="BOT_TOKEN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
