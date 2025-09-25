import re, timeit
from pathlib import Path

def boyer_moore_horspool(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    skip = {c: m - i - 1 for i, c in enumerate(pattern[:-1])}
    i = m - 1
    while i < n:
        k = 0
        while k < m and pattern[m-1-k] == text[i-k]:
            k += 1
        if k == m:
            return i - m + 1
        i += skip.get(text[i], m)
    return -1

def kmp_table(p):
    lps = [0]*len(p)
    j = 0
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = lps[j-1]
        if p[i] == p[j]:
            j += 1
            lps[i] = j
    return lps

def kmp_search(t, p):
    m = len(p)
    if m == 0:
        return 0
    lps = kmp_table(p)
    j = 0
    for i, ch in enumerate(t):
        while j > 0 and ch != p[j]:
            j = lps[j-1]
        if ch == p[j]:
            j += 1
            if j == m:
                return i - m + 1
    return -1

def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    powm = pow(base, m-1, mod)
    hp = 0
    ht = 0
    for i in range(m):
        hp = (hp*base + ord(pattern[i])) % mod
        ht = (ht*base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if hp == ht and text[i:i+m] == pattern:
            return i
        if i < n - m:
            ht = (ht - ord(text[i]) * powm) % mod
            ht = (ht*base + ord(text[i+m])) % mod
    return -1

def read_text(p: Path):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return p.read_text(errors="ignore")

def pick_patterns(text, want_len_exist=12):
    words = re.findall(r"\w{6,}", text)
    if words:
        w = words[len(words)//2]
        exist = w[:want_len_exist] if len(w) >= want_len_exist else w
    else:
        if len(text) >= want_len_exist:
            mid = len(text)//2
            exist = text[mid:mid+want_len_exist]
        else:
            exist = text
    miss = exist
    if miss:
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for ch in chars:
            if not miss.endswith(ch):
                cand = miss[:-1] + ch
                if cand not in text:
                    miss = cand
                    break
    else:
        miss = "qzjxvkwp"
        while miss in text:
            miss += "z"
    return exist, miss

def bench_one(fn, text, pattern, repeat=9, number=1):
    t = timeit.Timer(lambda: fn(text, pattern)).repeat(repeat=repeat, number=number)
    return min(t)/number

def main():
    here = Path(__file__).parent
    f1 = here / "file1.txt"
    f2 = here / "file2.txt"
    if not f1.exists() or not f2.exists():
        raise SystemExit("Покладіть file1.txt і file2.txt у ту саму теку зі скриптом.")
    text1 = read_text(f1)
    text2 = read_text(f2)
    p1_exist, p1_miss = pick_patterns(text1)
    p2_exist, p2_miss = pick_patterns(text2)
    algos = {
        "Boyer-Moore": boyer_moore_horspool,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp,
    }
    cases = {
        ("file1", "exist"): (text1, p1_exist),
        ("file1", "miss"):  (text1, p1_miss),
        ("file2", "exist"): (text2, p2_exist),
        ("file2", "miss"):  (text2, p2_miss),
    }
    results = {}
    for (fname, kind), (tx, pat) in cases.items():
        results[(fname, kind)] = {}
        for name, fn in algos.items():
            sec = bench_one(fn, tx, pat, repeat=9, number=1)
            results[(fname, kind)][name] = sec
    print("\nПатерни:")
    print(f"file1 exist: {p1_exist!r}")
    print(f"file1 miss : {p1_miss!r}")
    print(f"file2 exist: {p2_exist!r}")
    print(f"file2 miss : {p2_miss!r}")
    print("\nРезультати (секунди, менше — краще):")
    for fname in ("file1","file2"):
        for kind in ("exist","miss"):
            row = results[(fname,kind)]
            best = min(row, key=row.get)
            msg = " | ".join(f"{k}: {v:.6f}s" for k,v in row.items())
            print(f"{fname:5s} {kind:5s} -> {msg}  | best: {best}")
    agg_per_text = {}
    for fname in ("file1","file2"):
        sums = {k: 0.0 for k in algos}
        for kind in ("exist", "miss"):
            for k, v in results[(fname, kind)].items():
                sums[k] += v
        best = min(sums, key=sums.get)
        agg_per_text[fname] = (best, sums)
    overall = {k: 0.0 for k in algos}
    for fname in ("file1", "file2"):
        sums_dict = agg_per_text[fname][1]
        for k, v in sums_dict.items():
            overall[k] += v
    overall_best = min(overall, key=overall.get)
    print("\nПереможці по текстах (сума exist+miss):")
    for fname, (best, sums) in agg_per_text.items():
        print(f"{fname}: {best}  " + " | ".join(f"{k}={sums[k]:.6f}s" for k in algos))
    print(f"\nЗагальний переможець: {overall_best}")
    md = []
    md.append("# Порівняння алгоритмів пошуку підрядка\n\n")
    md.append(f"Файли: `{f1.name}`, `{f2.name}`\n\n")
    md.append("## Патерни\n")
    md.append(f"- file1 exist: `{p1_exist}`\n- file1 miss: `{p1_miss}`\n")
    md.append(f"- file2 exist: `{p2_exist}`\n- file2 miss: `{p2_miss}`\n\n")
    md.append("## Результати (секунди)\n\n")
    md.append("| файл | кейс | Boyer-Moore | KMP | Rabin-Karp | найкращий |\n|:----:|:----:|------------:|----:|-----------:|:----------|\n")
    for fname in ("file1","file2"):
        for kind in ("exist","miss"):
            row = results[(fname,kind)]
            best = min(row, key=row.get)
            md.append(f"| {fname} | {kind} | {row['Boyer-Moore']:.6f} | {row['KMP']:.6f} | {row['Rabin-Karp']:.6f} | {best} |\n")
    md.append("\n## Переможці по текстах (сума exist+miss)\n\n")
    for fname,(best,sums) in agg_per_text.items():
        md.append(f"- **{fname}**: {best}  (BM={sums['Boyer-Moore']:.6f}s, KMP={sums['KMP']:.6f}s, RK={sums['Rabin-Karp']:.6f}s)\n")
    md.append(f"\n**Загалом**: переможець — **{overall_best}**\n\n")
    md.append("## Висновки\n")
    md.append("- Boyer–Moore (Horspool) часто найшвидший на природних текстах, особливо для відсутніх підрядків.\n")
    md.append("- KMP стабільно лінійний і може лідирувати для коротких патернів або малих абеток.\n")
    md.append("- Рабін–Карп корисний при множинних патернах; для одного зазвичай повільніший за BM/KMP.\n")
    Path("README.md").write_text("".join(md), encoding="utf-8")
    print("\nЗвіт записано у README.md")

if __name__ == "__main__":
    main()  
