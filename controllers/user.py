from fastapi import HTTPException
from models.User import User
from schemas.user import UserBase
from sqlalchemy.orm import Session


class UserController:

    def get_all(self, bd: Session):
        return bd.query(User).all()

    def create_record(self, bd: Session, user: UserBase):
        new_user = User(**user.model_dump())
        bd.add(new_user)
        bd.commit()
        bd.refresh(new_user)
        return new_user

    def get_by_id(self, db: Session, id: int):
        record = db.query(User).filter(User.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail="User not found")
        return
