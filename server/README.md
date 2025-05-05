# 作文识别服务

这是一个基于FastAPI的作文识别服务，可以上传作文图片并获取AI分析结果。

## 功能特点

- 支持上传作文图片
- 使用vivo AI API进行文字识别和分析
- 提供作文评价和改进建议
- 支持自定义提示词

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动
通过python -m http.server 3000 启动前端服务
启动服务后，可以访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
