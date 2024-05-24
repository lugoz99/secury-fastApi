from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.rol import RolBase, RolOut
from controllers.rol import RolController
from schemas.user import UserBase
from services.auth import get_current_user_token, validate_role_permission

router = APIRouter(
    tags=["rol"],
)


@router.post("/rol")
async def new_rol(
    rol: RolBase,
    db: Session = Depends(get_db),
    _=Depends(get_current_user_token),
):
    controller = RolController()
    record = controller.create_record(db, rol)
    return JSONResponse(status_code=200, content=jsonable_encoder(record))


@router.get("/items/")
async def read_items(validate: bool = Depends(validate_role_permission)):
    return {"message": "User has the necessary permissions"}
