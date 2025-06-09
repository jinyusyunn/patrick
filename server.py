from flask import Flask, request, jsonify
from patrick_method import patrick_minimize, multi_output_minimize

# ✅ 建立 Flask 應用
app = Flask(__name__)

# ✅ 設定一個 POST API 路由 /minimize，用來處理 Patrick Method 最小化的請求
@app.route('/minimize', methods=['POST'])
def minimize():
    data = request.json  # 取得前端傳來的 JSON 輸入資料
    pis = data['pis']  # Prime Implicants，格式如 ['1-0', '-11']
    outputs = data['outputs']  # 輸出對應的 minterms，格式如 {'F': ['100', '110']}

    if len(outputs) == 1:
        # ✅ 若只有一個輸出（單輸出），使用 patrick_minimize
        out_name = list(outputs.keys())[0]
        result = {out_name: patrick_minimize(pis, outputs[out_name])}
    else:
        # ✅ 多輸出情況，使用 multi_output_minimize 分別計算每個輸出
        result = multi_output_minimize(pis, outputs)

    return jsonify(result)  # 回傳 JSON 結果

# ✅ 當直接執行 server.py 時，開啟本地伺服器（供除錯使用）
# 若用 Gunicorn 部署到 Render，這段會被跳過
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # 本地啟動 Flask，監聽所有網卡（可跨裝置連線）
