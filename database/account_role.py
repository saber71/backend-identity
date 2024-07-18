from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import mapped_column

from database import Base


# 账号角色关系表
class AccountRole(Base):
    __tablename__ = "account_role"

    id = mapped_column(String, primary_key=True, autoincrement=True)
    account_id = mapped_column(String, ForeignKey("account.id"), comment="账号id")
    role_id = mapped_column(String, ForeignKey("role.id"), comment="角色id")
    update_time = mapped_column(DateTime, comment="更新时间")
    create_time = mapped_column(DateTime, comment="创建时间")

    __table_args__ = UniqueConstraint(
        "role_id", "account_id", name="unique_account_role"
    )
