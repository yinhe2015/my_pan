from 自定义http服务器 import *
from 常量与配置 import *
from 工具.从参数获取path import 从参数获取path
import shutil
import os

def 处理DELETE请求(
    存储路径: str,
    相对URL: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    if 相对URL == '/api/delete':
        路径 = 从参数获取path(存储路径, 请求.参数, 操作器)
        if not 路径:
            return
        if not os.path.exists(路径):
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(f'文件 {路径} 不存在')
            日志.记录(f'由于 DELETE 请求尝试删除不存在的文件 {路径}, 发送 404 错误响应')
            return
        
        try:
            if os.path.isdir(路径):
                shutil.rmtree(路径)
            else:
                os.remove(路径)
        except Exception:
            import traceback
            错误信息 = traceback.format_exc()
            日志.错误(f'删除 {路径} 失败: {错误信息}')
            操作器.发送响应(500)
            操作器.结束头()
            操作器.写入(f'文件删除失败: {错误信息}')
            return

        操作器.发送响应(200)
        操作器.结束头()
        操作器.发送JSON('删除成功')
        日志.记录(f'发送 200, 文件删除成功: {路径}')
    else:
        操作器.发送响应(404)
        操作器.结束头()
        操作器.写入(f'未找到路径 {相对URL}')
        日志.记录(f'由于未找到路径 {相对URL}, 发送 404 错误响应')