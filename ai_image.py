#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
import time
from auth_util import gen_sign_headers

# 请替换为你的 APP_ID 和 APP_KEY
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
DOMAIN = 'api-ai.vivo.com.cn'

def submit_task():
    uri = '/api/v1/task_submit'
    method = 'POST'
    params = {}

    data = {
        'height': 1024,
        'width': 768,
        'prompt': '一只梵高画的猫',
        'styleConfig': '7a0079b5571d5087825e52e26fc3518b',
        'userAccount': 'thisistestuseraccount'
    }

    headers = gen_sign_headers(APP_ID, APP_KEY, method, uri, params)
    headers['Content-Type'] = 'application/json'

    url = f'http://{DOMAIN}{uri}'
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        result = response.json()
        print('提交成功:', result)
        task_id = result.get('data', {}).get('taskId')
        return task_id
    else:
        print('提交失败:', response.status_code, response.text)
        return None

def check_progress(task_id):
    uri = '/api/v1/task_progress'
    method = 'GET'
    params = {'task_id': task_id}

    headers = gen_sign_headers(APP_ID, APP_KEY, method, uri, params)

    uri_params = '&'.join([f'{k}={v}' for k, v in params.items()])
    url = f'http://{DOMAIN}{uri}?{uri_params}'

    print('进度查询URL:', url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print('查询结果:', result)
        return result
    else:
        print('查询失败:', response.status_code, response.text)
        return None

def main():
    task_id = submit_task()
    if not task_id:
        return

    print(f'任务已提交，task_id: {task_id}，正在查询进度...')
    for _ in range(10):  # 最多轮询10次
        result = check_progress(task_id)
        if not result:
            break

        status = result.get('data', {}).get('status')
        if status == 'FINISHED':
            print('绘画完成！结果:', result.get('data'))
            break
        elif status == 'FAILED':
            print('绘画失败。')
            break
        else:
            print('任务未完成，等待5秒后重试...')
            time.sleep(5)

if __name__ == '__main__':
    main()
