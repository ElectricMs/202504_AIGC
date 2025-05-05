from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import base64
import uuid
import time
import requests
from auth_util import gen_sign_headers
import os
from typing import Optional
from pydantic import BaseModel
import json
import asyncio

app = FastAPI(title="作文识别服务")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置信息
APP_ID = '2025128664'
APP_KEY = 'nhNvMbxSvnZpsLVl'
URI = '/vivogpt/completions/stream'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'

class ChatRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

async def stream_generator(response):
    """生成流式响应"""
    try:
        first_line = True
        start_time = time.time()
        
        for line in response.iter_lines():
            if line:
                try:
                    # 解码并处理每一行响应
                    decoded_line = line.decode('utf-8', errors='ignore')
                    
                    if first_line:
                        first_line = False
                        fl_time = time.time()
                        fl_timecost = fl_time - start_time
                        yield f"data: {{\"first_token_time\": {fl_timecost}}}\n\n"
                    
                    # 返回原始响应数据
                    yield f"data: {decoded_line}\n\n"
                except Exception as e:
                    print(f"处理流式响应时出错: {str(e)}")
                    continue
    except Exception as e:
        print(f"流式生成器错误: {str(e)}")
        yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    与AI进行文本对话，支持流式输出
    
    Args:
        request: 包含prompt、temperature和stream的请求体
    """
    try:
        # 生成请求参数
        params = {
            'requestId': str(uuid.uuid4())
        }
        
        # 构建请求数据
        data = {
            'prompt': request.prompt,
            'model': 'vivo-BlueLM-TB-Pro',
            'sessionId': str(uuid.uuid4())
        }
        
        # 生成请求头
        headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
        headers['Content-Type'] = 'application/json'
        
        # 发送请求
        start_time = time.time()
        url = f'http://{DOMAIN}{URI}'
        
        if request.stream:
            # 流式输出
            response = requests.post(url, json=data, headers=headers, params=params, stream=True)
            
            if response.status_code == 200:
                return StreamingResponse(
                    stream_generator(response),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                    }
                )
            else:
                return {
                    "status": "error",
                    "message": f"API请求失败: {response.status_code}",
                    "details": response.text
                }
        else:
            # 普通输出
            response = requests.post(url, json=data, headers=headers, params=params)
            
            if response.status_code == 200:
                result = response.json()
                end_time = time.time()
                timecost = end_time - start_time
                
                if result['code'] == 0 and result.get('data'):
                    return {
                        "status": "success",
                        "data": result['data']['content'],
                        "time_cost": f"{timecost:.2f}秒"
                    }
                else:
                    return {
                        "status": "error",
                        "message": result.get('msg', '未知错误'),
                        "code": result.get('code', -1)
                    }
            else:
                return {
                    "status": "error",
                    "message": f"API请求失败: {response.status_code}",
                    "details": response.text
                }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"处理请求时发生错误: {str(e)}"
        }

@app.post("/analyze_essay")
async def analyze_essay(file: UploadFile = File(...), prompt: Optional[str] = None):
    """
    分析作文图片并返回AI评价
    
    Args:
        file: 上传的作文图片文件
        prompt: 可选的提示词，默认为分析作文内容
    """
    try:
        # 读取上传的文件
        contents = await file.read()
        image = base64.b64encode(contents).decode('utf-8')
        
        # 生成请求参数
        params = {
            'requestId': str(uuid.uuid4())
        }
        
        # 构建请求数据
        data = {
            'prompt': prompt or '识别作文内容',
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
                    "content": "请识别图片中的文字内容",
                    "contentType": "text"
                }
            ],
        }
        
        # 生成请求头
        headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
        headers['Content-Type'] = 'application/json'
        
        # 发送请求
        start_time = time.time()
        url = f'http://{DOMAIN}{URI}'
        response = requests.post(url, json=data, headers=headers, params=params)
        
        # 处理响应
        if response.status_code == 200:
            result = response.json()
            end_time = time.time()
            timecost = end_time - start_time
            
            return {
                "status": "success",
                "data": result,
                "time_cost": f"{timecost:.2f}秒"
            }
        else:
            return {
                "status": "error",
                "message": f"API请求失败: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"处理请求时发生错误: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 