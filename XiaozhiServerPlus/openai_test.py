
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
     api_key=os.getenv("OPENAI_API_KEY"),
     base_url="http://localhost:8000/v1",
)

chat_completion = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': '你是 AI Studio 实训AI开发平台的开发者助理，你精通开发相关的知识，负责给开发者提供搜索帮助建议。'},
        {'role': 'user', 'content': '你好，请介绍一下AI Studio'}
    ],
    model=os.getenv("OPENAI_MODEL"),
)

print(chat_completion.choices[0].message.content)