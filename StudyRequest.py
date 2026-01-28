from parsel import Selector

# 导入模块  requests会自动实现持久连接keep-alive
import requests
import json

# 东贝系统 特点 传统的strus1架构
login_url = 'http://10.0.93.106:8081/donper/loginAction.do'
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
body = {
        "username": "admin",
        "password": "666666"
        }
res = requests.post(login_url, headers=headers, data=body)

"""
# 方法一：
cookies = res.cookies
# 把返回的cookies转换成字典,以下两种方式均可
cookie = requests.utils.dict_from_cookiejar(cookies)
cookie = cookies.get_dict()
print(type(cookie), cookie)
# 使用cookies
res = requests.get(url=login_url, cookies=cookie)
print(res.status_code)

# 方法二：
cookies = res.cookies.items()
cookie = ''
for name, value in cookies:
    cookie += '{0}={1};'.format(name, value)
# 使用cookies
headers = {"cookie": cookie}
res = requests.get(url=login_url, headers=headers)
"""






"""
# 长城项目  特点：前后端分离
login_url = 'http://betasrm.greatwall.com.cn/login'
header = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "userinfo-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/78.0.3904.108 Safari/537.36"}
body = {
        "username": "admin",
        "password": "123456",
        }
r2 = requests.post(url=login_url, headers=header, data=json.dumps(body))
print(r2.status_code)
"""


"""
# 发送简洁的请求
url = "http://dict.baidu.com"
# 字典传递参数，如果值为None的键不会被添加到url中
r1 = requests.get(url, params={'wd': 'python', 'zhangsan': None})
r1.encoding = 'utf-8'

requests.get('https://github.com/timeline.json')                                # GET请求
requests.post('http://httpbin.org/post')                                        # POST请求
requests.put('http://httpbin.org/put')                                          # PUT请求
requests.delete('http://httpbin.org/delete')                                    # DELETE请求
requests.head('http://httpbin.org/get')                                         # HEAD请求
requests.options('http://httpbin.org/get')                                      # OPTIONS请求


# 响应的内容
print(r1.url)
print(r1.encoding)                  # 获取当前的编码
print(r1.text)                      # 以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
print(r1.content)                   # 以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。
print(r1.headers)                   # 以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
print(r1.status_code)               # 响应状态码
print(r1.raw)                       # 返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()
print(r1.ok)                        # 查看r.ok的布尔值便可以知道是否登陆成功
# *特殊方法* #
r1.json()                           # Requests中内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常
r1.raise_for_status()               # 失败请求(非200响应)抛出异常
"""
