from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

import database


# 账号
class Account(database.Base):
    __tablename__ = "account"

    id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False, unique=True, comment="账号名")
    create_time = mapped_column(DateTime, comment="创建时间")
    update_time = mapped_column(DateTime, comment="更新时间")
