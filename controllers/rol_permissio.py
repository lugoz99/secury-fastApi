from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models.RolPermission import RolPermission
from schemas.rol_permission import RolPermissionBase, RolPermissionsCreate


class RolPermissionController:
    def get_all(self, db: Session):
        return db.query(RolPermission).all()

    def get_by_id(self, db: Session, id: int):
        rol_permission = db.query(RolPermission).filter(RolPermission.id == id).first()
        if not rol_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="RolPermission not found"
            )
        return rol_permission

    def create(self, db: Session, rol_permission: RolPermissionBase):
        new_rol_permission = RolPermission(**rol_permission.model_dump())
        db.add(new_rol_permission)
        db.commit()
        db.refresh(new_rol_permission)
        return new_rol_permission

    def create_multiple(self, db: Session, rol_permissions: RolPermissionsCreate):
        for id_permission in rol_permissions.permissions:
            new_rol_permission = RolPermission(
                id_rol=rol_permissions.id_rol, id_permission=id_permission
            )
            db.add(new_rol_permission)
        db.commit()
        return {"Msg": "Permisos creados"}

    def update(self, db: Session, id: int, rol_permission: RolPermissionBase):
        existing_rol_permission = (
            db.query(RolPermission).filter(RolPermission.id == id).first()
        )
        if not existing_rol_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="RolPermission not found"
            )
        for key, value in rol_permission.dict().items():
            # establecer atributos actualizandolos
            setattr(existing_rol_permission, key, value)
        db.commit()
        return existing_rol_permission

    def delete(self, db: Session, id: int):
        existing_rol_permission = (
            db.query(RolPermission).filter(RolPermission.id == id).first()
        )
        if not existing_rol_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="RolPermission not found"
            )
        db.delete(existing_rol_permission)
        db.commit()

    def get_permissions_by_rol(self, db: Session, id_rol: int):
        rol_permissions = (
            db.query(RolPermission).filter(RolPermission.id_rol == id_rol).all()
        )
        permissions = [rol_permission.Permission for rol_permission in rol_permissions]
        return permissions

    from sqlalchemy import and_

    def get_role_permission(self, db: Session, role_id: int, permission_id: int):
        role_permission = (
            db.query(RolPermission)
            .filter(
                and_(
                    RolPermission.id_rol == role_id,
                    RolPermission.id_permission == permission_id,
                )
            )
            .first()
        )
        return role_permission
