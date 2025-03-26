# 微信小程序自动化反编译工具 🚀

[![GitHub](https://img.shields.io/badge/GitHub-sonumb%2FAutoDecompileApplet-blue)](https://github.com/sonumb-z/AutoDecompileApplet)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

通过 Web 界面实现微信小程序反编译流程的自动化监控与执行，无缝衔接 FindSomething、HaE、BurpSuite 等安全分析工具，提升小程序逆向效率。

---

## 🌟 功能亮点

| 功能模块           | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **实时目录监控**   | 每 2 秒扫描小程序缓存目录，自动触发反编译流程                |
| **可视化操作界面** | Bootstrap 5 响应式设计，支持移动端/PC 端自适应               |
| **状态实时反馈**   | 使用 Bootstrap 警报组件显示编译状态（等待/进行中/完成）      |
| **文件浏览器**     | 支持直接查看反编译后的文件内容，支持代码高亮                 |
| **一键清空目录**   | 确认式操作确保操作安全                                       |
| **集成工具链**     | 与 FindSomething、HaE、BurpSuite 等工具无缝衔接，快速定位接口与敏感数据 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Flask Web 框架
- Bootstrap 5 前端框架（自动通过 CDN 加载）

### 步骤指南

```bash
# 1. 克隆仓库
git clone https://github.com/sonumb-z/AutoDecompileApplet.git
cd AutoDecompileApplet

# 2. 配置参数
# --appletDir: "E:\\WeChat Files\\Applet"  # 小程序缓存目录
# --outputDir: "result"                   # 反编译输出目录

# 3. 启动服务
python main.py --appletDir="E:\\WeChat Files\\Applet" --outputDir="result"

# 4. 使用流程
清空小程序缓存-->开始监控-->重新打开小程序-->自动反编译-->查看反编译文件
```

![image-20250326224547555](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326224547555.png)

![image-20250326224625960](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326224625960.png)

![image-20250326225035196](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326225035196.png)



![image-20250326225108368](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326225108368.png)

![image-20250326225136653](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326225136653.png)

![image-20250326225201062](C:\Users\52211\AppData\Roaming\Typora\typora-user-images\image-20250326225201062.png)
