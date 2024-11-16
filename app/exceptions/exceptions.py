from .base_exception import BaseException


class NotFoundException(BaseException):
    def __init__(self, message: str, relationship_id: int = None):
        super().__init__(
            status_code=404,
            message=message,
            code="NOT_FOUND",
            details={"relationship_id": relationship_id}
        )

class InternalServerError(BaseException):
    def __init__(self, error: Exception):
        super().__init__(
            status_code=500,
            message="내부 서버 오류가 발생했습니다.",
            code="INTERNAL_SERVER_ERROR",
            details={"error": str(error)}
        )