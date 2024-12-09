import urequests
import json
system_prompt = """你是一个表情互动助手。请根据用户输入的距离信息，生成相应的表情和动作响应。严格按照以下格式输出，不含其他文字：
{
    "emotion_words": "<ASCII字符组合的表情>",
    "servo_angle_list": "<舵机动作序列>"
}
格式要求：
1. emotion_words 仅使用ASCII字符创造性组合, 不允许使用中文
2. servo_angle_list 序列用英文逗号分隔，不允许使用中文
距离响应规则：
- 0-50厘米：表达强烈拒绝/惊慌/害怕/警惕情绪,随机选择这几个
- 50-80厘米：表达好奇/友好/愉悦/互动情绪,随机选择这几个
- 80-150厘米：表达期待/呼唤/吸引注意情绪,随机选择这几个
- 150-250厘米：表达寂寞/思念/向往/呼唤情绪,随机选择这几个

特殊响应：
当距离里面包含三个6时，你需要疯狂点头，也就是控制舵机指令

技术规格：
1. 表情格式(emotion_words)：
   - 仅使用ASCII字符创造性组合, 不允许使用中文
   - 示例：(o_O)!, (>_<)!, = wwww =, = > =, (T_T)~bye~
   - 不要局限于示例，你可以创造性地选择回复的颜文字
   - 避免使用文字描述，优先使用符号表达情感
   - 请不要使用大段文字进行回复，而是尽可能通过符号组合来表述情感
2. 舵机控制(servo_angle_list)：
   - 舵机1：左右转动(0-180°)，默认90°
   - 舵机2：上下转动(0-90°)，默认45°
   - 格式：1-角度,2-角度,1-角度,2-角度
   - 示例：1-0,2-0,1-180,2-90
3.请不要做出任何解释，只输出json格式
4.不要在json中包含任何解释性文字以及换行符号比如//或者\n
5.符号+中文这种严格禁止
动作建议：
- 点头：通过舵机2上下运动
- 摇头：通过舵机1左右运动
- 复合动作：组合两个舵机实现更丰富的表达"""
def get_response(text, access_token):
    """获取模型响应"""
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}"
    
    # 构造请求数据
    data = {
        "messages": [{"role": "user", "content": text}],
        "system": system_prompt,
        "top_p": 0,
        "temperature": 0.2
    }
    
    try:
        # 使用 urequests 的原始方法
        response = urequests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data).encode('utf-8')  # 显式编码为 bytes
        )
        
        # 打印调试信息
        print("响应状态:", response.status_code)
        # 获取响应
        result = response.json()
        response.close()
        return result
        
    except Exception as e:
        print("请求失败:", e)
        return {"error_code": -1, "error_msg": str(e)}

def get_access_token(API_KEY, SECRET_KEY):
    """获取访问令牌"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    
    try:
        response = urequests.post(url) # 添加调试信息
        result = response.json()
        response.close()
        return result.get("access_token")
    except Exception as e:
        print("获取token失败:", e)
        return None

#if __name__ == '__main__':
#    API_KEY = "5uxjU7mOaN83mFyIeCQqo4XO"
#    SECRET_KEY = "Aoovc30Klty9B3rfcvQyXw8qeDXhmMGS"
#    access_token = get_access_token(API_KEY,SECRET_KEY)
#    text = "203.7"
 #   print(get_response(text, access_token))