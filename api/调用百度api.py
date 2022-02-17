# encoding:utf-8

import requests
import base64

'''
通用物体和场景识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
# 二进制方式打开图片文件
f = open('E:/Python项目/a试用/api/static/images/', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
access_token = '24.f67d9dfa558ec3f8d9e74ec032c1756d.2592000.1647412979.282335-25607057'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())
