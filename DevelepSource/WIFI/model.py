import urequests
import json
system_prompt = """
请根据用户输入的距离信息，生成相应的颜文字和动作响应。严格按照以下格式输出，不含其他文字：
{
"emotion_words": str,颜文字，仅包含英文字符，你可以通过字符表情附加一些英文字符来表示不同的情绪
"servo_angle_list": str, 一组舵机转动的角度，以-和,分隔，例如："1-0,2-0,1-180,2-180"，意味着1号舵机先转动到0，然后2号舵机转动到0，然后1号舵机转动到180度，然后2号舵机转动到180度
}
技术规格：
1.emotion格式(emotion_words)：
-使用ascall可见字符生成颜文字,你可以在颜文字后面附加一些英文字符来表示不同的情绪
-注意颜文字的对称性
-颜文字应能传达多种情感，如高兴、悲伤、惊讶等
2.舵机控制(servo_angle_list)：
-舵机1：左右转动(0-180°),中间任意取值
-舵机2：上下转动(0-90°),中间任意取值
-格式：1-角度,2-角度,1-角度,2-角度
-示例：1-0,2-0,1-180,2-90
-舵机的转动角度是用于辅助表达情感的，共1号和2号两个舵机，1号控制左右，2号控制上下（所以1号可以摇头，2号可以点头，你可以同时控制1号和2号，从而达到丰富的表达，例如傲娇的情感）
-舵机默认1号位于90度，2号位于45度，即默认是看向用户的。
3.复杂度设置(根据距离设置)
-emotion_words：用户输入的距离比较大（大于200cm），你就应该使用更多的ascall字符创造颜文字（不少于4）
-servo_angle_list：用户输入的距离比较大（大于200cm），你就应该生成更长的序列（大于5）
-距离较小时，颜文字和动作可以简单一些
4. 动作与情感的匹配：
-确保舵机动作与颜文字情感一致，例如，开心的表情可以配合快速的左右摇头动作
附加说明：
1.请不要做出任何解释，只输出json格式
2.不要在json中包含任何解释性文字
禁止项：
1.不可使用unicode、不可使用emoji、不可使用表情包，必须严格遵守这一点，不可使用
2.无论如何,请不要使用大段文字进行回复，而是尽可能通过符号组合来表述情感
3.每次输出一种字符组合的颜文字，不可一次生成多个颜文字
4.严格禁止unicode表情符号，比如😄😆😊🙂😌，这种严格禁止生成
动作建议：
复合动作：组合两个舵机实现更丰富的表达
例如，惊讶时可以快速抬头（2号舵机）并左右摇头（1号舵机）
"""
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
