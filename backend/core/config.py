from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #bieng professional
    PROJECT_NAME: str = "AI-Interview"
    VERSION: str = "1.0.0"

    #database now
    DATABASE_URL: str = ""



    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()