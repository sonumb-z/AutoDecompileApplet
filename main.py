import json
import logging
import os
import subprocess
import sys
import time
import argparse
import shutil

import requests
from flask import Flask, request, render_template, redirect, url_for, jsonify, abort
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Lock

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--appletDir', default='E:\\1qq\\WeChat Files\\Applet', help='监控目录|微信小程序缓存目录Applet')
parser.add_argument('--outputDir', default='D:\\PycharmProjects\\AutoDecompileApplet\\output', help='输出目录')
args = parser.parse_args()

APPLET_DIR = args.appletDir
DEFAULT_OUTPUT_DIR = args.outputDir

if not os.path.exists(DEFAULT_OUTPUT_DIR):
        try:
            os.makedirs(DEFAULT_OUTPUT_DIR)
            print(f"输出目录已创建: {DEFAULT_OUTPUT_DIR}")
        except Exception as e:
            print(f"创建输出目录失败: {str(e)}")
            sys.exit(1)
else:
    print(f"输出目录已存在: {DEFAULT_OUTPUT_DIR}")

monitor_running = False
observer = None
latest_applet_dir = None

startDecompile = None
endDecompile = None  # 新增全局变量
lock = Lock()  # 新增线程锁

HEADERS = {
    "Accept-Encoding": "gzip",
    "Content-Type": "application/json;charset=utf-8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}
URL = "https://kainy.cn/api/weapp/info/"


def getAppletNickname(appId):
    try:
        res = requests.post(
            url=URL,
            headers=HEADERS,
            data=json.dumps({"appid": appId}),
            verify=False
        )
        tmp = res.json()
        print(res)
        if not tmp or "data" not in tmp:
            res_json = {
                "nickname": "查询异常",
                "username": "查询异常",
                "description": "查询异常：未返回data字段",
                "avatar": "查询异常",
                "uses_count": "查询异常",
                "principal_name": "查询异常"
            }
        else:
            res_json = tmp["data"]
            print(res_json)
        nickname = res_json["nickname"]
        print(nickname)
        return nickname
    except Exception as e:
        logging.info(f"获取小程序名称失败：{str(e)}", "error")
        return "unknown"


def auto_compile(appletDir, appId, appletOutputDir, appletNickname):
    try:
        print("开始反编译")

        wxapkg_files = []
        for root, dirs, files in os.walk(os.path.join(appletDir, appId)):
            for file in files:
                if file.endswith(".wxapkg"):
                    wxapkg_files.append(os.path.join(root, file))
                    print("找到了。。。")

        if not wxapkg_files:
            print("没有找到。。。")
            raise FileNotFoundError(f"未找到 .wxapkg 文件在目录 {os.path.join(appletDir, appId)}")

        global startDecompile
        startDecompile = 1

        shell = f'''wxapkg.exe unpack -o "{appletOutputDir}" -r "{os.path.join(appletDir, appId)}"'''
        sys2 = subprocess.Popen(shell, shell=True)
        sys2.wait()

        # 使用锁保护共享变量
        with lock:
            global endDecompile
            endDecompile = 1
        logging.info("反编译已完成")
    except Exception as e:
        logging.error(f"反编译失败：{str(e)}")


class AppletDirHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            dir_name = os.path.basename(event.src_path)
            if dir_name.startswith('wx'):
                global latest_applet_dir
                latest_applet_dir = event.src_path
                print(f"检测到新目录：{dir_name}")
                time.sleep(2)

                appId = dir_name
                appletNickname = getAppletNickname(appId)
                appletOutputDir = os.path.join(DEFAULT_OUTPUT_DIR, appletNickname)

                # 正确启动线程（修正参数传递方式）
                #Thread(target=self.auto_compile, args=(APPLET_DIR, appId, appletOutputDir, appletNickname)).start()
                auto_compile(APPLET_DIR, appId, appletOutputDir, appletNickname)

@app.route('/')
def index():
    return render_template('index.html',
                           applet_dir=APPLET_DIR,
                           monitor_status="运行中" if monitor_running else "未启动")

@app.route('/start_monitor', methods=['POST'])
def start_monitor():
    global monitor_running, observer
    if not monitor_running:
        observer = Observer()
        event_handler = AppletDirHandler()
        observer.schedule(event_handler, APPLET_DIR, recursive=False)
        observer.start()
        monitor_running = True
        logging.info("监控已启动", "success")
    return redirect(url_for('index'))


@app.route('/stop_monitor', methods=['POST'])
def stop_monitor():
    global monitor_running, observer
    if monitor_running:
        observer.stop()
        observer.join()
        monitor_running = False
        logging.info("监控已停止", "success")
    return redirect(url_for('index'))


@app.route('/applet_clear', methods=['POST'])
def clear_applet_dir():
    confirm = request.form.get('confirm')
    if confirm != 'true':
        logging.info("请确认操作：清空目录可能包含重要数据", "warning")
        return redirect(url_for('index'))

    try:
        for entry in os.scandir(APPLET_DIR):
            if entry.is_dir() and entry.name.startswith('wx') and len(entry.name) == 18:
                shutil.rmtree(entry.path)
            else:
                pass
        logging.info(f"目录 {APPLET_DIR} 已清空", "success")
    except Exception as e:
        logging.info(f"清空目录失败：{str(e)}", "error")
    return redirect(url_for('index'))


@app.route('/check_status')
def check_status():
    global endDecompile, startDecompile
    with lock:
        if endDecompile:
            startDecompile = None
            endDecompile = None  # 重置状态
            return jsonify({'status': 'end'})

    if startDecompile:
        return jsonify({'status': 'start'})
    return jsonify({'status': 'pending'})


@app.route('/browse')
@app.route('/browse/<path:subpath>')
def browse_output(subpath=""):
    """
    展示指定目录的文件和子目录列表
    """
    # 构造当前目录的绝对路径
    current_dir = os.path.join(DEFAULT_OUTPUT_DIR, subpath)

    # 检查路径是否存在
    if not os.path.exists(current_dir):
        abort(404)  # 返回 404 错误页面

    # 获取当前目录的文件和子目录列表
    try:
        entries = os.listdir(current_dir)
        files = []
        for entry in entries:
            entry_path = os.path.join(current_dir, entry)
            is_dir = os.path.isdir(entry_path)
            relative_path = os.path.join(subpath, entry)  # 相对于根目录的路径
            files.append({
                "name": entry,
                "is_dir": is_dir,
                "url": f"/browse/{relative_path}" if is_dir else f"/view/{relative_path}"
            })
        return render_template('browse.html', files=files, current_path=subpath)
    except Exception as e:
        return f"发生错误: {str(e)}", 500

@app.route('/view/<path:filepath>')
def view_file(filepath):
    """
    查看文件内容
    """
    file_path = os.path.join(DEFAULT_OUTPUT_DIR, filepath)

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        abort(404)  # 返回 404 错误页面

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().replace('\t', ' ')
        return render_template('view.html', filename=os.path.basename(file_path), content=content)
    except Exception as e:
        return f"无法读取文件: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)