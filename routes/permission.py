from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel

import database
from database import Permission

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
