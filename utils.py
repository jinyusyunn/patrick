# utils.py
# 實用工具函式，用於轉換格式與驗證輸入
# By: 瑄庭

def truth_table_to_minterms(table):
    """
    將布林真值表轉換為 SOP minterms
    輸入格式：list of tuples [(input, output), ...]
    例如：[("000", 0), ("001", 1)] -> ["001"]
    """
    return [inputs for inputs, output in table if output == 1]

def validate_pi_format(pis):
    """
    驗證所有 Prime Implicants 是否為合法格式（例如：1-0、-11）
    """
    for pi in pis:
        if not all(c in '01-' for c in pi):
            return False
    return True

def validate_minterms_format(minterms):
    """
    驗證所有 minterms 是否只包含 0 或 1 且長度一致
    """
    if not minterms:
        return False
    length = len(minterms[0])
    for m in minterms:
        if any(c not in '01' for c in m) or len(m) != length:
            return False
    return True
