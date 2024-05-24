from typing import Optional
from pydantic import BaseModel


class RolBase(BaseModel):
    name: str
    description: str


class RolOut(RolBase):
    id: int

    class Config:
        orm_mode = True  # Esto permite que Pydantic trabaje con objetos de SQLAlchemy
