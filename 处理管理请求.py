from 自定义http服务器 import *
from 常量与配置 import *

管理_html_路径 = os.path.join(静态目录, '管理.html')
管理登录_html_路径 = os.path.join(静态目录, '管理登录.html')

def 处理管理请求(
    请求: 自定义HTTP服务器.请求,
    操作器: 自定义HTTP服务器.操作,
):
    相对URL = 请求.相对URL[7:]
    if not 相对URL.startswith('/'):
        相对URL = '/' + 相对URL

    if 相对URL in {'/login', '/login/', '/login/verify_key'}:
        if 相对URL == '/login/verify_key':
            if 管理密码:
                if 'key' in 请求.参数:
                    实际密码 = 请求.参数['key']
                    if 实际密码 == 管理密码:
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
                操作器.发送JSON({'success': True, 'message': '服务器未设置密码, 默认成功'})
        else:
            操作器.发送文件(管理登录_html_路径, MIME类型=MIME类型映射['html'], 显示进度条=显示进度条)
        return

    if 管理密码:
        if 'key' in 请求.参数:
            实际密码 = 请求.参数['key']
            if 实际密码 != 管理密码:
                操作器.发送响应(403)
                操作器.结束头()
                操作器.写入(页面_403.format('密码错误'))
                日志.记录(f'由于密码错误, 发送 403 错误响应')
                return
        else:
            操作器.发送重定向('/manage/login')
            return

    match 请求.类型:
        case 'GET':
            match 相对URL:
                case '/':
                    操作器.发送文件(管理_html_路径, MIME类型=MIME类型映射['html'], 显示进度条=显示进度条)
                case _:
                    操作器.发送响应(404)
                    操作器.结束头()
                    操作器.写入(页面_404.format(相对URL))
                    日志.记录(f'功能 {相对URL} 不存在, 发送 404 错误响应')
            return
        case 'POST':
            match 相对URL:
                case '/stop':
                    日志.记录('停止服务器')
                    操作器.发送JSON({'success': True, 'message': '服务器正在停止'})
                    exit(0)
                case '/restart':
                    操作器.发送JSON({'success': False, 'message': '重启服务器未实现'})
                    日志.记录('重启服务器未实现')
                case _:
                    操作器.发送响应(404)
                    操作器.结束头()
                    操作器.发送JSON({'success': False, 'message': f'功能 {相对URL} 不存在'})
                    日志.记录(f'功能 {相对URL} 不存在, 发送 404 错误响应')
            return
        case _:
            操作器.发送响应(404)
            操作器.结束头()
            操作器.写入(页面_404.format(相对URL))
            日志.记录(f'功能 {相对URL} 不存在, 发送 404 错误响应')