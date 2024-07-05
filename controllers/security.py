from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import TokenBase
from services.auth import generate_token
from sqlalchemy.orm import session


async def login_for_access_token(db: session, form_data: OAuth2PasswordRequestForm):
    access_token = generate_token(db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}
