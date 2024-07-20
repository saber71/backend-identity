import datetime
import os

from sqlalchemy import create_engine, Engine, DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
    mapped_column,
    declared_attr,
)

# 配置身份验证数据库的路径
option = {"path": os.path.join(os.path.expanduser("~"), "identity.sqlite")}

# 全局变量，用于存储数据库引擎实例
__engine__ = None

# 全局变量，用于存储数据库会话实例
__session_cls__ = None


def engine() -> Engine:
    """
    获取数据库引擎实例。

    如果尚未创建实例，则创建并返回一个新的数据库引擎实例。
    使用SQLite数据库，数据库文件位于用户的主目录下。

    :return: 数据库引擎实例
    """
    global __engine__
    if __engine__ is None:
        __engine__ = create_engine("sqlite:///" + option["path"])
    return __engine__


def session_cls() -> sessionmaker[Session]:
    """
    获取数据库会话类
    """
    global __session_cls__
    if __session_cls__ is None:
        __session_cls__ = sessionmaker(engine())
    return __session_cls__


def begin():
    """
    开始一个新的数据库事务。

    :return: 事务对象
    """
    return session_cls().begin()


def session() -> Session:
    """
    创建并返回一个会话实例
    """
    return session_cls()()


# 定义基类，所有数据库模型类将继承自这个基类
class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """
    时间戳混合类，用于在继承该类的模型中自动添加创建时间和更新时间的字段。
    这个类利用SQLAlchemy的declared_attr装饰器动态定义属性，以便在数据库表中包含时间戳信息。
    """

    @declared_attr
    def create_time(self):
        """
        自动创建时间属性，记录实体的创建时间。

        返回:
            DateTime类型的映射列，默认值为当前时间。
        """
        return mapped_column(
            DateTime,
            default=datetime.datetime.now(),
            comment="创建时间",
        )

    @declared_attr
    def update_time(self):
        """
        自动更新时间属性，记录实体的最后更新时间。

        返回:
            DateTime类型的映射列，默认值为当前时间，每次更新时也会自动更新。
        """
        return mapped_column(
            DateTime,
            default=datetime.datetime.now(),
            comment="更新时间",
            onupdate=datetime.datetime.now,
        )
