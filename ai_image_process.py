#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
from auth_util import gen_sign_headers

# 请注意替换APP_ID、APP_KEY
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
URI = '/api/v1/task_progress'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'GET'
	
def progress():
   params = {
       # 注意替换为提交作画任务时返回的task_id
       'task_id': '955804c6341a57d1b6ca2142fa394b1a'
   }
   headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)

   uri_params = ''
   for key, value in params.items():
       uri_params = uri_params + key + '=' + value + '&'
   uri_params = uri_params[:-1]

   url = 'http://{}{}?{}'.format(DOMAIN, URI, uri_params)
   print('url:', url)
   response = requests.get(url, headers=headers)
   if response.status_code == 200:
       # print(response.json())
       print(json.dumps(response.json(), indent=4))
   else:
       print(response.status_code, response.text)

if __name__ == '__main__':
   progress()