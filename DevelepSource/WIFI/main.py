from machine import Pin, PWM, I2C
import time
from wifi_utils import connect_wifi, process_model_response
from ssd1306 import SSD1306_I2C
from model import get_response, get_access_token
import gc
# 配置参数
WIFI_SSID = 'TP-LINK_817'
WIFI_PASSWORD = '123456789'
API_KEY = "5uxjU7mOaN83mFyIeCQqo4XO"
SECRET_KEY = "Aoovc30Klty9B3rfcvQyXw8qeDXhmMGS"

#是否启用多轮对话
MULTI_TALK = False

# 硬件初始化
ENABLE_SEND = True
if ENABLE_SEND:
    from hcsr04 import HCSR04
    ultrasonic = HCSR04(trigger_pin=3, echo_pin=2, echo_timeout_us=1000000)

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)

servo1 = PWM(Pin(6))
servo1.freq(50)
servo2 = PWM(Pin(7))
servo2.freq(50)

def servo_move(servo, target_angle, speed=100):
    """
    控制舵机移动到目标角度，可控制速度
    """
    current_duty = servo.duty_u16()
    max_value = 2.5 / 20 * 65535
    min_value = 0.5 / 20 * 65535
    current_angle = int((current_duty - min_value) * 180 / (max_value - min_value))
    
    target_angle = max(0, min(180, target_angle))
    step = 1 if speed >= 50 else 0.5
    delay = (100 - speed) / 1000
    
    while abs(current_angle - target_angle) > step:
        if current_angle < target_angle:
            current_angle += step
        else:
            current_angle -= step
            
        max_value = 2.5 / 20 * 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        min_value = 0.5 / 20 * 65535
        target = int(min_value + ((current_angle / 180) * (max_value - min_value)))
        servo.duty_u16(target)
        time.sleep(delay)

def handle_response(text, access_token, oled, servo1, servo2,history=[]):
    """处理响应数据"""
    try:
        # 获取模型响应并处理
        emotion_words, servo_angle_list = process_model_response(text, access_token,history,MULTI_TALK)
        #如果是多轮对话，则更新历史
        if MULTI_TALK:
            #如果历史长度超过10，则删除前8条
            if len(history) > 10:
                history = history[-2:]
         # 去除可能存在的引号，并清理字符串
       # emotion_words = emotion_words.strip('"').strip()
        # 显示表情
        oled.fill(0)
        oled.text(emotion_words, 0, 12)
        oled.show()
        
        # 执行舵机动作序列
        for servo_id, angle in servo_angle_list:
            try:
                if servo_id == 1:
                    servo_move(servo1, angle)
                elif servo_id == 2:
                    servo_move(servo2, angle)
                time.sleep(0.1)  # 动作间延时
            except Exception as e:
                print(f"舵机控制失败: {e}")
        
        # 恢复默认位置
        time.sleep(1)
        servo_move(servo1, 90)
        servo_move(servo2, 30)
        
    except Exception as e:
        print(f"处理响应失败: {e}")
def show():
    """显示内存使用情况"""
    gc.collect()  # 执行垃圾回收
    free_mem = gc.mem_free()  # 空闲内存
    alloc_mem = gc.mem_alloc()  # 已分配内存
    total_mem = free_mem + alloc_mem  # 总内存
    
    print(f"内存使用情况:")
    print(f"总内存: {total_mem/1024:.2f}KB")
    print(f"已用: {alloc_mem/1024:.2f}KB")
    print(f"空闲: {free_mem/1024:.2f}KB")
    print(f"使用率: {(alloc_mem/total_mem)*100:.1f}%")
def main():
    # 连接WiFi
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("WiFi连接失败")
        return
    
    # 获取访问令牌
    print("获取访问令牌...")
    access_token = get_access_token(API_KEY, SECRET_KEY)
    if not access_token:
        print("获取访问令牌失败")
        return
    
    # 初始化显示
    oled.fill(0)
    oled.text("Ready!", 0, 12)
    oled.show()
    
    # 初始化舵机位置
    servo_move(servo1, 90)
    servo_move(servo2, 30)
    
    last_distance = 0
    last_request_time = 0
    #多轮历史
    history=[]
    print("开始主循环...")
    while True:
        try:
            current_time = time.time()
            if ENABLE_SEND:
                distance = ultrasonic.distance_cm()  # 在同一行更新
                # 当距离变化超过阈值且距离上次请求超过10秒时发送请求
                if (abs(distance - last_distance) > 200 and 
                    current_time - last_request_time > 7):
                    oled.fill(0)
                    oled.text("Thinking...", 0, 12)
                    oled.show()
                    print(f"检测到距离变化: {distance}cm")
                    handle_response(str(distance), access_token, oled, servo1, servo2,history)
                    last_distance = distance
                    last_request_time = current_time
                    #延时1.5s
                    time.sleep(1.5)
                elif(abs(distance - last_distance) > 300 and 
                    current_time - last_request_time < 7):
                    oled.fill(0)
                    oled.text("take it easy @_@", 0, 12)
                    oled.show()
                    #延时1.5s
                    time.sleep(1.5)
                else:
                    oled.fill(0)
                    oled.text("(^O^) Ready", 0, 12)
                    oled.show()
            time.sleep(0.1)
            
        except Exception as e:
            print(f"错误: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()





