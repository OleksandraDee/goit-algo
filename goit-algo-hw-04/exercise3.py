import random, timeit, platform, sys
from statistics import median
from pathlib import Path

def insertion_sort(a):
    arr = a[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    if i < len(left): out.extend(left[i:])
    if j < len(right): out.extend(right[j:])
    return out

def gen_data(n, kind, seed=42):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(0, 10**9) for _ in range(n)]
    if kind == "reversed":
        return list(range(n, 0, -1))
    if kind == "nearly":
        x = list(range(n))
        swaps = max(1, n // 100)
        for _ in range(swaps):
            i = rng.randrange(n); j = rng.randrange(n)
            x[i], x[j] = x[j], x[i]
        return x
    if kind == "few_unique":
        return [rng.randrange(10) for _ in range(n)]
    return [rng.randint(0, 10**9) for _ in range(n)]

def bench(func, base, repeat=5, number=1):
    t = timeit.Timer(lambda: func(base.copy()))
    xs = t.repeat(repeat=repeat, number=number)
    return min(xs) / number

def main():
    algos = [
        ("insertion", insertion_sort),
        ("merge", merge_sort),
        ("timsort", sorted),
    ]
    kinds = ["random", "nearly", "reversed", "few_unique"]
    sizes = [1000, 5000, 10000, 20000]
    base_data = {}
    for n in sizes:
        for k in kinds:
            base_data[(n, k)] = gen_data(n, k, seed=12345)
    results = []
    for n in sizes:
        for k in kinds:
            base = base_data[(n, k)]
            for name, fn in algos:
                if name == "insertion" and n > 5000:
                    continue
                t = bench(fn, base, repeat=5, number=1)
                results.append((name, n, k, t))
                print(f"{name:9s} n={n:6d} kind={k:12s} time={t:.6f}s")
    by_key = {}
    for name, n, k, t in results:
        by_key.setdefault((n, k), {})[name] = t
    lines = []
    lines.append("# Порівняння алгоритмів сортування\n")
    lines.append(f"- Python: {sys.version.split()[0]}\n- Platform: {platform.platform()}\n")
    header = "| n | dataset | insertion | merge | timsort | winner |\n|---:|:--------|---------:|------:|-------:|:-------|\n"
    lines.append(header)
    for n in sizes:
        for k in kinds:
            row = by_key.get((n, k), {})
            ins = row.get("insertion")
            mer = row.get("merge")
            tim = row.get("timsort")
            def fmt(x): return f"{x:.6f}s" if x is not None else "-"
            best = None
            vals = {a: row.get(a) for a in ("insertion","merge","timsort")}
            vals = {a:v for a,v in vals.items() if v is not None}
            if vals:
                best = min(vals, key=vals.get)
            lines.append(f"| {n} | {k} | {fmt(ins)} | {fmt(mer)} | {fmt(tim)} | {best or '-'} |\n")
    notes = []
    notes.append("\n## Висновки\n")
    notes.append("1. На всіх наборах даних найчастіше перемагає `timsort` (вбудоване `sorted`).\n")
    notes.append("2. На малих вибірках `insertion` може бути конкурентним, але росте квадратично й програє на більших n.\n")
    notes.append("3. `merge` стабільний і показує близький до лінійно-логарифмічного час; для великих n він помітно швидший за `insertion`, але поступається `timsort`, що адаптується до майже відсортованих даних і багатьох дубльованих значень.\n")
    lines.extend(notes)
    Path("readme.md").write_text("".join(lines), encoding="utf-8")
    print("\nЗвіт записано у readme.md")

if __name__ == "__main__":
    main()
