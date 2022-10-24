from aioaws.s3 import S3Client, S3Config
from httpx import AsyncClient

from app.config import settings


async def get_s3_client():
    async with AsyncClient(timeout=30) as client:
        s3_config = S3Config(
            settings.aws_access_key,
            settings.aws_secret_key.get_secret_value(),
            settings.aws_region,
            settings.aws_s3_bucket,
        )
        yield S3Client(client, s3_config)
