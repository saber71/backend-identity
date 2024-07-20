from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column

from database import Base, TimestampMixin


# 角色权限关联类，用于定义角色与权限之间的映射关系
class RolePermissions(Base, TimestampMixin):
    # 表名
    __tablename__ = "role_permissions"

    # 关联角色表的外键，标识角色id
    role_id = mapped_column(
        Integer, ForeignKey("role.id"), comment="角色id", primary_key=True
    )
    # 关联权限表的外键，标识权限id
    permission_id = mapped_column(
        Integer, ForeignKey("permission.id"), comment="权限id", primary_key=True
    )
