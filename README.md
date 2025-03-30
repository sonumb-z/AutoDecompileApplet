# 自动化微信小程序反编译工具 🚀

[![GitHub](https://img.shields.io/badge/GitHub-sonumb%2FAutoDecompileApplet-blue)](https://github.com/sonumb-z/AutoDecompileApplet)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

通过 Web 界面实现微信小程序反编译流程的自动化监控与执行，无缝衔接 FindSomething、HaE、BurpSuite 等安全分析工具，提升小程序逆向效率。

---

## 🌟 功能亮点

| 功能模块         | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| **实时目录监控** | 每 2 秒扫描小程序缓存目录，自动触发反编译流程                |
| **集成工具链**   | 与 FindSomething、HaE、BurpSuite 等工具无缝衔接，快速定位接口与敏感数据 |

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **Flask**: Web 框架
- **Bootstrap 5**: 前端框架（通过 CDN 自动加载）

### 安装与配置

```bash
# 1. 克隆仓库
git clone https://github.com/sonumb-z/AutoDecompileApplet.git
cd AutoDecompileApplet

# 2. 配置参数
# 在命令行中指定：
#   --appletDir: "E:\\WeChat Files\\Applet"  # 小程序缓存目录，需替换成自己的
#   --outputDir: "D:\\PycharmProjects\\AutoDecompileApplet\\output" # 反编译输出目录，需替换成自己的
# 或者直接修改 main.py 中的默认参数

# 3. 启动服务
python main.py --appletDir="E:\\WeChat Files\\Applet" --outputDir="D:\\PycharmProjects\\AutoDecompileApplet\\output"

# 4、桌面bat一键启动服务：命令如下，自行修改路径，保存为bat文件即可
@echo off
REM 自行修改项目中main.py路径、小程序缓存目录、输出目录
python D:\PycharmProjects\AutoDecompileApplet\main.py --appletDir="E:\1qq\WeChat Files\Applet" --outputDir="D:\PycharmProjects\AutoDecompileApplet\result"
pause
```

### 🌐 访问界面

浏览器访问：`http://127.0.0.1:5000`

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601364.png)

## 💡 使用流程

1. **清空缓存** ：点击 `清空目录` 按钮，确保小程序缓存目录干净
2. **启动监控** ：点击 `开始监控`，系统将自动检测新创建的小程序包
3. **触发反编译** ：重新打开目标小程序，系统将自动执行反编译流程
4. **结果查看** ：编译完成后跳转至文件列表，支持直接预览代码与资源文件

## 🛠️ 功能演示

### 🔍 文件浏览器

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601366.png)

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601367.png)

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601368.png)

### 🕵️ 敏感信息扫描

结合 **FindSomething** 插件提取接口：

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601369.png)

联动burp和HaE插件

![](https://cdn.jsdelivr.net/gh/sonumb-z/IMG-Repo@main/img/20250327181601370.png)

## 📖 参考项目

- https://github.com/wux1an/wxapkg
- https://github.com/G0mini/PyBy2
- https://github.com/wwsuixin/ws_tools
