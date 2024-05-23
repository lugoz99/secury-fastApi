from pydantic import BaseModel


class PermissionBase(BaseModel):
    url: str
    method: str
    menuItem: str


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True
