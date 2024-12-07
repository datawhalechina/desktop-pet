import network
import time

# 设置 Wi-Fi SSID 和密码
SSID = 'ziroom603'
PASSWORD = '4001001111'
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    max_wait = 15  # 最长等待时间为15秒
    while max_wait > 0:
        if wlan.isconnected():
            break
        print('等待连接...')
        time.sleep(1)
        max_wait -= 1
    if wlan.isconnected():
        print('已连接到 Wi-Fi')
        print('网络配置：', wlan.ifconfig())
        return wlan.ifconfig()[0]  # 返回分配的 IP 地址
    else:
        print('无法连接到 Wi-Fi')
        return None
