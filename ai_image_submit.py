#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
from auth_util import gen_sign_headers

# 请注意替换APP_ID、APP_KEY
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
URI = '/api/v1/task_submit'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'

def submit():
   params = {}
   data = {
    'height': 1024,
    'width': 768,
    'prompt': '千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。',
    'styleConfig': '7a0079b5571d5087825e52e26fc3518b',
    'userAccount': 'thisistestuseraccount'
   }

   headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
   headers['Content-Type'] = 'application/json'

   url = 'http://{}{}'.format(DOMAIN, URI)
   response = requests.post(url, data=json.dumps(data), headers=headers)
   if response.status_code == 200:
       # print(response.json())
       print(json.dumps(response.json(), indent=4))
   else:
       print(response.status_code, response.text)

if __name__ == '__main__':
   submit()