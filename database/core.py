import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# 配置身份验证数据库的路径
option = {"path": os.path.join(os.path.expanduser("~"), "identity.sqlite")}

# 全局变量，用于存储数据库引擎实例
__engine__ = None

# 全局变量，用于存储数据库会话实例
__session__ = None


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


def session() -> sessionmaker[Session]:
    """
    获取数据库会话实例。

    如果尚未创建实例，则创建并返回一个新的会话实例。
    会话实例是用于与数据库进行交互的。

    :return: 数据库会话实例
    """
    global __session__
    if __session__ is None:
        __session__ = sessionmaker(engine())
    return __session__


def begin():
    """
    开始一个新的数据库事务。

    :return: 事务对象
    """
    return session().begin()


# 定义基类，所有数据库模型类将继承自这个基类
class Base(DeclarativeBase):
    pass
