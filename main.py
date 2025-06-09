# main.py
# ✅ 啟動主控腳本：同時執行 Flask 後端與 Streamlit 前端
# By: 瑄庭

import subprocess
import threading
import os
import sys

def resource_path(relative_path):
    """
    ✅ 獲取檔案的絕對路徑
    若使用 PyInstaller 打包，則會使用 _MEIPASS 為暫存目錄
    否則回傳目前目錄下的檔案路徑
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller 打包後的暫存目錄
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ✅ 啟動 Flask 後端（背景執行）
def run_flask():
    subprocess.Popen(["python", resource_path("server.py")])  # 非阻塞方式執行

# ✅ 啟動 Streamlit 前端（主線程執行）
def run_streamlit():
    subprocess.run(["streamlit", "run", resource_path("app.py")])  # 阻塞直到退出

# ✅ 主程式執行區：先開後端，再開前端
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # 用子執行緒開 Flask
    run_streamlit()  # 主執行緒跑 Streamlit
