import re
from time import timezone
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.db import get_db
from models.User import User
from models.RolPermission import RolPermission
from datetime import datetime, timedelta, timezone

from config.setting import settings
from fastapi import Depends, HTTPException, Request, status

from schemas.auth import TokenData
from models.Permission import Permission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_password_hashed(password: str):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def generate_token(db: Session, username, password):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"id": user.id, "username": user.email, "rol": user.id},
        expires_delta=access_token_expires,
    )


def validate_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        expire = payload.get("exp")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
            )

        expire_datetime = datetime.fromtimestamp(expire)
        expire_datetime = expire_datetime.replace(
            tzinfo=timezone.utc
        )  # Corrección aquí
        if expire_datetime < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
            )
        return TokenData(
            id=str(payload["id"]), username=payload["username"], rol=str(payload["rol"])
        )  # Devuelve una instancia de TokenData
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )


async def get_current_user_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"},
    )
    try:
        token_data = validate_token(token)
        user = db.query(User).filter(User.id == token_data.id).first()
        return user
    except jwt.PyJWTError:
        raise credentials_exception


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = token.split("Bearer ")[1]
    user_data = validate_token(token)
    user = db.query(User).filter(User.id == user_data.id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_new_url(url: str) -> str:
    parts = url.split("/")
    new_url_parts = []
    for part in parts[1:]:
        if re.search(r"\d", part):
            new_url_parts.append("?")
        else:
            new_url_parts.append(part)
    new_url = "/".join(new_url_parts)
    return new_url


def validate_role_permission(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url = request.url.path
    method = request.method
    url = get_new_url(url)
    print("URL", url)
    print("METHOD", method)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission for this page se",
        )
    permission = (
        db.query(Permission)
        .filter(Permission.url == url and Permission.method == method)
        .first()
    )
    print("PERMISION", permission)

    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission for this page permissions",
        )

    role_permission = (
        db.query(RolPermission)
        .filter(
            RolPermission.id_rol == current_user.id_rol,
            RolPermission.id_permission == permission.id,
        )
        .first()
    )

    if role_permission is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission for this page",
        )

    return True
