from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.rol import RolBase
from controllers.rol import RolController

router = APIRouter(
    tags=["rol"],
)


@router.post("/rol")
async def new_rol(rol: RolBase, db: Session = Depends(get_db)):
    controller = RolController()
    record = controller.create_record(db, rol)
    return JSONResponse(status_code=200, content=jsonable_encoder(record))
