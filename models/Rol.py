from sqlalchemy import Column, Integer, String
from database.db import Base


class Rol(Base):
    __tablename__ = "rols"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
