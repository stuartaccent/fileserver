from typing import List, Optional

from pydantic import BaseSettings, HttpUrl, SecretStr


class Settings(BaseSettings):
    allow_origins: List[str] = ["*"]
    allowed_hosts: List[str] = ["*"]
    aws_access_key: str
    aws_secret_key: SecretStr
    aws_region: str
    aws_s3_bucket: str
    sentry_dsn: Optional[HttpUrl] = None


settings = Settings()
