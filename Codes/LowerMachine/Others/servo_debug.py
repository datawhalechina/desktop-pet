# 舵机调试代码,复位之后调好舵机位置

from machine import Pin, PWM
import time

# 初始化舵机
servo1 = PWM(Pin(6))  # 左右舵机
servo1.freq(50)
servo2 = PWM(Pin(7))  # 上下舵机
servo2.freq(50)

def servo_move(servo, target_angle, speed=100):
    """
    控制舵机移动到目标角度
    :param servo: PWM对象
    :param target_angle: 目标角度(0-180)
    :param speed: 移动速度(1-100)
    """
    target_angle = max(0, min(180, target_angle))
    
    # 计算PWM占空比
    max_value = 2.5 / 20 * 65535
    min_value = 0.5 / 20 * 65535
    target = int(min_value + ((target_angle / 180) * (max_value - min_value)))
    
    servo.duty_u16(target)
    time.sleep(0.5)  # 等待舵机到达位置

def test_servo_position():
    """测试舵机位置"""
    while True:
        try:
            print("\n舵机调试菜单:")
            print("1. 设置舵机1角度 (左右)")
            print("2. 设置舵机2角度 (上下)")
            print("3. 复位到默认位置")
            print("4. 退出")
            
            choice = input("请选择操作 (1-4): ")
            
            if choice == '1':
                angle = int(input("请输入舵机1角度 (0-180): "))
                servo_move(servo1, angle)
                print(f"舵机1已移动到 {angle} 度")
                
            elif choice == '2':
                angle = int(input("请输入舵机2角度 (0-90): "))
                angle = min(180, angle)  # 限制舵机2最大角度为180
                servo_move(servo2, angle)
                print(f"舵机2已移动到 {angle} 度")
                
            elif choice == '3':
                print("复位到默认位置...")
                servo_move(servo1, 90)  # 舵机1默认90度
                servo_move(servo2, 45)  # 舵机2默认45度
                print("复位完成")
                
            elif choice == '4':
                print("退出程序")
                break
                
            else:
                print("无效选择，请重试")
                
        except ValueError:
            print("请输入有效的数字")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    print("开始舵机调试程序...")
    print("默认位置: 舵机1=90度, 舵机2=45度")
    
    # 先设置到默认位置
    servo_move(servo1, 90)
    servo_move(servo2, 45)
    
    test_servo_position()