from typing import Optional
from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    username: Optional[str] = None
    rol: str
