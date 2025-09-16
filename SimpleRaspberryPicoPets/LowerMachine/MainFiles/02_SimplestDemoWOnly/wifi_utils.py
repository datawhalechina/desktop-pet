import network
import time
from machine import Pin
import json
import urequests

# 配置板载LED用于状态显示
led = Pin("LED", Pin.OUT)

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
-emotion_words：用户输入的距离比较大（大于200cm），你就应该使用更多的ascall字符创造颜文字（不少于4）,但是颜文字与英文总和长度不能超过12
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

def get_access_token(API_KEY, SECRET_KEY):
    """获取访问令牌"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"

    try:
        response = urequests.post(url)  # 添加调试信息
        result = response.json()
        response.close()
        return result.get("access_token")
    except Exception as e:
        print("获取token失败:", e)
        return None  # 多轮对话


def get_response(text, history, access_token):
    """获取多轮对话的模型响应也适用于单轮对话"""
    # 你可以通过更改这里url去切换百度的api模型，其他api还未了解
    # 但是更改模型之后，模型对这个系统设定（system_prompt）回复可能与现在模型有区别，你需要去修改clean_json_response函数去清理返回数据得到json字符串，可能也需要改system_prompt
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}"

    # Update the prompt with the conversation history
    messages = history.copy()
    messages.append({"role": "user", "content": text})
    print(messages)
    # Construct request data
    data = {
        "messages": messages,
        "top_p": 0.9,
        "temperature": 0.7,
        "system": system_prompt,
    }
    try:
        # Properly encode the data
        json_data = json.dumps(data)

        # Send the request with minimal arguments
        response = urequests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json_data.encode('utf-8')
        )

        print("Request payload:", json_data)  # Debug the actual sent data

        # 可以将json结果转化为字典
        # 但是result是markdown格式，需要解析
        result = response.json()
        response.close()

        return result

    except Exception as e:
        print("请求失败:", e)
        return {"error_code": -1, "error_msg": str(e)}


def clean_json_response(result_str):
    """
    清理模型返回的JSON响应
    Args:
        result_str: 原始响应字符串
    Returns:
        cleaned_str: 清理后的JSON字符串
    """
    # 1. 查找JSON部分（在```json和```之间的内容）
    start_index = result_str.find('```json\n')
    end_index = result_str.find('\n```', start_index)
    if start_index != -1 and end_index != -1:
        result_str = result_str[start_index + 7:end_index]

    # 2. 移除JSON中的注释
    result_lines = result_str.split('\n')
    cleaned_lines = []
    for line in result_lines:
        comment_index = line.find('//')
        if comment_index != -1:
            line = line[:comment_index]
        cleaned_lines.append(line.strip())
    result_str = '\n'.join(cleaned_lines)

    # 3. 提取大括号内的内容
    start_index = result_str.find('{')
    end_index = result_str.rfind('}') + 1
    if start_index != -1 and end_index != -1:
        result_str = result_str[start_index:end_index]

    return result_str

# 连接WiFi
def connect_wifi(ssid, password):
    """连接到指定的WiFi网络"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # 如果已经连接，则返回
    if wlan.isconnected():
        return True
    
    # 开始连接WiFi
    print('正在连接WiFi...')
    wlan.connect(ssid, password)
    
    # 等待连接或失败
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('等待连接...')
        time.sleep(1)
    
    # 处理连接结果
    if wlan.status() != 3:
        led.off()
        print('WiFi连接失败')
        return False
    else:
        led.on()
        print('连接成功')
        status = wlan.ifconfig()
        print('IP地址:', status[0])
        return True 

def process_model_response(text, access_token, history, MULTI_TALK=False):
    """处理模型响应数据"""
    try:
        response = get_response(text, history, access_token)
        print("原始响应:", response)
        
        if 'error_code' in response:
            print(f"API错误: {response.get('error_msg', '未知错误')}")
            return "error", []
        
        # 提取并清理 JSON 响应
        result_str = response.get('result', '')
        result_str = clean_json_response(result_str)
        print("清理后的JSON:", result_str)
        
        # 解析 JSON 字符串
        result_dict = json.loads(result_str)
        
        # 提取情感词和舵机角度列表
        emotion_words = result_dict.get("emotion_words", "")
        servo_angle_list_str = result_dict.get("servo_angle_list", "")
        
        # 增加历史
        if MULTI_TALK:
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": result_str})
        
        # 处理舵机角度列表
        servo_angle_list = []
        if servo_angle_list_str:
            pairs = [p.strip() for p in servo_angle_list_str.split(',')]
            for pair in pairs:
                try:
                    if '-' in pair:
                        servo, angle = pair.split('-')
                        servo_num = int(servo)
                        angle_num = int(angle)
                        if 1 <= servo_num <= 2:
                            servo_angle_list.append((servo_num, angle_num))
                except ValueError:
                    continue
        
        print(f"解析结果:")
        print(f"Emotion Words: {emotion_words}")
        print(f"Servo Angle List: {servo_angle_list}")
        return emotion_words, servo_angle_list
        
    except Exception as e:
        print(f"处理响应失败: {e}")
        return "error", []

