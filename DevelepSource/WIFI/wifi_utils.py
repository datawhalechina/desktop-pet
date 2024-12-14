import network
import time
from machine import Pin
import json

# 配置板载LED用于状态显示
led = Pin("LED", Pin.OUT)
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
    from model import get_response,clean_json_response
    
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

