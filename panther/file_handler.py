from functools import cached_property

from panther import status
from pydantic import BaseModel, field_validator

from panther.exceptions import APIException


class File(BaseModel):
    file_name: str
    content_type: str
    file: bytes

    @cached_property
    def size(self):
        return len(self.file)

    def __repr__(self) -> str:
        return f'{self.__repr_name__()}(file_name={self.file_name}, content_type={self.content_type})'

    __str__ = __repr__


class Image(File):
    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, content_type: str) -> str:
        if not content_type.startswith('image/'):
            msg = f"{content_type} is not a valid image 'content_type'"
            raise APIException(detail=msg, status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return content_type
