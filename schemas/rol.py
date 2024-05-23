from typing import Optional
from pydantic import BaseModel


class RolBase(BaseModel):
    name: str
    description: str
