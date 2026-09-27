from 自定义http服务器 import *
from 常量与配置 import *

登录_html_路径 = os.path.join(静态目录, '文件管理', '登录.html')

def 处理登录请求(
    相对URL: str,
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    print
    if 请求.类型 == 'GET':
        if 相对URL == '/login' or 相对URL == '/login/':
            with open(登录_html_路径, 'r', encoding=默认编码) as 文件:
                文本 = 文件.read()
            操作器.发送响应(200)
            操作器.发送头('Content-type', 'text/html')
            操作器.结束头()
            操作器.写入(文本.replace(':::名称:::', 名称))
            日志.记录(f'发送 登录.html')
            return
        else:
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(相对URL))
            日志.记录(f'由于路径 {相对URL} 不存在, 发送 404 错误响应')
            return
    elif 请求.类型 == 'POST':
        if 相对URL == '/login/verify_key':
                if 文件管理密码:
                    if 'key' in 请求.参数:
                        实际密码 = 请求.参数['key']
                        if 实际密码 == 文件管理密码:
                            操作器.发送JSON({'success': True, 'message': '密码正确'})
                        else:
                            操作器.发送响应(403)
                            操作器.结束头()
                            操作器.发送JSON({'success': False, 'message': '密码错误'})
                            日志.记录(f'由于密码错误, 发送 403 错误响应')
                            return
                    else:
                        操作器.发送JSON({'success': False, 'message': '请求参数中缺少 key 参数'})
                        return
                else:
                    操作器.发送JSON({'success': True, 'message': '服务器为设置密码, 默认成功'})