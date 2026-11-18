from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Resolve from this file so `uvicorn` may be launched from either the
    # repository root or the backend directory.
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[3] / ".env", extra="ignore")
    # The JCX aliases prevent globally exported MYSQL_* variables (for
    # example from Conda) from overriding this project's Docker settings.
    mysql_host: str = Field(default="127.0.0.1", validation_alias="JCX_MYSQL_HOST")
    # Docker exposes this project's MySQL container on host port 3307 to avoid
    # colliding with a separately installed local MySQL service on port 3306.
    mysql_port: int = Field(default=3307, validation_alias="JCX_MYSQL_PORT")
    mysql_database: str = Field(default="jingcaixing", validation_alias="JCX_MYSQL_DATABASE")
    mysql_user: str = Field(default="jcx_app", validation_alias="JCX_MYSQL_USER")
    mysql_password: str = Field(default="jcx_dev_2026", validation_alias="JCX_MYSQL_PASSWORD")
    ai_provider: str = "mock"
    map_provider: str = Field(default="mock", validation_alias="JCX_MAP_PROVIDER")
    amap_web_service_key: str | None = Field(default=None, validation_alias="JCX_AMAP_WEB_SERVICE_KEY")
    qwen_api_key: str | None = None
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen4-max"
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"

def get_settings() -> Settings:
    return Settings()
