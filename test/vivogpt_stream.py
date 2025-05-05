# encoding: utf-8
import uuid
import time
import requests
from auth_util import gen_sign_headers

# 请替换APP_ID、APP_KEY
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
URI = '/vivogpt/completions/stream'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'


def stream_vivogpt():
    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'prompt': '写一首春天的诗',
        'sessionId': str(uuid.uuid4()),
        'model': 'vivo-BlueLM-TB-Pro'
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=data, headers=headers, params=params, stream=True)

    if response.status_code == 200:
        first_line = True
        for line in response.iter_lines():
            if line:
                if first_line:
                    first_line = False
                    fl_time = time.time()
                    fl_timecost = fl_time - start_time
                    print("首字耗时: %.2f秒" % fl_timecost)
                print(line.decode('utf-8', errors='ignore'))
    else:
        print(response.status_code, response.text)
    end_time = time.time()
    timecost = end_time - start_time
    print("请求耗时: %.2f秒" % timecost)


if __name__ == "__main__":
    stream_vivogpt()