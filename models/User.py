from sqlalchemy import Column, ForeignKey, Integer, String
from database.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    id_rol = Column(Integer, ForeignKey("rols.id"))
    Rol = relationship("Rol", cascade="all,delete")
