# main.py
import subprocess
import threading
import os
import sys

def resource_path(relative_path):
    """獲取打包後的實際路徑"""
    try:
        base_path = sys._MEIPASS  # PyInstaller 打包後的暫存路徑
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def run_flask():
    subprocess.Popen(["python", resource_path("server.py")])

def run_streamlit():
    subprocess.run(["streamlit", "run", resource_path("app.py")])

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_streamlit()
