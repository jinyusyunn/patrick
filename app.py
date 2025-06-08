# app.py
# Streamlit 前端應用程式：輸入 PI 和 minterms，呼叫後端最小化
# By: 瑄庭

import streamlit as st
import requests

st.set_page_config(page_title="Patrick Method 最小化工具", layout="centered")

st.title("🌟 Patrick Method SOP 最小化工具")
st.write("輸入 Prime Implicants（PI）與 minterms，系統將使用 Patrick Method 找出最小 SOP 解。")

# 輸入 Prime Implicants
pis_input = st.text_area(
    "輸入 Prime Implicants（每行一個，例如 1-0 或 -11）：",
    height=150,
    placeholder="例如：\n1-0\n-11"
)

# 輸入 Minterms
minterms_input = st.text_area(
    "輸入 minterms（每行一個，例如 100 或 011）：",
    height=150,
    placeholder="例如：\n100\n110"
)

# 執行按鈕
if st.button("🚀 開始最小化"):
    # 解析輸入
    pis = [line.strip() for line in pis_input.splitlines() if line.strip()]
    minterms = [line.strip() for line in minterms_input.splitlines() if line.strip()]

    if not pis or not minterms:
        st.error("請輸入 PI 和 minterms，兩者皆不可為空。")
    else:
        # 準備資料
        payload = {
            "pis": pis,
            "outputs": {
                "F": minterms  # 單輸出時使用 output 名為 "F"
            }
        }

        try:
            # 傳送 POST 請求到後端 Flask API
            response = requests.post("http://localhost:5000/minimize", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.success("✅ 最小化結果如下：")
                for output, terms in result.items():
                    st.code(f"{output} = {' + '.join(terms)}", language="text")
            else:
                st.error(f"❌ 錯誤：{response.json().get('error', '未知錯誤')}")
        except requests.exceptions.RequestException:
            st.error("❌ 無法連線至 Flask 後端，請確認 `server.py` 已啟動。")
