import datetime
from typing import Optional

import fastapi
import storage
from fastapi import APIRouter
from pydantic import BaseModel

import constants
import database
from database import Account

router = APIRouter(prefix="/account")


# 用于表示创建账户时的请求数据
class CreateAccount(BaseModel):
    name: str  # 账户名称
    password: str  # 账户密码
    properties: Optional[dict]  # 保存账户的额外属性，如年龄、性别等


# 定义创建账户的API路由
@router.post("/create")
def create(data: CreateAccount):
    if data.properties and "id" in data.properties:
        raise fastapi.HTTPException(status_code=422, detail="properties中不能包含有id")
    """
    创建一个新的账户。

    使用提供的账户名称和密码创建一个账户实体，并将其存储在数据库中。
    同时，将账户ID和密码存储在持久化存储中。

    参数:
    - data: CreateAccount类型的实例，包含账户名称和密码。
    """
    with database.begin() as session:
        # 创建一个新的账户实体
        account = Account(
            name=data.name,
            update_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # 将账户实体添加到数据库会话中，准备插入数据库
        session.add(account)
        storage.save(
            {
                "name": constants.STORAGE_NAME,
                "value": [{"id": account.id, "password": data.password}],
            }
        )
        storage.save(
            {
                "name": constants.STORAGE_ACCOUNT_PROPERTIES_NAME,
                "value": [
                    {**(data.properties if data.properties else {}), "id": account.id}
                ],
            }
        )


# 定义删除账户的API路由
@router.post("/delete")
def remove(id: str):
    """
    删除一个账户。

    根据提供的账户ID从数据库中删除对应的账户实体。
    同时，从持久化存储中删除账户的ID和密码。

    参数:
    - id: 要删除的账户的ID。
    """
    with database.begin() as session:
        session.query(Account).filter_by(id=id).delete()
        storage.delete({"name": constants.STORAGE_NAME, "id": id})
        storage.delete({"name": constants.STORAGE_ACCOUNT_PROPERTIES_NAME, "id": id})
