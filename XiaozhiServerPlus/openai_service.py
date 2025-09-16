import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
from typing import Dict, Any

load_dotenv()

app = FastAPI()

# 创建OpenAI客户端用于转发
upstream_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_URL")
)

def log_request(body: Dict[str, Any]):
    """记录请求信息"""
    print("=" * 60)
    print("📨 收到OpenAI请求:")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    print(f"🔧 模型: {body.get('model', 'default')}")
    print(f"💬 消息数量: {len(body.get('messages', []))}")
    print(f"🌊 流式模式: {body.get('stream', False)}")
    print("=" * 60)

async def stream_generator(stream_response):
    """异步生成器处理流式响应"""
    try:
        for chunk in stream_response:
            chunk_data = chunk.model_dump()
            print(f"📡 流式数据块: {chunk_data}")
            yield f"data: {json.dumps(chunk_data)}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"❌ 流式处理错误: {str(e)}")
        error_chunk = {
            "error": {
                "message": f"Stream error: {str(e)}",
                "type": "stream_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"

@app.post("/v1/chat/completions")
async def openai_proxy(request: Request):
    try:
        # 获取请求体
        body = await request.json()
        log_request(body)
        
        # 提取所有可能的参数
        api_params = {
            "model": body.get("model", os.getenv("OPENAI_MODEL")),
            "messages": body.get("messages", []),
        }
        
        # 可选参数，只有在请求中存在时才添加
        optional_params = [
            "temperature", "max_tokens", "top_p", "frequency_penalty", 
            "presence_penalty", "stop", "n", "stream", "logit_bias",
            "user", "response_format", "seed", "tools", "tool_choice"
        ]
        
        for param in optional_params:
            if param in body:
                api_params[param] = body[param]
        
        print(f"🚀 转发参数: {list(api_params.keys())}")
        
        # 使用OpenAI客户端调用上游API
        chat_completion = upstream_client.chat.completions.create(**api_params)
        
        # 检查是否为流式响应
        if body.get("stream", False):
            print("🌊 开始流式响应")
            return StreamingResponse(
                stream_generator(chat_completion),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/plain; charset=utf-8"
                }
            )
        else:
            # 非流式响应
            result = chat_completion.model_dump()
            
            print("✅ API响应成功:")
            print(f"📝 内容预览: {result.get('choices', [{}])[0].get('message', {}).get('content', '')[:100]}...")
            print(f"📊 使用情况: {result.get('usage', {})}")
            
            return JSONResponse(content=result)
        
    except Exception as e:
        print(f"❌ 调用异常: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": f"Proxy error: {str(e)}",
                    "type": "proxy_error"
                }
            }
        )

# 添加其他OpenAI端点的转发支持
@app.get("/v1/models")
async def list_models():
    """转发模型列表请求"""
    try:
        print("📋 收到模型列表请求")
        models = upstream_client.models.list()
        result = models.model_dump()
        print(f"📋 返回 {len(result.get('data', []))} 个模型")
        return JSONResponse(content=result)
    except Exception as e:
        print(f"❌ 模型列表获取异常: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": f"Models list error: {str(e)}",
                    "type": "models_error"
                }
            }
        )

@app.post("/v1/embeddings")
async def embeddings_proxy(request: Request):
    """转发嵌入请求"""
    try:
        body = await request.json()
        print("🔤 收到嵌入请求:")
        print(json.dumps(body, indent=2, ensure_ascii=False))
        
        # 使用OpenAI客户端调用嵌入API
        embedding_response = upstream_client.embeddings.create(**body)
        result = embedding_response.model_dump()
        
        print(f"✅ 嵌入响应成功: {len(result.get('data', []))} 个向量")
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"❌ 嵌入请求异常: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": f"Embeddings error: {str(e)}",
                    "type": "embeddings_error"
                }
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
