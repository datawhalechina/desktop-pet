from PyQt5.QtCore import QTimer

import yaml

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initTimer(window):
    # 画面切换
    window.timer = QTimer() # 定时器设置
    window.timer.timeout.connect(window.updateUI) # 绑定结束时动作
    window.timer.start(1000) # 动作时间切换设置, 1000ms = 1s