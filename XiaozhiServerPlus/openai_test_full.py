import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 测试非流式调用
def test_normal_call():
    print("测试非流式调用...")
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {'role': 'user', 'content': '请简单介绍一下Python'}
        ],
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.7,
        max_tokens=100
    )

    print("非流式响应:")
    print(chat_completion.choices[0].message.content)
    print("-" * 50)

# 测试流式调用
def test_stream_call():
    print("测试流式调用...")
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1",
    )

    stream = client.chat.completions.create(
        messages=[
            {'role': 'user', 'content': '请告诉我一个有趣的故事'}
        ],
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.8,
        max_tokens=200,
        stream=True
    )

    print("流式响应:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n" + "-" * 50)

if __name__ == "__main__":
    test_normal_call()
    test_stream_call()