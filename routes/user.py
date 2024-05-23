from fastapi import APIRouter, HTTPException, Request
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from controllers.user import UserController
from database.db import get_db
from models.User import User
from schemas.user import UserBase

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    tags=["user"],
)

controller = UserController()


@router.get("/users")
def get_all_user(db: Session = Depends(get_db)):
    return controller.get_all()


@router.post("/users")
def new_user(user: UserBase, db: Session = Depends(get_db)):
    return controller.create_record(db, user)


@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return controller.get_by_id(db, id)
