# app.py
# Streamlit 前端應用程式：輸入 PI 和 minterms，呼叫後端最小化
# By: 庭瑄

import streamlit as st
import requests

# ✅ 頁面基本設定：標題與版面配置
st.set_page_config(page_title="Patrick Method 最小化工具", layout="centered")

# ✅ 顯示標題與說明文字
st.title("🌟 Patrick Method SOP 最小化工具")
st.write("輸入 Prime Implicants（PI）與 minterms，系統將使用 Patrick Method 找出最小 SOP 解。")

# =============================
# 使用者輸入區（Prime Implicants）
# =============================
pis_input = st.text_area(
    "輸入 Prime Implicants（每行一個，例如 1-0 或 -11）：",
    height=150,
    placeholder="例如：\n1-0\n-11"
)

# =============================
# 使用者輸入區（Minterms）
# =============================
minterms_input = st.text_area(
    "輸入 minterms（每行一個，例如 100 或 011）：",
    height=150,
    placeholder="例如：\n100\n110"
)

# =============================
# 當使用者按下按鈕時觸發後端呼叫
# =============================
if st.button("🚀 開始最小化"):
    # 將每一行輸入去除空白並組成 list
    pis = [line.strip() for line in pis_input.splitlines() if line.strip()]
    minterms = [line.strip() for line in minterms_input.splitlines() if line.strip()]

    # 如果任一欄為空，提示錯誤
    if not pis or not minterms:
        st.error("請輸入 PI 和 minterms，兩者皆不可為空。")
    else:
        # 準備要送到後端的 JSON 資料格式
        payload = {
            "pis": pis,
            "outputs": {
                "F": minterms  # 單輸出格式，key 為 "F"
            }
        }

        try:
            # ✅ 傳送 POST 請求到雲端 Flask Server（修改成妳的網址）
            response = requests.post("https://patrick-osj5.onrender.com/minimize", json=payload)

            # 若回應成功，顯示結果
            if response.status_code == 200:
                result = response.json()
                st.success("✅ 最小化結果如下：")
                for output, detail in result.items():
                    final_terms = detail.get("Final", [])
                    st.code(f"{output} = {' + '.join(final_terms)}", language="text")

            else:
                # 回應失敗，顯示錯誤訊息
                st.error(f"❌ 錯誤：{response.json().get('error', '未知錯誤')}")
        except requests.exceptions.RequestException:
            # 無法連線到 server
            st.error("❌ 無法連線至 Flask 後端，請確認伺服器網址正確。")
