from models.Permission import Permission as permissionModel
from schemas.permission import PermissionBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError


class PermissionController:

    def create_record(self, db: Session, permission: PermissionBase):
        try:
            existing_permission = (
                db.query(permissionModel)
                .filter(
                    permissionModel.url == permission.url,
                    permissionModel.method == permission.method,
                )
                .first()
            )
            if existing_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Permission already exists",
                )
            permission_model = permissionModel(**permission.model_dump())
            db.add(permission_model)
            db.commit()
            db.refresh(permission_model)
            return permission_model
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_all(self, db: Session):
        """
        Fetch all Permission records from the database.

        Args:
            db (Session): database session

        Returns:
            List[Permission]: list of Permission records

        Raises:
            HTTPException: if an error occurs while fetching the records.
        """
        try:
            return db.query(permissionModel).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_by_id(self, db: Session, id: int):
        record = db.query(permissionModel).filter(permissionModel.id == id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            )
        return record

    def get_permission(self, db: Session, url: str, method: str):
        permission = (
            db.query(permissionModel)
            .filter(permissionModel.url == url, permissionModel.method == method)
            .first()
        )
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            )
        return permission
