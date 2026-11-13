from 自定义http服务器 import *
from 常量与配置 import *
import shutil
import os

def 处理POST请求(
    存储路径: str,
    相对URL: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    if 相对URL == '/api/move':
        if 'path' not in 请求.参数 or 'targetPath' not in 请求.参数:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('请求必须包含 ?path=路径&targetPath=目标路径'))
            日志.记录(f'由于 请求没有包含 path 或 targetPath 参数, 发送 400 错误响应')
            return
        路径 = 请求.参数['path']
        if '..' in 路径:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('POST 请求路径不能包含 ../'))
            日志.记录(f'由于 POST 请求路径包含 ../, 发送 400 错误响应')
            return
        路径 = 路径.replace('/', os.path.sep)
        目标路径 = 请求.参数['targetPath']
        if '..' in 目标路径:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('POST 请求目标路径不能包含 ../'))
            日志.记录(f'由于 POST 请求目标路径包含 ../, 发送 400 错误响应')
            return
        目标路径 = 目标路径.replace('/', os.path.sep)
        目标路径 = os.path.join(存储路径, 目标路径, os.path.basename(路径))
        旧路径 = os.path.join(存储路径, 路径)
        if not os.path.exists(旧路径):
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(旧路径))
            日志.记录(f'由于路径 {旧路径} 不存在, 发送 404 错误响应')
            return
        if os.path.exists(目标路径):
            操作器.发送响应(409)
            操作器.结束头()
            操作器.写入(页面_409.format(目标路径))
            日志.记录(f'由于 请求尝试移动到已存在的路径 {目标路径}, 发送 409 错误响应')
            return
        shutil.move(旧路径, 目标路径)
        操作器.发送响应(200)
        操作器.结束头()
        操作器.写入('移动成功')
        日志.记录(f'移动 {旧路径} 到 {目标路径}')
    elif 相对URL == '/api/rename':
        if 'path' not in 请求.参数 or 'newName' not in 请求.参数:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('请求必须包含 ?path=路径&newName=新文件名'))
            日志.记录(f'由于 请求没有包含 path 或 newName 参数, 发送 400 错误响应')
            return
        路径 = 请求.参数['path']
        if '..' in 路径:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('POST 请求路径不能包含 ../'))
            日志.记录(f'由于 POST 请求路径包含 ../, 发送 400 错误响应')
            return
        路径 = 路径.replace('/', os.path.sep)
        新名称 = 请求.参数['newName']

        旧路径 = os.path.join(存储路径, 路径)
        新路径 = os.path.join(os.path.dirname(旧路径), 新名称)
        if not os.path.exists(旧路径):
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(旧路径))
            日志.记录(f'由于路径 {旧路径} 不存在, 发送 404 错误响应')
            return
        if os.path.exists(新路径):
            操作器.发送响应(409)
            操作器.结束头()
            操作器.写入(页面_409.format(新路径))
            日志.记录(f'由于 请求尝试重命名为已存在的文件 {新路径}, 发送 409 错误响应')
            return
        os.rename(旧路径, 新路径)
        操作器.发送响应(200)
        操作器.结束头()
        操作器.写入('重命名成功')
        日志.记录(f'重命名 {旧路径} 为 {新路径}')
    elif 相对URL == '/api/mkdir':
        if 'path' not in 请求.参数 or 'name' not in 请求.参数:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('请求必须包含 ?path=路径&name=名称'))
            日志.记录(f'由于 请求没有包含 path 或 name 参数, 发送 400 错误响应')
            return
        路径 = 请求.参数['path']
        if '..' in 路径:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('POST 请求路径不能包含 ../'))
            日志.记录(f'由于 POST 请求路径包含 ../, 发送 400 错误响应')
            return
        路径 = 路径.replace('/', os.path.sep)
        路径 = os.path.join(存储路径, 路径)
        名称 = 请求.参数['name']
        if not 名称:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('name不能为空'))
            日志.记录(f'由于 请求 name 参数为空 {请求.参数['path']}, 发送 400 错误响应')
            return
        if os.path.exists(路径):
            if not os.path.isdir(路径):
                操作器.发送响应(409)
                操作器.结束头()
                操作器.写入(页面_409.format(路径))
                日志.记录(f'由于 请求尝试在文件中创建目录 {请求.参数['path']}, 发送 409 错误响应')
                return
        目录路径 = os.path.join(路径, 名称)
        try:
            os.mkdir(目录路径)
        except FileExistsError:
            操作器.发送响应(409)
            操作器.结束头()
            操作器.写入(页面_409.format(目录路径))
            日志.记录(f'由于 请求尝试创建已存在的目录 {目录路径}, 发送 409 错误响应')
            return
        操作器.发送响应(200)
        操作器.结束头()
        操作器.写入('目录创建成功')
        日志.记录(f'创建目录 {目录路径}')
    else:
        操作器.发送响应(404)
        操作器.结束头()
        操作器.写入(页面_404.format(相对URL))
        日志.记录(f'由于路径 {相对URL} 不存在, 发送 404 错误响应')
        return