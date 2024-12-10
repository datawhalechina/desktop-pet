# 基于文心一言和树莓派Pico的最简易桌面宠物

本界面介绍了如何通过最低50元人民币左右的金额（只是估算，可能需要更多），购买一整套组件，自己搭建一个如下图所示的硬件结构，通过UWB口连接电脑，当你输入信息的时候，屏幕上会显示颜文字，并配合一些动作。

![DesktopPet_demo.png](./docs/Images/DesktopPet_demo.jpg)

除此之外，你也可以再外接一个感知设备，如下图所示，增加了一个雷达测距工具（硬件成本仅增加了3块多），从而你可以通过硬件传感器感知周围的状态，并反馈给电脑。但这会导致代码逻辑非常复杂，所以本文会同时介绍如何无雷达和有雷达的两种情况。如果你对这一切都不熟悉，可以仅关注不包含雷达的版本，作为你的新手入门。

![DesktopPet_demo2.png](./docs/Images/DesktopPet_demo2.jpg)

不加载雷达时，仅能通过电脑端交互，加载雷达后，可以基于你的手指动作进行交互~示例如下：

![DesktopPet_demo.gif](./docs/Images/DesktopPet_demo.gif)
![DesktopPet_demo.gif2](./docs/Images/DesktopPet_demo2.gif)

安装流程详见docs文档，如果在安装过程中出现疑问，请移步install-tips（强烈建议先看一遍再里面的注意事项再来进行连线和舵机安装！）

## 参与贡献

- 如果你想参与到项目中来欢迎查看项目的 [Issue]() 查看没有被分配的任务。
- 如果你发现了一些问题，欢迎在 [Issue]() 中进行反馈🐛。
- 如果你对本项目感兴趣想要参与进来可以通过 [Discussion]() 进行交流💬。

如果你对 Datawhale 很感兴趣并想要发起一个新的项目，欢迎查看 [Datawhale 贡献指南](https://github.com/datawhalechina/DOPMC#%E4%B8%BA-datawhale-%E5%81%9A%E5%87%BA%E8%B4%A1%E7%8C%AE)。

## 贡献者名单

| 姓名 | 职责 | 简介 |
| :----| :---- | :---- |
| Liyulingyue | 项目负责人 | 一个擅长烂尾的开发者 |


## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg" width = "180" height = "180">
</div>
