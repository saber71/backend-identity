from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, relationship

from database import Base, TimestampMixin


# 角色
class Role(Base, TimestampMixin):
    __tablename__ = "role"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, comment="角色名")
    description = mapped_column(String, comment="角色描述", default="")
    accounts = relationship("Account", back_populates="role")
    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
