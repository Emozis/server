from pydantic import ValidationError
from enum import Enum
from typing import Type, Optional

from .base_exception import BaseException
from ..models.enums import ImageGenderEnum, ImageAgeGroupEnum, ImageEmotionEnum


class UnsupportedImageFormatException(BaseException):
    def __init__(self, content_type: str = None):
        data = {
            "content_type": content_type,
            "supported_formats": ["image/jpeg", "image/png", "image/gif"]
        }
        super().__init__(
            status_code=415,
            message="지원하지 않는 파일 형식입니다.",
            code="UNSUPPORTED_IMAGE_FORMAT",
            data=data
        )

class ImageNotFoundException(BaseException):
    def __init__(self, image_id: int):
        super().__init__(
            status_code=404,
            message="이미지를 찾을 수 없습니다.",
            code="IMAGE_NOT_FOUND",
            data={
                "image_id": image_id
            }
        )

class InvalidEnumValueException(BaseException):
    @classmethod
    def from_validation_error(cls, error: ValidationError, field_names: dict[str, str] = None) -> Optional['InvalidEnumValueException']:
        """
        ValidationError로부터 InvalidEnumValueException을 생성합니다.
        
        Args:
            error: Pydantic ValidationError
            field_names: 필드명과 표시될 이름의 매핑 딕셔너리 (선택사항)
        """
        error_detail = error.errors()[0]
        if error_detail["type"] != "enum":
            return None
            
        field = error_detail["loc"][0]
        provided_value = error_detail["input"]
        
        # Pydantic v2에서는 error message에서 enum 값들을 파싱해야 함
        error_msg = error_detail.get("msg", "")
        # "Input should be 'value1', 'value2' or 'value3'" 형태의 메시지에서 값들을 추출
        import re
        matches = re.findall(r"'([^']*)'", error_msg)
        allowed_values = list(dict.fromkeys(matches))  # 중복 제거
        
        return cls(
            field=field,
            provided_value=provided_value,
            allowed_values=allowed_values,
            field_name=field_names.get(field, field) if field_names else field
        )

    @classmethod
    def from_enum(
        cls,
        field: str,
        enum_class: Type[Enum],
        provided_value: str,
        field_name: Optional[str] = None
    ) -> 'InvalidEnumValueException':
        """
        Enum 클래스로부터 직접 InvalidEnumValueException을 생성합니다.
        
        Args:
            field: 필드명
            enum_class: Enum 클래스
            provided_value: 제공된 값
            field_name: 표시될 필드 이름 (선택사항)
        """
        allowed_values = [e.value for e in enum_class]
        return cls(
            field=field,
            provided_value=provided_value,
            allowed_values=allowed_values,
            field_name=field_name or field
        )

    def __init__(
        self,
        field: str,
        provided_value: str,
        allowed_values: list[str],
        field_name: Optional[str] = None
    ):
        """
        InvalidEnumValueException을 초기화합니다.
        
        Args:
            field: 필드명
            provided_value: 제공된 값
            allowed_values: 허용된 값들의 리스트
            field_name: 표시될 필드 이름 (선택사항)
        """
        data = {
            "field": field,
            "field_name": field_name or field,
            "provided_value": provided_value,
            "allowed_values": allowed_values
        }
        
        super().__init__(
            status_code=422,
            message=f"잘못된 {field_name or field} 값입니다.",
            code="INVALID_ENUM_VALUE",
            data=data
        )