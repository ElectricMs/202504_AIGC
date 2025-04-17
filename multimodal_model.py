# encoding: utf-8
import base64
import uuid
import time
import requests
from auth_util import gen_sign_headers

# 请替换APP_ID、APP_KEY
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
URI = '/vivogpt/completions'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'
PIC_FILE = './test2.jpg'


def stream_vivogpt():
    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])
    picture = PIC_FILE
    with open(picture, "rb") as f:
        b_image = f.read()
    image = base64.b64encode(b_image).decode('utf-8')
    data = {
        'prompt': '你好',
        'sessionId': str(uuid.uuid4()),
        'requestId': params['requestId'],
        'model': 'vivo-BlueLM-V-2.0',
        "messages": [
            {
                "role": "user",
                "content": "data:image/JPEG;base64," + image,
                "contentType": "image"
            },
            {
                "role": "user",
                "content": "我将给你一张作文图片，请告诉我图片中的文字内容，并从高考语文的角度评价一下这段文字，给出一些改进意见",
                "contentType": "text"
            }
        ],
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.text)
    end_time = time.time()
    timecost = end_time - start_time
    print("请求耗时: %.2f秒" % timecost)


if __name__ == "__main__":
    stream_vivogpt()