import sys
import os
sys.path.append(os.path.join(os.path.expanduser('~'), 'pylib'))
sys.path.append(os.path.join(os.path.expanduser('~'), 'disk-d', 'pylib'))

from 自定义http服务器 import *
from 常量与配置 import *
from 处理管理请求 import 处理管理请求
from 文件管理 import 处理文件管理请求
import os

index_html_路径 = os.path.join(静态目录, 'index.html')

def 处理函数(
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    相对URL = 请求.相对URL

    if 相对URL.startswith('//'):
        日志.记录(f'相对URL {相对URL} 不能以 // 开头')
        操作器.发送响应(400)
        操作器.结束头()
        操作器.写入(页面_400.format(f'相对URL {相对URL} 不能以 // 开头'))
        日志.记录(f'由于相对URL {相对URL} 不能以 // 开头, 发送 400 错误响应')
        return
    
    if 相对URL.startswith('/manage'): # 管理功能
        处理管理请求(请求, 操作器)
        return
    
    if 相对URL.startswith('/file_manager'): # 文件管理功能
        处理文件管理请求(存储路径, 请求, 操作器)
        return

    if 请求.类型 == 'GET':
        if 相对URL == '/' or 相对URL == '/index.html':
            操作器.发送文件(index_html_路径, MIME类型=MIME类型映射['html'], 显示进度条=显示进度条)
        elif 相对URL.startswith('/static/'):
            原始路径 = 相对URL[8:].replace('/', os.path.sep)
            路径 = os.path.join(静态目录, 原始路径)
            if not os.path.exists(路径):
                操作器.发送响应(404)
                操作器.结束头()
                操作器.写入(页面_404.format(路径))
                日志.记录(f'由于资源 {路径} 不存在, 发送 404 错误响应')
                return
            操作器.发送文件(路径, 发送文件名=True, 显示进度条=显示进度条)
        elif 相对URL == '/favicon.ico':
            if favicon_ico:
                操作器.发送响应(200)
                操作器.发送头('Content-type', 'image/x-icon')
                操作器.结束头()
                操作器.写入(favicon_ico)
                日志.记录(f'发送 favicon.ico')
            else:
                操作器.发送响应(404)
                操作器.结束头()
                操作器.写入(页面_404.format('favicon.ico'))
                日志.记录(f'由于 favicon.ico 不存在, 发送 404 错误响应')

if __name__ == '__main__':
    服务器 = 自定义HTTP服务器(处理函数, 端口=8080, 日志=日志)
    服务器.启动()
