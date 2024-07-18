from fastapi import APIRouter

# 导入数据库模块，用于后续数据库操作
import database

# 初始化API路由器，并设置路由前缀为"/database"
# 这里的目的是为了组织和管理与数据库相关的API端点
router = APIRouter(prefix="/database")


@router.post("/memory")
# 定义一个处理内存数据库配置的端点
# 该端点通过POST请求来切换数据库到内存模式
def memory():
    """
    将数据库配置切换到内存模式。

    本函数不接受任何参数。

    返回值:
    - 字符串"ok"，表示切换操作成功。
    """
    # 将数据库的路径设置为":memory:", 以启用内存数据库
    # 这种配置通常用于测试和开发环境，而不是生产环境
    database.option["path"] = ":memory:"
    return "ok"
