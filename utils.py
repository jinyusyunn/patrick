# utils.py
# 實用工具函式，用於轉換格式與驗證輸入
# By: 瑄庭

def truth_table_to_minterms(table):
    """
    ✅ 將布林真值表轉換為 SOP 所需的 minterms 列表
    👉 輸入格式：list of tuples [(input, output), ...]
       其中 input 是字串（例如 "001"），output 是 0 或 1
    👉 回傳：只取出 output 為 1 的 input，作為 minterm（例如 ["001", "011", ...]）

    例子：
    [("000", 0), ("001", 1), ("010", 1)] → ["001", "010"]
    """
    return [inputs for inputs, output in table if output == 1]

def validate_pi_format(pis):
    """
    ✅ 檢查所有 Prime Implicants 是否為合法格式
    👉 每個 PI 應該只包含 '0', '1' 或 '-'（don't care）
       例如：'1-0', '--1', '011' 都合法，但 '2-0' 或 'a01' 不合法

    回傳：
    - True：所有格式合法
    - False：有一個以上不合法
    """
    for pi in pis:
        if not all(c in '01-' for c in pi):  # 檢查字元是否只包含 0, 1, -
            return False
    return True

def validate_minterms_format(minterms):
    """
    ✅ 驗證所有 minterms 是否為合法格式
    👉 每個 minterm 應只包含 '0' 或 '1'，且長度一致（不能有的長 3、有的長 2）

    回傳：
    - True：格式正確且長度一致
    - False：含非法字元或長度不一致
    """
    if not minterms:
        return False  # 空的直接錯誤

    length = len(minterms[0])  # 第一個 minterm 的長度作為標準

    for m in minterms:
        if any(c not in '01' for c in m) or len(m) != length:
            return False  # 有非法字元或長度不同都錯誤

    return True
