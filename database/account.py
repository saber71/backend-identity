import uuid

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column

import database


# 账号
class Account(database.Base, database.TimestampMixin):
    __tablename__ = "account"

    id = mapped_column(String, primary_key=True, default=uuid.uuid4())
    name = mapped_column(String, nullable=False, unique=True, comment="账号名")
    role_id = mapped_column(Integer, ForeignKey("role.id"), comment="角色id")
