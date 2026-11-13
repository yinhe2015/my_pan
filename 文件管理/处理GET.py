from 自定义http服务器 import *
from 常量与配置 import *
from 工具.从参数获取path import 从参数获取path
from urllib.parse import quote
import zipfile
import io

浏览目录模板_html_路径 = os.path.join(静态目录, '文件管理', '浏览目录模板.html')

def 处理GET请求(
    存储路径: str,
    相对URL: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    if 相对URL == '/' or 相对URL == '/index.html':
        if 文件管理密码:
            操作器.发送重定向('/file_manager/files/?key=' + 文件管理密码)
        else:
            操作器.发送重定向('/file_manager/files/')
    elif 相对URL.startswith('/files/'):
        原始路径 = 相对URL[7:]
        if '..' in 原始路径:
            操作器.发送响应(403)
            操作器.结束头()
            操作器.写入(页面_403.format(f'{相对URL} (包含上级目录 ..)'))
            日志.记录(f'由于尝试访问上级目录, 发送 403 错误响应')
            return
        路径 = 原始路径.replace('/', os.path.sep)
        路径 = os.path.join(存储路径, 路径)
        if os.path.exists(路径):
            if os.path.isdir(路径):
                with open(浏览目录模板_html_路径, 'r', encoding=默认编码) as 文件:
                    浏览目录模板 = 文件.read()
                操作器.发送响应(200)
                操作器.发送头('Content-type', MIME类型映射['html'])
                操作器.结束头()
                操作器.写入(浏览目录模板.replace(':::名称:::', 名称)
                       .replace('\'占位符_由后端动态替换\'', repr(原始路径)))
            else:
                MIME类型 = 获取MIME类型(路径, 默认值=None) # None = 不发送 MIME 类型
                操作器.发送文件(路径, MIME类型=MIME类型, 显示进度条=显示进度条, 额外头={
                    'Content-type': f'charset={默认编码}'
                })
        else:
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(原始路径))
            日志.记录(f'由于路径 {路径} 不存在, 发送 404 错误响应')
    elif 相对URL == '/api/list_dir':
        路径 = 从参数获取path(存储路径, 请求.参数, 操作器)
        if not 路径:
            return
        if not os.path.exists(路径):
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(路径))
            日志.记录(f'由于路径 {路径} 不存在, 发送 404 错误响应')
            return
        if not os.path.isdir(路径):
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format(f'{路径} 不是目录'))
            日志.记录(f'由于 {路径} 不是目录, 发送 400 错误响应')
            return
        日志.记录(f'目录列表: {路径}')
        文件列表 = []
        for 文件 in os.listdir(路径):
            文件路径 = os.path.join(路径, 文件)
            属性 = os.stat(文件路径)
            是目录 = os.path.isdir(文件路径)
            文件列表.append({
                'name': 文件,
                'size': 属性.st_size if not 是目录 else 0,
                'is_dir': 是目录,
                'modified': 属性.st_mtime,
            })
        操作器.发送JSON({'files': 文件列表})
        日志.记录(f'发送目录列表: {文件列表}')
    elif 相对URL == '/api/download':
        路径 = 从参数获取path(存储路径, 请求.参数, 操作器)
        if not 路径:
            return
        if os.path.exists(路径):
            if os.path.isdir(路径):
                操作器.发送响应(200)
                操作器.发送头('Content-Disposition', f'attachment; filename="{quote(os.path.basename(路径))}.zip"')
                操作器.发送头('Content-Type', 'application/zip')
                IO = io.BytesIO()
                with zipfile.ZipFile(IO, 'w', zipfile.ZIP_DEFLATED) as zip文件:
                    for 根目录, 目录列表, 文件列表 in os.walk(路径):
                        for 文件 in 文件列表:
                            文件路径 = os.path.join(根目录, 文件)
                            归档路径 = os.path.relpath(文件路径, 路径)
                            zip文件.write(文件路径, 归档路径)
                        for 目录 in 目录列表:
                            文件路径 = os.path.join(根目录, 目录)
                            归档路径 = os.path.relpath(文件路径, 路径)
                            zip文件.mkdir(归档路径)
                操作器.发送头('Content-Length', str(IO.tell()))
                操作器.结束头()
                操作器.写入(IO.getvalue())
                IO.close()
            else:
                操作器.发送文件(路径, MIME类型='application/octet-stream', 发送文件名=True, 显示进度条=显示进度条)
        else:
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(路径))
            日志.记录(f'由于路径 {路径} 不存在, 发送 404 错误响应')
    else:
        操作器.发送响应(404)
        操作器.结束头()
        操作器.写入(页面_404.format(相对URL))
        日志.记录(f'由于路径 {相对URL} 不存在, 发送 404 错误响应')