import tkinter as tk
from tkinter import messagebox
import requests

# ✅ 修改為妳伺服器的區網 IP 和 port
SERVER_URL = "http://127.0.0.1:5000/minimize"



def send_request():
    pis = entry_inputs.get().strip().split(",")
    outputs_raw = entry_outputs.get("1.0", tk.END).strip().split("\n")

    try:
        # 👇 每一行轉成 list：['100', '110'] 等
        outputs = {
            f"F{i+1}": [m.strip() for m in line.split(",") if m.strip()]
            for i, line in enumerate(outputs_raw)
        }

        payload = {
            "pis": [p.strip() for p in pis if p.strip()],
            "outputs": outputs
        }

        response = requests.post(SERVER_URL, json=payload)

        if response.ok:
            result = response.json()
            result_text.delete("1.0", tk.END)
            for out, detail in result.items():
                result_text.insert(tk.END, f"📌 {out}\n")
                result_text.insert(tk.END, f"  🟩 EPI   : {detail['EPI']}\n")
                result_text.insert(tk.END, f"  ➕ Extra : {detail['Extra']}\n")
                result_text.insert(tk.END, f"  ✅ Final : {detail['Final']}\n\n")
        else:
            messagebox.showerror("伺服器錯誤", f"❌ 回應失敗：{response.status_code}")

    except Exception as e:
        print("⚠️ DEBUG:", e)
        messagebox.showerror("錯誤", f"無法連線至伺服器：\n{e}")

# ====== GUI 建立 ======
root = tk.Tk()
root.title("Patrick Method App")
root.geometry("500x400")

tk.Label(root, text="輸入變數（用逗號隔開）:").pack()
entry_inputs = tk.Entry(root, width=50)
entry_inputs.pack()

tk.Label(root, text="輸出表達式（每行一個）:").pack()
entry_outputs = tk.Text(root, height=5, width=50)
entry_outputs.pack()

tk.Button(root, text="送出給 Server", command=send_request).pack(pady=10)

tk.Label(root, text="最小化 SOP 結果:").pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
