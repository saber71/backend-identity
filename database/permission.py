from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column

import database


# 权限
class Permission(database.Base, database.TimestampMixin):
    __tablename__ = "permission"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, unique=True, nullable=False, comment="权限名")
    description = mapped_column(String, comment="权限描述", default="")
