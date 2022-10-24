from pydantic import BaseModel, HttpUrl, constr


class S3BrowserRequest(BaseModel):
    path: str = None

    class Config:
        schema_extra = {
            "example": {
                "path": "path/to/",
            }
        }


class S3DeleteRequest(BaseModel):
    path: str

    class Config:
        schema_extra = {
            "example": {
                "path": "path/to/",
            },
        }


PathStr = constr(regex=r"^([a-z]+\/)+$")


class S3UploadRequest(BaseModel):
    path: PathStr
    filename: str
    content_type: str
    size: int

    class Config:
        schema_extra = {
            "example": {
                "path": "path/to/",
                "filename": "file.txt",
                "content_type": "text/plain",
                "size": 50,
            }
        }


class S3UploadFields(BaseModel):
    key: str
    content_type: str
    content_disposition: str
    x_amz_algorithm: str
    x_amz_credential: str
    x_amz_signature: str
    x_amz_date: str
    policy: str

    class Config:
        @classmethod
        def alias_generator(cls, string: str) -> str:
            return "-".join(word.capitalize() for word in string.split("_"))


class S3UploadResponse(BaseModel):
    url: HttpUrl
    fields: S3UploadFields
