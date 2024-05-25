from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.permission import PermissionController
from schemas.permission import PermissionBase
from database.db import get_db
from services.permission_access import validate_role_permission

router = APIRouter(
    tags=["permissions"],
)


@router.post("/permissions", response_model=dict, status_code=200)
def create_permission(
    record: PermissionBase,
    db: Session = Depends(get_db),
    _: bool = Depends(validate_role_permission),  # Add this line
):
    controller = PermissionController()
    return JSONResponse(
        status_code=200, content=jsonable_encoder(controller.create_record(db, record))
    )


@router.get("/permissions")
def get_all_permissions(
    db: Session = Depends(get_db), _: bool = Depends(validate_role_permission)
):
    controller = PermissionController()
    return JSONResponse(
        status_code=200, content=jsonable_encoder(controller.get_all(db))
    )


@router.get("/permissions/{id}")
def get_permission(id: int, db: Session = Depends(get_db)):
    controller = PermissionController()
    return controller.get_by_id(db, id)


@router.delete("/permissions/{id}")
def delete_permission(
    id: int, db: Session = Depends(get_db), _: bool = Depends(validate_role_permission)
):
    controller = PermissionController()
    return controller.delete(db, id)
