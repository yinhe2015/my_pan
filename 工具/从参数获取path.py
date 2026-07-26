from 自定义http服务器 import 自定义HTTP服务器, 页面_400
from 常量与配置 import *

def 从参数获取path(存储路径: str, 参数: dict, 操作器: 自定义HTTP服务器.操作, 相对路径: bool=False, 绝对路径: bool=True) -> str:
    if not 相对路径 and not 绝对路径:
        raise ValueError('相对路径和绝对路径至少要选择一个')
    日志.记录(f'从参数获取path, 参数 {参数}')

    if 'path' not in 参数:
        操作器.发送响应(400)
        操作器.结束头()
        操作器.写入(页面_400.format('GET 请求必须包含 ?path=路径'))
        日志.记录(f'由于请求必须包含 ?path=路径, 发送 400 错误响应')
        return ''
        
    路径 = 参数['path']
    if '..' in 路径:
        操作器.发送响应(400)
        操作器.结束头()
        操作器.写入(页面_400.format(f'{路径} (包含上级目录 ..)'))
        日志.记录(f'由于 {路径} (包含上级目录 ..), 发送 400 错误响应')
        return ''
    if 路径.startswith('/'):
        路径 = 路径[1:]

    路径 = 路径.replace('/', os.path.sep)
    日志.记录(f'相对路径 {路径}')
    
    输出 = []
    if 相对路径:
        输出.append(路径)
    if 绝对路径:
        输出.append(os.path.join(存储路径, 路径))
        日志.记录(f'绝对路径 {输出[-1]}')
        
    if len(输出) == 1:
        return 输出[0]
    else:
        return tuple(输出)
