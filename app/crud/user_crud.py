from sqlalchemy.orm import Session

from ..models.users import User
from ..schemas.user import UserUpdate

# select
def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_by_id(user_id: int, db: Session) -> User:
    return db.query(User).filter(
        User.user_id == user_id,
        User.user_is_active == True
        ).first()

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(
        User.user_email == email,
        User.user_is_active == True
        ).first()

# update
def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session) -> User:
    user_to_update = db.query(User).filter(
        User.user_id == user_id,
        User.user_is_active == True
        ).first()
    if user_to_update:
        for attr, value in vars(user_data).items():
            if value is not None and attr != "_sa_instance_state":
                setattr(user_to_update, attr, value)
        db.commit()
        return user_to_update
    return None

# delete
def delete_user_by_id(user_id: int, db: Session) -> bool:
    user_to_delete = db.query(User).filter(User.user_id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return True
    return False

# deactivate
def deactivate_user_by_id(user_id: int, db: Session):
    user_to_deactivate = db.query(User).filter(
        User.user_id == user_id,
        User.user_is_active == True
        ).first()
    if user_to_deactivate:
        user_to_deactivate.user_is_active = False
        user_to_deactivate.user_email = None
        db.commit()
        return user_to_deactivate
    return None