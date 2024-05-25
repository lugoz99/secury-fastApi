from fastapi import Depends, HTTPException, Request, status
from models.Permission import Permission
from models.RolPermission import RolPermission
from services.auth import get_current_user
from models.User import User
from database.db import get_db
from sqlalchemy.orm import Session
import re


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
