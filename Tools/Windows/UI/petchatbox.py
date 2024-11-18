import yaml
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initUI(window):
    # 取消右上角退出按钮
    if hasattr(window, "sub_window_flag"):
        # ~QtCore.Qt.WindowCloseButtonHint 可以让右上角关闭功能无效
        window.setWindowFlags(window.windowFlags() | QtCore.Qt.SubWindow)

    window.setGeometry(300, 300, 280, 170)
    window.setWindowTitle("Pet Chat Box")

    window.command = QTextEdit()
    window.serial_port = QLineEdit() # serial port
    window.serial_status = QLabel("closed")
    window.in_text = QLineEdit()
    window.btn_connect = QPushButton("Connect")
    window.btn_send = QPushButton("Send")
    window.btn_exit = QPushButton("Exit")

    window.command.setReadOnly(True)
    window.serial_port.setPlaceholderText("请输入串口名称，如：COM3")
    window.in_text.setPlaceholderText("请输入要发送的指令，如：hi")
    window.btn_exit.clicked.connect(lambda : window.setVisible(False))

    vbox = QVBoxLayout()
    vbox.addWidget(QLabel("Command"))
    vbox.addWidget(window.command)

    hbox = QHBoxLayout()
    hbox.addWidget(QLabel("Serial Port"))
    hbox.addStretch(1) # stretch to fill the space
    hbox.addWidget(window.serial_status)
    vbox.addLayout(hbox)

    hbox = QHBoxLayout()
    hbox.addWidget(window.serial_port)
    hbox.addWidget(window.btn_connect)
    vbox.addLayout(hbox)

    vbox.addWidget(QLabel("Input"))
    hbox = QHBoxLayout()
    hbox.addWidget(window.in_text)
    hbox.addWidget(window.btn_send)
    vbox.addLayout(hbox)

    if hasattr(window, "sub_window_flag"):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(window.btn_exit)
        vbox.addLayout(hbox)

    window.setLayout(vbox)

    if hasattr(window, "sub_window_flag"):
        window.setVisible(False)
    else:
        window.show()
