from fastapi import HTTPException
from schemas.rol import RolBase
from sqlalchemy.orm import Session
from models.Rol import Rol


class RolController:

    def create_record(self, db: Session, orden: RolBase):
        orden_model = Rol(**orden.model_dump())
        db.add(orden_model)
        db.commit()
        db.refresh(orden_model)
        return orden_model

    def get_all(self, db: Session):
        return db.query(Rol).all()

    def get_by_id(self, db: Session, id: int):
        record = db.query(Rol).filter(Rol.id == id)
        if not record:
            raise HTTPException(status_code=404, detail="Rol not found")
        return record
