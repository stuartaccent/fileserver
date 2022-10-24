from typing import List

from aioaws.s3 import S3Client, S3File
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse, Response

from app.api.dependencies import get_s3_client
from app.api.schemas import (
    S3BrowserRequest,
    S3DeleteRequest,
    S3UploadRequest,
    S3UploadResponse,
)

router = APIRouter()


@router.delete(
    "/delete",
    response_class=Response,
    status_code=204,
)
async def s3_delete(
    data: S3DeleteRequest,
    s3_client: S3Client = Depends(get_s3_client),
):
    """delete all files recursively under the given path

    Examples:

    Single file

        {"path": "path/to/file.txt"}

    Recursive (all files found under path)

        {"path": "path/to/"}


    """
    await s3_client.delete_recursive(data.path)


@router.get(
    "/get/{path:path}",
    response_class=RedirectResponse,
)
async def s3_get_object(
    path: str,
    s3_client: S3Client = Depends(get_s3_client),
):
    """returns a redirect response with the url of the object from s3"""
    return s3_client.signed_download_url(path, max_age=3600)


@router.post(
    "/list",
    response_model=List[S3File],
)
async def s3_list_objects(
    data: S3BrowserRequest,
    s3_client: S3Client = Depends(get_s3_client),
):
    """list objects recursively under the given path"""
    return [f async for f in s3_client.list(data.path)]


@router.post(
    "/upload/request",
    response_model=S3UploadResponse,
)
async def s3_upload_request(
    data: S3UploadRequest,
    s3_client: S3Client = Depends(get_s3_client),
):
    """returns the data required to perform a direct upload to s3"""
    upload_data = s3_client.signed_upload_url(**data.dict())
    return S3UploadResponse.parse_obj(upload_data)
