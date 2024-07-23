import bridge
from fastapi import APIRouter

import database
import routes.permission
from database import Role

router = APIRouter(prefix="/role")


@router.get("/get")
def get(id: int):
    session = database.session()
    role = session.query(Role).filter_by(id=id).first()
    bridge.assert_not_none(role, detail="角色不存在")
    return role


@router.get("/detail")
def detail(id: int):
    role = get(id)
    permissions = routes.permission.search(role_id=id)
    return {"role": role, "permissions": permissions}
