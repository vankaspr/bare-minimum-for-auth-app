from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo_pool: bool = False
    echo: bool = False
    max_overflow: int = 50
    pool_size: int = 10

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()

settings = Settings()