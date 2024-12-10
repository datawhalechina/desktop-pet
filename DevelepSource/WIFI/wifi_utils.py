import network
import time
from machine import Pin

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

# 处理模型响应
def process_model_response(text, access_token):
    """处理模型响应数据"""
    from model import get_response
    
    try:
        response = get_response(text, access_token)
        print("原始响应:", response)
        
        if 'error_code' in response:
            print(f"API错误: {response.get('error_msg', '未知错误')}")
            return "error", []
        
        result_str = response.get('result', '')
        
        # 找到最后一个 { 和对应的 } 之间的内容
        json_start = result_str.rfind('{')
        if json_start >= 0:
            json_end = result_str.find('}', json_start) + 1
            if json_end > json_start:
                result_str = result_str[json_start:json_end]
                
                # 提取表情
                emotion_start = result_str.find('"emotion_words"') + 15
                emotion_start = result_str.find('"', emotion_start) + 1
                if emotion_start > 0:
                    emotion_end = result_str.find('"', emotion_start)
                    emotion_words = result_str[emotion_start:emotion_end]
                    # 只保留ASCII字符部分
                    ascii_emotion = ""
                    for char in emotion_words:
                        if ord(char) < 128:  # 只保留ASCII字符
                            ascii_emotion += char
                else:
                    emotion_words = ""
                    
                # 提取舵机序列
                servo_start = result_str.find('"servo_angle_list"') + 18
                servo_start = result_str.find('"', servo_start) + 1
                if servo_start > 0:
                    servo_end = result_str.find('"', servo_start)
                    servo_str = result_str[servo_start:servo_end]
                    
                    # 处理舵机角度列表
                    servo_angle_list = []
                    if servo_str:
                        pairs = [p.strip() for p in servo_str.split(',')]
                        for pair in pairs:
                            try:
                                if '-' in pair:
                                    servo, angle = pair.split('-')
                                    servo_num = int(servo)
                                    angle_num = int(angle)
                                    if 1 <= servo_num <= 2:
                                        servo_angle_list.append((servo_num, angle_num))
                            except:
                                continue
                else:
                    servo_angle_list = []
                
                print(f"解析结果:")
                print(f"Emotion Words: {emotion_words}")
                print(f"Servo Angle List: {servo_angle_list}")
                return emotion_words, servo_angle_list
        
        print("未找到有效的JSON数据")
        return "waiting", []
            
    except Exception as e:
        print(f"处理响应失败: {e}")
        return "error", []