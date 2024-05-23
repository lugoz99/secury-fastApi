from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    id_rol: int


class TokenData(BaseModel):
    username: str
