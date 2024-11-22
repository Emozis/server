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
        """
        새로운 기본 이미지 생성 서비스
        Args:
            default_image (DefaultImageCreate): 이미지 생성에 필요한 데이터
            image (UploadFile): 업로드할 이미지 파일
        Returns:
            MessageResponse: 생성 성공 메세지
        """
        # S3에 이미지 업로드
        default_image.image_url = await upload_to_s3(file=image, folder_path="default_images")
        
        # 파일 이름 제작
        cnt = self.default_image_crud.get_total_count()
        default_image.image_name = f"{str(default_image.image_gender.value)[0].upper()}{str(default_image.image_age_group.value)[0].upper()}{str(default_image.image_emotion.value)[0].upper()}-{str(cnt).zfill(3)}"

        # DB에 이미지 저장
        created_image = self.default_image_crud.create(DefaultImageMapper.create_to_model(default_image))

        logger.info(f"✅ Successfully created default image: {created_image.image_name} (ID: {created_image.image_id})")
        return MessageResponse(message="기본 이미지가 성공적으로 저장되었습니다.")
    
    def get_default_images(self) -> list[DefaultImageResponse]:
        """
        모든 기본 이미지 조회
        Returns:
            list[DefaultImageResponse]: 조회된 모든 기본 이미지 정보 리스트
        """
        images = self.default_image_crud.get_all()
        logger.info(f"📸 Total {len(images)} default images found")
        return DefaultImageMapper.to_dto_list(images)
    
    def get_default_image(self, image_id: int) -> DefaultImageResponse:
        """
        ID로 기본 이미지 조회
        Args:
            image_id (int): 조회할 이미지 ID
        Returns:
            DefaultImageResponse: 조회된 이미지 정보
        Raises:
            NotFoundException: 이미지를 찾을 수 없는 경우
        """
        db_default_image = self.default_image_crud.get_by_id(image_id)
        if not db_default_image:
            logger.warning(f"❌ Failed to find default image with id {image_id}")
            raise NotFoundException("이미지를 찾을 수 없습니다.", "image_id", image_id)

        logger.info(f"📸 Found default image: {db_default_image.image_name} (ID: {image_id})")
        return DefaultImageMapper.to_dto(db_default_image)
    
    async def update_default_image(self,  image_id: int, default_image: DefaultImageCreate, image: UploadFile):
        """
        기본 이미지 정보 업데이트
        Args:
            image_id (int): 업데이트할 이미지 ID
            default_image (DefaultImageCreate): 업데이트할 이미지 정보
            image (UploadFile): 업데이트할 이미지 파일
        Returns:
            MessageResponse: 업데이트 성공 메세지
        Raises:
            NotFoundException: 이미지를 찾을 수 없는 경우
        """
        self.get_default_image(image_id)

        # S3에 이미지 업로드
        default_image.image_url = await upload_to_s3(file=image, folder_path="default_images")

        # 파일 이름 제작
        cnt = self.default_image_crud.get_total_count()
        default_image.image_name = f"{str(default_image.image_gender.value)[0].upper()}{str(default_image.image_age_group.value)[0].upper()}{str(default_image.image_emotion.value)[0].upper()}-{str(cnt).zfill(3)}"

        # DB에 이미지 저장
        self.default_image_crud.update(image_id, DefaultImageMapper.update_to_model(default_image))

        logger.info(f"✅ Successfully updated default image: {default_image.image_name} (ID: {image_id})")
        return MessageResponse(message="기본 이미지가 성공적으로 저장되었습니다.")
    
    def delete_default_image(self,  image_id: int):
        """
        기본 이미지 삭제
        Args:
            image_id (int): 삭제할 이미지 ID
        Returns:
            MessageResponse: 삭제 성공 메세지
        Raises:
            NotFoundException: 이미지를 찾을 수 없는 경우
        """
        image = self.get_default_image(image_id)
        if self.default_image_crud.delete(image_id):
            logger.info(f"✅ Successfully deleted default image: {image.image_name} (ID: {image_id})")
            return MessageResponse(message="이미지가 성공적으로 삭제되었습니다.")
