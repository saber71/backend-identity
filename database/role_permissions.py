from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import mapped_column

from database import Base


# 角色权限关联表
class RolePermissions(Base):
    __tablename__ = "role_permissions"

    id = mapped_column(String, primary_key=True, autoincrement=True)
    role_id = mapped_column(String, ForeignKey("role.id"), comment="角色id")
    permission_id = mapped_column(
        String,
        ForeignKey("permission.id"),
        comment="权限id",
    )
    update_time = mapped_column(DateTime, comment="更新时间")
    create_time = mapped_column(DateTime, comment="创建时间")

    __table_args__ = UniqueConstraint(
        "role_id", "permission_id", name="unique_role_permission"
    )
