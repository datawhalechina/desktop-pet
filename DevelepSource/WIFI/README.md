# WiFi智能交互系统

这是一个基于Raspberry Pi Pico W的智能交互系统，能够通过超声波传感器检测距离，并通过AI模型生成相应的表情和动作响应。

## 功能特点

- WiFi连接功能
- 超声波距离检测
- OLED显示屏输出
- 双舵机动作控制
- AI模型交互响应（使用免费的百度文心大模型ernie-speed型）

## 硬件要求

- Raspberry Pi Pico W
- HC-SR04超声波传感器
- SSD1306 OLED显示屏 (I2C接口)
- 2个舵机
- LED指示灯

## 引脚连接
按照`DevelepSource/DesktopPet项目连接即可

## 软件依赖

- MicroPython固件
- 百度文心大模型API

## 文件说明

- `wifi_main.py`: 主程序入口
- `wifi_utils.py`: WiFi连接和响应处理工具
- `model.py`: AI模型接口
- `ssd1306.py`: OLED显示驱动
- `hcsr04.py`: 超声波传感器驱动

## 配置说明

在`wifi_main.py`中配置以下参数：
WIFI_SSID = 'Your_SSID' # 你的WiFi名称
WIFI_PASSWORD = 'Your_Password' # 你的WiFi密码
API_KEY = "Your_API_Key" # 你的API_KEY
SECRET_KEY = "Your_Secret_Key" # 你的SECRET_KEY

API_KEY 和 SECRET_KEY 获取地址：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Dlkm79mnx
# 创建一个应用即可获取


## 使用说明

1. 将所有文件上传到Pico W
2. 确保正确配置WiFi和API密钥
3. 运行`wifi_main.py`
4. 系统将自动：
   - 连接WiFi
   - 初始化硬件
   - 进入交互循环
5.然后就可以脱离pc，连接任意电源即可（但要确保WiFi信号稳定）
## 交互逻辑

根据检测到的距离，系统会做出不同的响应：

这一部分可自行更改prompt，但是要保证返回的数据格式能被正确处理，提取emotion_words和servo_angle_list
（可以自行调教模型（> <））

