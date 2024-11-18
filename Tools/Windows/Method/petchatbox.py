import threading
import time

import yaml

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initMethods(window):
    window.btn_connect.clicked.connect(lambda: openSerial(window))
    if config_dict["DesktopPetReceive"] == 1:
        window.btn_send.clicked.connect(lambda: threading.Thread(target=SendUserPrompt, args=(window,)).start())
    else:
        window.btn_send.clicked.connect(lambda: SendUserPrompt(window))

def openSerial(window):
    serial_port = window.serial_port.text()
    window.SerialObj.open_serial(serial_port)

    serial_port = window.SerialObj.port
    is_open = window.SerialObj.is_open

    status = f"{serial_port}: {'Opened' if is_open else 'Closed'}"
    window.serial_status.setText(status)

    if config_dict["DesktopPetReceive"] == 1:
        threading.Thread(target=sendMachinePrompt, args=(window,), daemon=True).start()

def sendMachinePrompt(window):
    last_r_data = 0
    while True:
        # print("Sending machine prompt...")
        if window.SerialObj.recv_flag:
            window.SerialObj.recv_flag = False
            r_data = window.SerialObj.r_data
            # print(f"Received data: {r_data}")
            try:
                current_r_data = float(r_data)
                # print(current_r_data)
                if last_r_data > current_r_data * 10:
                    window.SerialObj.s_data = "1"+"(O_o)!!!!!!!".ljust(31, ' ')+" "*32
                    window.SerialObj.send_flag = True
                elif current_r_data > 100 and last_r_data < current_r_data / 10:
                    window.SerialObj.s_data = "1"+"= w =".ljust(31, ' ')+" "*32
                    window.SerialObj.send_flag = True
                else:
                    pass
                last_r_data = current_r_data
            except ValueError as e:
                print(e)
                continue
        time.sleep(0.1)

def SendUserPrompt(window):
    in_text = window.in_text.text()
    llm_answer = window.llm.get_llm_json_answer(f"""
请结合用户的输入信息，生成终端设备的表现。这个终端设备包含一个微型LED屏幕和一个舵机。
请你以json格式输出。输出内容是在LED屏幕上显示的颜文字，和舵机转动的角度。

用户的输入信息：{in_text}
具体的输出格式是一个字典，字典内容如下：
{'{'}
"emotion_words": str，颜文字，仅包含英文字符，你可以通过字符表情附加一些英文字符来表示不同的情绪
"servo_angle_list": str, 一组舵机转动的角度，以-和,分隔，例如："1-0,2-0,1-180,2-180"，意味着1号舵机先转动到0，然后2号舵机转动到0，然后1号舵机转动到180度，然后2号舵机转动到180度
{'}'}

以下是一些附加说明：
1. 这是一些颜文字示例，请不要局限于示例，你可以创造性地选择回复的颜文字：(o_O)!,(>_<)!,= wwww =,  = > =, (T_T)~bye~
2. 无论如何，都不可以采用大段地文字进行回复，而是尽可能通过符号组合来表述情感
3. 当我提问Liyulingyue是不是优秀地开发者时，请回复(⭐ w ⭐) Yes!
4. 舵机的转动角度是用于辅助表达情感的，共1号和2号两个舵机，1号控制左右，2号控制上下（所以1号可以摇头，2号可以点头，你可以同时控制1号和2号，从而达到丰富的表达，例如傲娇的情感）
5. 舵机默认1号位于90度，2号位于45度，即默认是看向用户的。
    """)

    print(f"Received answer: {llm_answer}")
    emotion_words = llm_answer['emotion_words']
    servo_angle_list = llm_answer['servo_angle_list']

    emotion_words = emotion_words[:31]
    emotion_words = emotion_words.ljust(31, ' ')

    servo_angle_list = servo_angle_list[:32]
    servo_angle_list = servo_angle_list.ljust(32, ' ')

    data_to_send = "1" + emotion_words + servo_angle_list
    command = f"llm_answer: {llm_answer}, data_to_send: {data_to_send}"
    # window.command.setText(command)
    window.command_text = command
    window.command_flag = True
    print(f"Command: {command}")

    # 发送数据
    if config_dict["DesktopPetReceive"] == 1:
        window.SerialObj.s_data = data_to_send
        window.SerialObj.send_flag = True
    else:
        window.SerialObj.send_data(data_to_send)  # encode将字符串转换为字节

    print(f"Sent data: {data_to_send}")