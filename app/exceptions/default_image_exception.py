from pydantic import ValidationError

from .base_exception import BaseException
from ..models.enums import ImageGenderEnum, ImageAgeGroupEnum, ImageEmotionEnum


class UnsupportedImageFormatException(BaseException):
    def __init__(self, content_type: str = None):
        details = {
            "content_type": content_type,
            "supported_formats": ["image/jpeg", "image/png", "image/gif"]
        }
        super().__init__(
            status_code=415,
            message="지원하지 않는 파일 형식입니다.",
            code="UNSUPPORTED_IMAGE_FORMAT",
            details=details
        )

class ImageNotFoundException(BaseException):
    def __init__(self, image_id: int):
        super().__init__(
            status_code=404,
            message="이미지를 찾을 수 없습니다.",
            code="IMAGE_NOT_FOUND",
            details={
                "image_id": image_id
            }
        )

class InvalidEnumValueException(BaseException):
    @classmethod
    def from_validation_error(cls, error: ValidationError):
        error_detail = error.errors()[0]
        if error_detail["type"] != "enum":
            return None
            
        field = error_detail["loc"][0]
        provided_value = error_detail["input"]
        
        # Enum 매핑
        enum_mappings = {
            "image_gender": ImageGenderEnum,
            "image_age_group": ImageAgeGroupEnum,
            "image_emotion": ImageEmotionEnum
        }
        
        if field in enum_mappings:
            allowed_values = [e.value for e in enum_mappings[field]]
            return cls(field=field, provided_value=provided_value, allowed_values=allowed_values)
        return None

    def __init__(self, field: str, provided_value: str, allowed_values: list[str]):
        field_names = {
            "image_gender": "성별",
            "image_age_group": "연령대",
            "image_emotion": "감정"
        }
        
        details = {
            "field": field,
            "field_name": field_names.get(field, field),
            "provided_value": provided_value,
            "allowed_values": allowed_values
        }
        
        super().__init__(
            status_code=400,
            message=f"잘못된 {field_names.get(field, field)} 값입니다.",
            code="INVALID_ENUM_VALUE",
            details=details
        )