from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_database: str = "jingcaixing"
    mysql_user: str = "jingcaixing"
    mysql_password: str = "change_me"
    ai_provider: str = "mock"
    map_provider: str = "mock"
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"

@lru_cache
def get_settings() -> Settings:
    return Settings()
