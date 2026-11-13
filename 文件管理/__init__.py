from 自定义http服务器 import *
from 常量与配置 import *
from .处理登录 import 处理登录请求
from .处理GET import 处理GET请求
from .处理POST import 处理POST请求
from .处理PUT import 处理PUT请求
from .处理DELETE import 处理DELETE请求

def 处理文件管理请求(
    存储路径: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    相对URL = 请求.相对URL[13:]
    if not 相对URL.startswith('/'):
        相对URL = '/' + 相对URL

    if 相对URL in {'/login', '/login/', '/login/verify_key'}:
        处理登录请求(相对URL, 请求, 操作器)
        return

    if 文件管理密码:
        if 'key' in 请求.参数:
            实际密码 = 请求.参数['key']
            if 实际密码 != 文件管理密码:
                操作器.发送响应(403)
                操作器.结束头()
                操作器.写入(页面_403.format('密码错误'))
                日志.记录(f'由于密码错误, 发送 403 错误响应')
                return
        else:
            操作器.发送重定向('/file_manager/login')
            return

    if 请求.类型 == 'GET':
        处理GET请求(存储路径, 相对URL, 请求, 操作器)
    elif 请求.类型 == 'POST':
        处理POST请求(存储路径, 相对URL, 请求, 操作器)
    elif 请求.类型 == 'PUT':
        处理PUT请求(存储路径, 相对URL, 请求, 操作器)
    elif 请求.类型 == 'DELETE':
        处理DELETE请求(存储路径, 相对URL, 请求, 操作器)
    else:
        操作器.发送响应(405)
        操作器.结束头()
        操作器.写入(页面_405.format(请求.类型))
        日志.记录(f'由于请求类型 {请求.类型} 不支持, 发送 405 错误响应')