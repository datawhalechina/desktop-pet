import time

import serial
import threading

# only for Petchatbox
# 其中有一个循环收送的工具，这个工具只能用在petchatbox，其他地方不能用
class SerialClass(object):
    def __init__(self, receive_loop_thread=0):
        super(SerialClass, self).__init__()
        self.ser = None # 初始化串口对象
        self.is_open = False # 初始化串口是否打开的标志
        self.port = None # 初始化串口端口号
        self.receive_loop_thread = receive_loop_thread

        self.thread = None
        self.send_flag = False
        self.s_data = None
        self.recv_flag = False
        self.r_data = None

    def open_serial(self, serial_port, baud_rate=115200):
        self.port = serial_port

        if self.is_open:
            self.close_serial()
        try:
            self.ser = serial.Serial(serial_port, baud_rate, timeout=10)
            self.is_open = True
            if self.receive_loop_thread == 1:
                # 守护线程，会在主线程结束时自动关闭
                self.thread = threading.Thread(target=self.send_and_receive_thread, daemon=True)
                self.thread.start()
            print("Serial port successfully opened on port {}.".format(serial_port))
        except Exception as e:
            print("Error opening serial port:", e)
            self.is_open = False

    def send_and_receive_thread(self):
        print("send_and_receive_thread", end='\n')
        while True:
            # print("send_______________________________")
            if self.send_flag == True:
                s_data = self.s_data
                self.send_flag = False
                self.send_data(s_data)
            else:
                self.send_data("0"*64) # 发送空指令

            time.sleep(0.2)

            # print("receive_______________________________")
            self.r_data = self.receive_data()
            # print(self.r_data)
            self.recv_flag = True

            # print(self.r_data)

            time.sleep(0.2)

    def close_serial(self):
        if self.is_open:
            self.ser.close()
            self.is_open = False
            print("Serial port successfully closed.")
        else:
            print("Serial port is already closed.")

    def send_data(self, data):
        if self.is_open:
            try:
                print("send_data: ", data)
                self.ser.write(data.encode('utf-8'))  # encode将字符串转换为字节
            except (serial.SerialTimeoutException, serial.SerialException) as e:
                print("Error sending data:", e)
        else:
            print("Serial port is not opened.")

    def receive_data(self):
        if self.is_open:
            try:
                # print("receive_data")
                response = self.ser.readline().decode('utf-8').strip()
                print("receive_data: ", response)
                self.clean_receive_buffer() # 清空接收缓冲区，避免异常堆积
                return response
            except (serial.SerialTimeoutException, serial.SerialException) as e:
                print("Error receiving data:", e)
                return ""
        else:
            print("Serial port is not opened.")
            return ""

    def clean_receive_buffer(self):
        """
        清理接收缓冲区。
        描述:
            如果串口已打开，则清空接收缓冲区。
            如果串口未打开，则打印提示信息"Serial port is not opened."。
        """
        if self.is_open:
            self.ser.reset_input_buffer()
        else:
            print("Serial port is not opened.")

