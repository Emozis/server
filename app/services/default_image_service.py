from sqlalchemy.orm import Session
from fastapi import UploadFile

from ..core import logger
from ..crud import DefaultImageCRUD
from ..mappers import DefaultImageMapper
from ..schemas import MessageResponse, DefaultImageCreate, DefaultImageResponse
from ..exceptions import NotFoundException
from ..utils import upload_to_s3

class DefaultImageService:
    def __init__(self, db: Session):
        self.db = db
        self.default_image_crud = DefaultImageCRUD(db)

    async def create_default_image(self, default_image: DefaultImageCreate, image: UploadFile) -> MessageResponse:
        # S3에 이미지 업로드
        default_image.image_url = await upload_to_s3(file=image, folder_path="default_images")
        
        # 파일 이름 제작
        cnt = self.default_image_crud.get_total_count()
        default_image.image_name = f"{str(default_image.image_gender.value)[0].upper()}{str(default_image.image_age_group.value)[0].upper()}{str(default_image.image_emotion.value)[0].upper()}-{str(cnt).zfill(3)}"

        # DB에 이미지 저장
        self.default_image_crud.create(DefaultImageMapper.create_to_model(default_image))
        return MessageResponse(message="기본 이미지가 성공적으로 저장되었습니다.")
    
    def get_default_images(self) -> list[DefaultImageResponse]:
        return DefaultImageMapper.to_dto_list(self.default_image_crud.get_all())
    
    def get_default_image(self, image_id: int) -> DefaultImageResponse:
        db_default_image = self.default_image_crud.get_by_id(image_id)
        if not db_default_image:
            logger.warning(f"❌ Failed to find default image with id {image_id}")
            raise NotFoundException("이미지를 찾을 수 없습니다.")

        return DefaultImageMapper.to_dto(db_default_image)
    
    async def update_default_image(self,  image_id: int, default_image: DefaultImageCreate, image: UploadFile):
        self.get_default_image(image_id)

        # S3에 이미지 업로드
        default_image.image_url = await upload_to_s3(file=image, folder_path="default_images")

        # 파일 이름 제작
        cnt = self.default_image_crud.get_total_count()
        default_image.image_name = f"{str(default_image.image_gender.value)[0].upper()}{str(default_image.image_age_group.value)[0].upper()}{str(default_image.image_emotion.value)[0].upper()}-{str(cnt).zfill(3)}"

        # DB에 이미지 저장
        self.default_image_crud.update(image_id, DefaultImageMapper.update_to_model(default_image))
        return MessageResponse(message="기본 이미지가 성공적으로 저장되었습니다.")
    
    def delete_default_image(self,  image_id: int):
        self.get_default_image(image_id)
        if self.default_image_crud.delete(image_id):
            return MessageResponse(message="이미지가 성공적으로 삭제되었습니다.")
