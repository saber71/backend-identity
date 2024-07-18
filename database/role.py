from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

from database import Base


# 角色
class Role(Base):
    __tablename__ = "role"
    id = mapped_column(String, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, comment="角色名")
    description = mapped_column(String, comment="角色描述")
    create_time = mapped_column(DateTime, comment="创建时间")
    update_time = mapped_column(DateTime, comment="更新时间")
