from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from controllers.security import login_for_access_token
from sqlalchemy.orm import Session

from database.db import get_db

router = APIRouter(
    tags=["user"],
)


@router.post("/login")
async def authenticate(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    login = await login_for_access_token(db, form_data)
    return login
