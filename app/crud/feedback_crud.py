from sqlalchemy.orm import Session

from ..models import Feedback
from .base_crud import BaseCRUD


class FeedbackCRUD(BaseCRUD[Feedback]):
    def __init__(self, db: Session):
        super().__init__(model=Feedback, db=db, id_field='feedback_id')