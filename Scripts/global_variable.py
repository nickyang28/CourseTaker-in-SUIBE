from collections import namedtuple

USERNUMBER = ''
PASSWORD = ''
VERIFYCODE = ''

DRIVER = None
HEADERS = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'xk.suibe.edu.cn',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
COOKIES = {}
TUNNEL_F2D = []
TUNNEL_L2I = []
code_info = namedtuple('class_code_info', ['num', 'status'])
USERNAME = ''
IN_PSW = ''
SUCCESS = 0
TIMES = 0
