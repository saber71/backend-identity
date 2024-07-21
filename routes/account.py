from typing import Optional

import bridge
import fastapi
import storage
from fastapi import APIRouter
from fastapi import Response
from pydantic import BaseModel

import constants
import database
from database import Account, Role, Permission, RolePermissions

router = APIRouter(prefix="/account")


# 验证账号的请求数据
class VerifyAccount(BaseModel):
    name: str  # 账户名称
    password: str  # 账户密码


# 用于表示创建账户时的请求数据
class CreateAccount(VerifyAccount):
    role_id: int  # 角色id
    properties: Optional[dict]  # 保存账户的额外属性，如年龄、性别等


# 账户的详细数据
class AccountDetail(BaseModel, Account):
    role: Role  # 对应的角色
    permissions: list[Permission]  # 对应的权限
    properties: Optional[dict]  # 保存账户的额外属性，如年龄、性别等
    pass


# 定义创建账户的API路由
@router.post("/create")
def create(data: CreateAccount):
    """
    创建一个新的账户。

    使用提供的账户名称和密码创建一个账户实体，并将其存储在数据库中。
    同时，将其他属性存储在持久化存储中。
    返回新建账号的id

    参数:
    - data: CreateAccount类型的实例，包含账户名称和密码。
    """
    if data.properties and "id" in data.properties:
        raise fastapi.HTTPException(status_code=422, detail="properties中不能包含有id")

    with database.begin() as session, storage.TransactionContext() as ctx:
        role = session.query(Role).filter_by(id=data.role_id).first()
        bridge.assert_not_none(role, detail=f"找不到[{data.role_id}]该角色")
        # 创建一个新的账户实体和对应角色映射
        account = Account(name=data.name, role_id=data.role_id)
        session.add(account)
        ctx.save(
            {
                "name": constants.STORAGE_ACCOUNT_PROPERTIES_NAME,
                "value": [
                    {**(data.properties if data.properties else {}), "id": account.id}
                ],
            }
        )
        bridge.post("/auth/save", data={"id": account.id, "password": data.password})

    return Response(account.id, media_type="text/plain")


# 定义删除账户的API路由
@router.post("/delete")
def delete(id: str):
    """
    删除一个账户。

    根据提供的账户ID从数据库中删除对应的账户实体。
    同时，从持久化存储中删除账户的ID和密码和相关属性。

    参数:
    - id: 要删除的账户的ID。
    """
    with database.begin() as session, storage.TransactionContext() as ctx:
        session.query(Account).filter_by(id=id).delete()
        bridge.post("/auth/delete", params={"id": id})
        ctx.delete({"name": constants.STORAGE_ACCOUNT_PROPERTIES_NAME, "id": id})

    return "ok"


@router.post("/verify")
def verify(data: VerifyAccount):
    """
    用户身份验证。

    该函数通过接收一个包含用户名和密码的数据对象，验证用户身份并在响应头设置认证令牌。

    :param data: 类型为AuthAccount的实例，包含用户名和密码。
    :raises fastapi.HTTPException: 如果账号不存在或认证失败，则抛出HTTP异常。
    """
    # 初始化数据库会话
    session = database.session()
    # 尝试根据用户名查询账号信息
    account = session.query(Account).filter_by(name=data.name).first()
    # 如果账号不存在，则抛出未认证异常
    bridge.assert_not_none(account, detail="账号不存在", status_code=401)
    # 调用远程服务验证用户名和密码
    res = bridge.post(
        "/auth/verify", json={"id": account.id, "password": data.password}
    )
    # 检查验证结果，如果失败则抛出异常
    bridge.check_res(res)
    # 调用远程服务生成JWT令牌
    res = bridge.post("/auth/jwt/encode", json={"account_id": account.id})
    # 检查令牌生成结果，如果失败则抛出异常
    bridge.check_res(res)
    # 返回生成的JWT令牌
    return Response("ok", headers={"Authorization": res.text})


@router.get("/detail")
def get_detail(id: str):
    """
    根据账号ID获取账号详情。

    本函数通过ID从数据库中查询账号信息，并结合存储系统中账号的属性信息，
    组装成账号详情对象返回。

    参数:
    - id: 账号的唯一标识字符串。

    返回:
    - 账号详情对象，包含账号的基本信息和属性信息。
    """
    # 初始化数据库会话
    session = database.session()
    # 根据ID查询账号信息
    account = session.query(Account).filter_by(id=id).first()
    # 确保账号存在，否则抛出异常
    bridge.assert_not_none(
        account,
        detail="账号不存在",
    )
    role = session.query(Role).filter_by(id=account.role_id).first()
    bridge.assert_not_none(role, detail="角色不存在")
    # 从存储系统中获取账号的属性信息
    res = storage.get({"name": constants.STORAGE_ACCOUNT_PROPERTIES_NAME, "id": id})
    permissions = (
        session.query(Permission)
        .join(RolePermissions, RolePermissions.permission_id == Permission.id)
        .filter(RolePermissions.role_id == account.role_id)
        .all()
    )
    # 将账号信息和属性信息合并，组装成账号详情对象
    account_detail = bridge.assign(
        AccountDetail(),
        account,
        {"properties": res.json(), "role": role, "permissions": permissions},
    )
    # 返回账号详情对象
    return account_detail
