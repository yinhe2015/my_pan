from 日志 import 控制台日志
import os

文件管理密码 = None
管理密码 = '123456'

调试模式 = True
日志 = 控制台日志(
    记录调试=调试模式,
    记录记录=调试模式,
    记录信息=调试模式,
    记录成功=调试模式,
    记录警告=True,
    记录错误=True,
    记录异常=True,
    记录其他=True,
)

基础目录 = os.path.dirname(os.path.abspath(__file__))
os.chdir(基础目录)

静态目录 = os.path.join(基础目录, '静态')
os.makedirs(静态目录, exist_ok=True)

块大小 = 1024 * 1024
显示进度条 = False

favicon_ico路径 = os.path.join(静态目录, 'favicon.ico')
if os.path.exists(favicon_ico路径):
    with open(favicon_ico路径, 'rb') as 文件:
        favicon_ico = 文件.read()
else:
    日志.警告('未找到 favicon.ico 文件')
    favicon_ico = None
