from itertools import combinations  # 用於產生所有可能的 PI 組合

# ✅ 檢查某個 PI（如 1-0）是否能覆蓋某個 minterm（如 100）
def match(pi, minterm):
    for p, m in zip(pi, minterm):
        if p != '-' and p != m:  # '-' 表示 don't care，可以匹配任意值
            return False
    return True

# ✅ 建立每個 PI 可以覆蓋哪些 minterms 的對照表
def build_cover_table(pis, minterms):
    table = {}
    for pi in pis:
        table[pi] = set()
        for m in minterms:
            if match(pi, m):
                table[pi].add(m)
    return table  # 範例：{'1-0': {'100', '110'}, '-11': {'011', '111'}}

# ✅ 找出 EPI（Essential Prime Implicants），也就是**只能被一個 PI 覆蓋的 minterm**
def find_epis(table, minterms):
    epis = set()
    uncovered = set(minterms)  # 尚未被覆蓋的 minterm
    for m in minterms:
        covering_pis = [pi for pi in table if m in table[pi]]  # 有覆蓋這個 minterm 的 PI
        if len(covering_pis) == 1:  # 只有一個 PI 覆蓋，則是 EPI
            epi = covering_pis[0]
            epis.add(epi)
            uncovered -= table[epi]  # 已經被 EPI 覆蓋的不再需要考慮
    return epis, uncovered

# ✅ 主邏輯：使用 Patrick Method 找出最少的 PI 組合來覆蓋所有 minterms
def patrick_minimize(pis, minterms):
    table = build_cover_table(pis, minterms)
    epis, uncovered = find_epis(table, minterms)

    non_epi = [pi for pi in pis if pi not in epis]  # 非 EPI 的 PI
    min_cover = None  # 額外需要的最小覆蓋組合

    # 嘗試所有非 EPI 的組合，找出最小集合可以補足未覆蓋的 minterms
    for i in range(1, len(non_epi) + 1):
        for comb in combinations(non_epi, i):
            cover = set()
            for pi in comb:
                cover |= table[pi]
            if uncovered.issubset(cover):  # 成功覆蓋所有剩下的 minterm
                min_cover = set(comb)
                break
        if min_cover:
            break

    # 整合：EPI + 額外補上的 Cover
    final = sorted(list(epis | (min_cover if min_cover else set())))

    return {
        "EPI": sorted(list(epis)),  # 必要項
        "Extra": sorted(list(min_cover)) if min_cover else [],  # 額外補足項
        "Final": final  # 最終最小 SOP 解
    }

# ✅ 多輸出版本：針對每個輸出都獨立執行 Patrick Method
def multi_output_minimize(pis, outputs):
    results = {}
    for name, minterms in outputs.items():  # 輸入格式如 {'Y1': ['100', '110'], 'Y2': ['011']}
        results[name] = patrick_minimize(pis, minterms)
    return results
