from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel

import database
from database import Permission, RolePermissions

router = APIRouter(prefix="/permission")


# 用于表示创建权限时的请求数据
class CreatePermission(BaseModel):
    name: str
    description: Optional[str]
    pass


@router.post("/create")
def create(data: List[CreatePermission]):
    with database.begin() as session:
        objects = map(
            lambda x: Permission(
                name=x.name,
                description=x.description,
            ),
            data,
        )
        session.add_all(objects)
    return map(lambda p: p.id, objects)


@router.get("/search")
def search(
    name: Optional[str],
    role_id: Optional[int],
    page: Optional[int],
    size: Optional[int] = 10,
):
    session = database.session()
    query = session.query(Permission)
    if role_id is not None:
        query = query.join(
            RolePermissions, RolePermissions.permission_id == Permission.id
        ).filter(RolePermissions.role_id == role_id)
    if name is not None:
        query = query.filter(Permission.name.like(f"%{name}%"))
    if page is not None:
        query = query.offset((page - 1) * size).limit(size)
    return query.all()
