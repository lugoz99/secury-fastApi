from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.rol_permissio import RolPermissionController
from schemas.rol_permission import RolPermissionsCreate
from database.db import get_db

router = APIRouter(
    tags=["rol"],
)


@router.post("/rol_permissions")
def create_multiple_rol_permissions(
    rol_permissions: RolPermissionsCreate, db: Session = Depends(get_db)
):
    controller = RolPermissionController()
    return controller.create_multiple(db, rol_permissions)


@router.delete("/rol_permissions/{id}")
def delete_rol_permission(rol_permission_id: int, db: Session = Depends(get_db)):
    controller = RolPermissionController()
    return controller.delete(db, rol_permission_id)
