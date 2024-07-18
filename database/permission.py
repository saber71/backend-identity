from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

import database


# 权限
class Permission(database.Base):
    __tablename__ = ("permission"
                     "")
    id = mapped_column(String, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, comment="权限名")
    description = mapped_column(String, comment="权限描述")
    create_time = mapped_column(DateTime, comment="创建时间")
    update_time = mapped_column(DateTime, comment="更新时间")
