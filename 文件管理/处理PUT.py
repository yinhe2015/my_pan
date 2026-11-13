from 自定义http服务器 import *
from 常量与配置 import *
import 格式化大小
import os

def 处理PUT请求(
    存储路径: str,
    相对URL: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    if 相对URL == '/api/upload':
        if 'path' not in 请求.参数 or 'name' not in 请求.参数:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('PUT 请求必须包含 ?path=路径&name=文件名'))
            日志.记录(f'由于 PUT 请求没有包含 path 或 name 参数, 发送 400 错误响应')
            return
        路径 = 请求.参数['path']
        if '..' in 路径:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('PUT 请求路径不能包含 ../'))
            日志.记录(f'由于 PUT 请求路径包含 .., 发送 400 错误响应')
            return
        路径 = 路径.replace('/', os.path.sep)
        路径 = os.path.join(存储路径, 路径)
        名称 = 请求.参数['name']
        if not 名称:
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(页面_400.format('PUT 请求必须包含 ?name=文件名'))
            日志.记录(f'由于 PUT 请求 name 参数为空, 发送 400 错误响应')
            return
        路径 = os.path.join(路径, 名称)
        if os.path.exists(路径):
            操作器.发送响应(409)
            操作器.结束头()
            操作器.写入(页面_409.format(路径))
            日志.记录(f'由于 PUT 请求尝试上传已存在的文件 {路径}, 发送 409 错误响应')
            return

        临时路径 = 路径 + '.part' # 使用临时文件存储, 避免不完整文件
        if os.path.exists(临时路径):
            操作器.发送响应(409)
            操作器.结束头()
            操作器.写入(页面_409.format(临时路径))
            日志.记录(f'由于 PUT 请求尝试上传已存在的临时文件 {临时路径}, 发送 409 错误响应')
            return

        try:
            大小字节 = int(请求.头.get('content-length', 0))
        except (KeyError, ValueError):
            操作器.发送响应(400)
            操作器.结束头()
            操作器.写入(f'PUT 请求必须包含 Content-length 头!')
            日志.记录(f'由于 PUT 请求没有包含 Content-length 头, 发送 400 错误响应')
            return

        日志.记录(f'开始接收文件请求, {路径}, 大小: {格式化大小.格式化大小(大小字节)}')

        实际块大小 = 块大小
        已接收 = 0

        try:
            with open(临时路径, 'wb') as 文件:
                while True:
                    if 已接收 >= 大小字节:
                        break
                    elif 实际块大小 > (大小字节 - 已接收):
                        # 最后一块数据可能小于块大小
                        实际块大小 = 大小字节 - 已接收

                    数据 = 操作器.读取(实际块大小)
                    if not 数据:
                        break
                    文件.write(数据)
                    已接收 += len(数据)
                    if 显示进度条:
                        print(
                            f'\r接收 {路径}: {格式化大小.格式化大小(已接收)} / {格式化大小.格式化大小(大小字节)}',
                            end=(' ' * 5), flush=True) # 结尾5个空格, 避免之前的内容残留

            if 显示进度条:
                print('') # 换行, 避免之前的内容残留

            # 接收完成后重命名临时文件
            日志.记录(f'接收 {路径} 成功')
            os.rename(临时路径, 路径)

            # 发送成功响应
            操作器.发送响应(200)
            操作器.结束头()
            操作器.写入('上传成功')
            日志.记录(f'发送 200, 文件上传成功: {路径}')
        except Exception:
            import traceback
            错误信息 = traceback.format_exc()

            日志.错误(f'接收 {路径} 失败: {错误信息}')
            if os.path.exists(临时路径):
                os.remove(临时路径)

            操作器.发送响应(500)
            操作器.结束头()
            操作器.写入(f'文件上传失败: {错误信息}')
    else:
        操作器.发送响应(404)
        操作器.结束头()
        操作器.写入(页面_404.format(相对URL))
        日志.记录(f'由于路径 {相对URL} 不存在, 发送 404 错误响应')