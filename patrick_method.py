from itertools import combinations

def match(pi, minterm):
    for p, m in zip(pi, minterm):
        if p != '-' and p != m:
            return False
    return True

def build_cover_table(pis, minterms):
    table = {}
    for pi in pis:
        table[pi] = set()
        for m in minterms:
            if match(pi, m):
                table[pi].add(m)
    return table

def find_epis(table, minterms):
    epis = set()
    uncovered = set(minterms)
    for m in minterms:
        covering_pis = [pi for pi in table if m in table[pi]]
        if len(covering_pis) == 1:
            epi = covering_pis[0]
            epis.add(epi)
            uncovered -= table[epi]
    return epis, uncovered

def patrick_minimize(pis, minterms):
    table = build_cover_table(pis, minterms)
    epis, uncovered = find_epis(table, minterms)

    non_epi = [pi for pi in pis if pi not in epis]
    min_cover = None

    for i in range(1, len(non_epi) + 1):
        for comb in combinations(non_epi, i):
            cover = set()
            for pi in comb:
                cover |= table[pi]
            if uncovered.issubset(cover):
                min_cover = set(comb)
                break
        if min_cover:
            break

    final = sorted(list(epis | (min_cover if min_cover else set())))

    return {
        "EPI": sorted(list(epis)),
        "Extra": sorted(list(min_cover)) if min_cover else [],
        "Final": final
    }

def multi_output_minimize(pis, outputs):
    results = {}
    for name, minterms in outputs.items():
        results[name] = patrick_minimize(pis, minterms)
    return results
