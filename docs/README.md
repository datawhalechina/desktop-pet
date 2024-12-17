# 基于树莓派Pico的桌面宠物

本界面介绍了如何通过最低50元人民币左右的金额（只是估算，可能需要更多），购买一整套组件，自己搭建一个如下图所示的硬件结构，通过UWB口连接电脑，当你输入信息的时候，屏幕上会显示颜文字，并配合一些动作。

![DesktopPet_demo.png](Images/DesktopPet_demo.jpg)

除此之外，你也可以再外接一个感知设备，如下图所示，增加了一个雷达测距工具（硬件成本仅增加了3块多），从而你可以通过硬件传感器感知周围的状态，并反馈给电脑。但这会导致代码逻辑非常复杂，所以本文会同时介绍如何无雷达和有雷达的两种情况。如果你对这一切都不熟悉，可以仅关注不包含雷达的版本，作为你的新手入门。

![DesktopPet_demo2.png](Images/DesktopPet_demo2.jpg)

不加载雷达时，仅能通过电脑端交互，加载雷达后，可以基于你的手指动作进行交互~示例如下：

![DesktopPet_demo.gif](Images/DesktopPet_demo.gif)
![DesktopPet_demo.gif2](Images/DesktopPet_demo2.gif)

## 快速开始

本项目没办法非常好的快速开始，因为你必须有一套能够配合的硬件，本章节会描述整个流程中最基本的部分。 但请不要担心，搭建桌面宠物并跑起来的过程，就像是搭积木一样，不需要你有什么经验。（如果你希望后续改造和扩展这个桌宠，我们在其他章节提供了简单的代码说明）

<span style="color: red;">本文档并不会详细对树莓派如何入门进行介绍，本仓库只会对必要的运行内容进行说明。如果你需要更深入了解，请参考官方文档。</span>

### 硬件资源

本项目所需的硬件资源如下：

- 树莓派Pico(焊好排针) 1个
- 两自由度舵机云台 1个
- 180°舵机 2个
- USB数据线 1个
- 0.91寸4管角oled显示屏ssd1306(焊好排针) 1个
- HC-SR04超声波测距模块 1个
- 2排×5P杜邦线排针板
- 母对母杜邦线 10根
- 公对母杜邦线 2根
- 剪刀、胶带等

<span style="color: red;">上述资源并非不可替代，建议新手跟着介绍走。你可以不加入超声波测距模块。</span>

#### 树莓派Pico与数据线

树莓派Pico是一个超级小的，仅仅比U盘大一圈的微型控制器，当前有很多型号可供选择，你可以购买任意型号的树莓派Pico用于本项目，建议选购【焊好引脚】的板子。价格在20~30元左右。

连接树莓派Pico和电脑需要一根数据线，如果你缺少数据线可以和树莓Pico一起购买。

![树莓派示意图](Images/pico-1s.png)

#### 云台与舵机

直接搜索 两轴云台 或 二自由度舵机云台 即可，有打包云台和舵机一起卖的情况。价格在10~20元左右。（特别提醒：有的商家卖的散件和图示有一定出入，拼接起来不是很顺畅，但基本可以自行通过剪刀啥的修整一下）

#### oled显示屏

价格10块钱左右，请务必选择焊好引脚的款式。

#### HC-SR04超声波测距模块

价格3元多一点。

#### 2排×5P杜邦线排针板

一块钱多一个。

#### 杜邦线

通常是一把起售（大约十多块钱买一把即可），平均下来0.1元一根。

### 接线

当我们集齐所有硬件后，先进行接线。（因为接线后可以运行一下程序，看一下硬件是否损坏），具体接线如下：

| 连接的引脚1       | 连接的引脚2       | 备注  |
| ------------ | ------------ | --- |
| 树莓派Pico引脚2   | 超声波测距模块 Echo |     |
| 树莓派Pico引脚3   | 超声波测距模块 Trig |     |
| 树莓派Pico引脚4   | oled SDA     |     |
| 树莓派Pico引脚5   | oled SCL     |     |
| 树莓派Pico引脚6   | 舵机1信号线       |     |
| 树莓派Pico引脚7   | 舵机2信号线       |     |
| 树莓派Pico 5v输出 | 排针版 +        |     |
| 树莓派Pico GND  | 排针版 -        |     |
| 排针版 +        | oled VCC     |     |
| 排针版 -        | oled GND     |     |
| 排针版 +        | 舵机1 VCC      |     |
| 排针版 -        | 舵机1 GND      |     |
| 排针版 +        | 舵机2 VCC      |     |
| 排针版 -        | 舵机2 GND      |     |
| 排针板 +        | 超声波模块 VCC    |     |
| 排针版 -        | 超声波模块 GND    |     |

### 运行MicroPython程序

如果你第一次接触树莓派Pico

1. 请参考 [英文教程](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) 或者 [中文教程](https://pidoc.cn/docs/microcontrollers/micropython)安装MicroPython到树莓派Pico
2. 安装[Thonny IDE](https://thonny.org/)

将树莓派Pico和电脑通过USB数据线连接，打开Thonny IDE（在Thonny IDE中，点击右下角选择解释器到你的树莓派Pico），通过编辑器打开本仓库 `DevelepSource/DesktopPet/` 下所有文件，点击另存为保存到树莓派中，命名保持相同即可。

- 如果你不使用超声波测距模块，将 `DevelepSource/DesktopPet/main.py` 文件中第九行改为 `ENABLE_SEND = False` 后，再保存到树莓派pico中。
- main.py 必要的入口文件
- ssd1306.py 显示oled显示屏的封装
- hcsr04.py 超声波测距的封装

重新拔插一下USB接口，如果能看到LED屏幕亮起，并且舵机转动（如果没有转动，你可以趁着没连接USB之前，把舵机角度掰偏一点），说明程序运行成功，接线以及所有硬件都是好的。

### 组装

1. 将云台组装起来
2. 将云台底部固定住，你可以采用硬纸板/纸盒/木片等任何物体
3. 将oled显示屏用胶水、胶带等任何方式固定在云台上方
4. (如果你使用超声波测距模块)用线/皮筋将超声波测距模块固定在oled屏幕上方
5. (可选)将杜邦线抓住，整理一下，用轧带/胶带捆起来，这样会看起来更整洁美观

### 通过上位机+LLM控制树莓派Pico

1. 打开设备管理器/Thonny IDE，找到树莓派Pico插入后的端口信息。
   
   ![port number.jpg](C:\Users\29435\Desktop\desktop-pet-pr\desktop-pet\docs\Images\port%20number.jpg)
2. **关闭Thonny IDE，重新拔插一下树莓派Pico的USB接口（非常重要）**。
   
   
   
   <mark>以下操作均在其他的编译软件，如PyCharm，可结合install-tips中readme文档使用 。</mark>
3. Clone 本仓库，修改 `Source/config.yaml` 文件中的 `LLM` 为 ernie, 修改 `ErnieToken` 为你的Token（从 https://aistudio.baidu.com/account/accessToken 获取，本仓库使用ernie3.5，应该是免费的），如果你希望使用本地/其他大模型，请参考 [README](../../README.md)
4. 安装requirements.txt中的库(pip install -r requirements.txt)
5. 若你使用超声波测距模块，修改 `Source/config.yaml` 中 `DesktopPetReceive` 为1（延迟有点高）
6. 若你不使用超声波测距模块，修改 `Source/config.yaml` 中 `DesktopPetReceive` 为0
7. 运行 `main_PetChat.py` 文件，会出现一个指令窗口。
   
   
   
   ![DesktopPet-window.jpg](C:\Users\29435\Desktop\desktop-pet-pr\desktop-pet\docs\Images\DesktopPet-window.jpg)
8. 输入你的端口号，点击 `Connect`，输入指令，即可通过大模型输出oled屏幕想要展示的颜文字，以及两个舵机的动作。

![DesktopPet-example.jpg](C:\Users\29435\Desktop\desktop-pet-pr\desktop-pet\docs\Images\DesktopPet-example.jpg)

### 更换大模型

如果你不想使用文心一言，在这里提供两种其他的大模型调用方案：

1. 基于Openvino量化后的 GLM3 模型
   - 根据 https://github.com/openvino-dev-samples/chatglm3.openvino 获取量化后的 GLM3 模型，并安装相关依赖
   - 将量化后的模型拷贝到项目文件夹 `/Source/Model/chatglm3-6b-ov` 文件夹下（文件夹下包含 `openvino_model.bin`, `openvino_model.xml` 等文件）
   - 在 `/Source/config.json` 文件中配置如下字段
     
     ```json
     LLM: glm3
     GLM3Directory: Source/Model/chatglm3-6b-ov
     ```
2. 远程服务器部署
   - 以部署Qwen2为例，参考 `https://github.com/QwenLM/Qwen` 下载相关依赖后，在远程服务器运行gradio脚本（可以参考 `/Scripts/gradio_code_qwen.py`
   - 在 `/Source/config.json` 文件中配置如下字段
     
     ```json
     LLM: GRADIO
     GradioURL: http://116.62.10.217:8890/ # 116.62.10.217需要改成你自己的服务器IP，8890需要改成你自己的端口号
     ```

## 代码说明

### 代码结构

这个代码最开是的时候并不是专门针对树莓派Pico的桌面宠物设计的，因此部分结构可能看起来费劲一点，在此特别解释：

1. Tools/Classes/SerialClass.py 文件是串口通信的封装，用于和树莓派Pico进行通信
2. Tools/LLM 文件夹是使用大模型进行交互的封装
3. Tools/Windows/petchatbox.py 是上位机界面，用于和树莓派Pico进行通信
4. Tools/Windows/*/petchatbox.py 是上位机界面的变量定义、布局定义、事件绑定等

### 无超声波测距模块的代码逻辑说明

- 上位机代码(PC代码)
1. 上位机代码首先基于 pyserial 建立了和树莓派Pico的串口通信
2. 上位机代码通过LLM将用户输入，转化为树莓派Pico的相应信息
3. 上位机代码通过串口通信将指令信息发送给树莓派Pico
- 下位机代码(树莓派Pico代码)
1. 初始化引脚
2. 初始化oled显示屏内容，并且将舵机转动到默认位置
3. 通过串口通信等待接收上位机发送的指令
4. 接收到指令后，根据指令更新oled显示屏内容，并执行舵机动作
5. 将舵机转回默认角度
6. 循环3-5

### 有超声波测距模块的代码逻辑说明

- 上位机代码(PC代码)
1. 上位机代码首先基于 pyserial 建立了和树莓派Pico的串口通信

2. 上位机代码开启线程，重复进行Serial信息发送和读取，此时发送的都是空命令(Pico接收到会忽略)

3. 上位机代码开启线程，重复根据串口收到的信息(测距结果)进行分析 

4. 上位机代码通过LLM将用户输入，转化为树莓派Pico的相应信息 

5. 上位机代码通过串口通信将指令信息发送给树莓派Pico
- 下位机代码(树莓派Pico代码)
1. 初始化引脚

2. 初始化oled显示屏内容，并且将舵机转动到默认位置

3. 通过串口通信等待接收上位机发送的指令

4. 通过串口通信向上位机反馈超声测距结果

5. 接收到指令后，根据指令更新oled显示屏内容，并执行舵机动作

6. 将舵机转回默认角度

7. 循环3-6
- 流程图
  ![DesktopPet_workflow.png](Images/DesktopPet_workflow.png)

## 开发者的展示环节

有的开发者确实有大病，不管什么都要找个盒子装起来=w=
![DesktopPet_Box.jpg](Images/DesktopPet_Box.jpg)
