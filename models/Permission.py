from sqlalchemy import Column, Integer, String, UniqueConstraint
from database.db import Base


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    method = Column(String)
    menuItem = Column(String)
