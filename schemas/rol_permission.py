from datetime import datetime
from typing import List
from pydantic import BaseModel


class RolPermissionBase(BaseModel):
    rol_id: int
    permission_id: int
    date: datetime


class RolPermissionsCreate(BaseModel):
    id_rol: int
    permissions: List[int]
