from sqlalchemy import Column, ForeignKey, Integer, String
from database.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship  # Import the relationship function


class RolPermission(Base):
    __tablename__ = "RolPermissions"
    id = Column(Integer, primary_key=True)
    id_permission = Column(String, ForeignKey("permissions.id"))
    id_rol = Column(Integer, ForeignKey("rols.id"))
    date = datetime
    Rol = relationship("Rol", back_populates="permissions", cascade="all,delete")
    Permission = relationship("Permission", back_populates="rols", cascade="all,delete")
