import tkinter as tk
from tkinter import messagebox
import requests

# ✅ 設定雲端伺服器網址（Render 雲端 API）
SERVER_URL = "https://patrick-osj5.onrender.com/minimize"

# ========================
# 發送 POST 請求給 Server
# ========================
def send_request():
    # 取得輸入變數（用逗號隔開），轉為 list
    pis = entry_inputs.get().strip().split(",")

    # 每一行輸出表達式分開處理（每行是一個 function）
    outputs_raw = entry_outputs.get("1.0", tk.END).strip().split("\n")

    try:
        # 每行轉為 list，例如 "100,110" → ['100', '110']
        outputs = {
            f"F{i+1}": [m.strip() for m in line.split(",") if m.strip()]
            for i, line in enumerate(outputs_raw)
        }

        # 建立要送出的 JSON payload
        payload = {
            "pis": [p.strip() for p in pis if p.strip()],
            "outputs": outputs
        }

        # 發送 POST 請求
        response = requests.post(SERVER_URL, json=payload)

        # 若回應成功（200 OK）
        if response.ok:
            result = response.json()
            result_text.delete("1.0", tk.END)  # 清空舊結果

            # 顯示每個輸出的最小 SOP 結果
            for out, detail in result.items():
                result_text.insert(tk.END, f"📌 {out}\n")
                result_text.insert(tk.END, f"  🟩 EPI   : {detail['EPI']}\n")
                result_text.insert(tk.END, f"  ➕ Extra : {detail['Extra']}\n")
                result_text.insert(tk.END, f"  ✅ Final : {detail['Final']}\n\n")

        else:
            # 若伺服器回應錯誤（如 500）
            messagebox.showerror("伺服器錯誤", f"❌ 回應失敗：{response.status_code}")

    except Exception as e:
        # 若請求失敗（如連不上網）
        print("⚠️ DEBUG:", e)
        messagebox.showerror("錯誤", f"無法連線至伺服器：\n{e}")

# ================
# GUI 介面建立區段
# ================
root = tk.Tk()
root.title("Patrick Method App")
root.geometry("500x400")

# ➤ 輸入變數欄位（如 A,B,C）
tk.Label(root, text="輸入變數（用逗號隔開）:").pack()
entry_inputs = tk.Entry(root, width=50)
entry_inputs.pack()

# ➤ 輸出函數表達式輸入區（每行一個 function）
tk.Label(root, text="輸出表達式（每行一個）:").pack()
entry_outputs = tk.Text(root, height=5, width=50)
entry_outputs.pack()

# ➤ 發送按鈕
tk.Button(root, text="送出給 Server", command=send_request).pack(pady=10)

# ➤ 結果輸出顯示區
tk.Label(root, text="最小化 SOP 結果:").pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# ➤ 啟動 GUI 主視窗
root.mainloop()
