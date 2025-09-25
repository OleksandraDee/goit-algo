# coins_hw.py
from math import inf
from time import perf_counter
from pathlib import Path

COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount: int, coins=COINS) -> dict[int,int]:
    res = {}
    for c in sorted(coins, reverse=True):
        if amount <= 0:
            break
        k, amount = divmod(amount, c)
        if k:
            res[c] = k
    return {} if amount != 0 else res

def find_min_coins(amount: int, coins=COINS) -> dict[int,int]:
    if amount < 0:
        return {}
    dp = [0] + [inf]*amount
    choice = [-1]*(amount+1)
    for c in coins:
        for a in range(c, amount+1):
            x = dp[a-c] + 1
            if x < dp[a]:
                dp[a] = x
                choice[a] = c
    if dp[amount] == inf:
        return {}
    res = {}
    a = amount
    while a > 0:
        c = choice[a]
        if c == -1:
            return {}
        res[c] = res.get(c, 0) + 1
        a -= c
    return dict(sorted(res.items()))

def demo():
    amount = 113
    g = find_coins_greedy(amount)
    d = find_min_coins(amount)
    sg = sum(k*v for k,v in g.items())
    sd = sum(k*v for k,v in d.items())
    print(f"Greedy для {amount}: {g} (сума={sg}, монет={sum(g.values())})")
    print(f"DP     для {amount}: {d} (сума={sd}, монет={sum(d.values())})")

def bench(amounts=(1_000, 10_000, 100_000, 200_000), repeat=3):
    rows = []
    for a in amounts:
        tg = 0.0
        td = 0.0
        for _ in range(repeat):
            t0 = perf_counter(); find_coins_greedy(a); tg += perf_counter()-t0
            t0 = perf_counter(); find_min_coins(a);   td += perf_counter()-t0
        tg /= repeat; td /= repeat
        rows.append((a, tg, td))
        print(f"amount={a:7d} | greedy: {tg:.6f}s | dp: {td:.6f}s")
    md = []
    md.append("# Порівняння жадібного алгоритму та ДП для розміну монет\n\n")
    md.append(f"Номінали: {COINS}\n\n")
    md.append("## Складність\n")
    md.append("- Greedy: ~O(K+M) при фіксованих номіналах ≈ O(1) по часу, O(1) памʼять\n")
    md.append("- DP: O(A·K) час, O(A) памʼять, де A — сума, K — кількість номіналів\n\n")
    md.append("## Результати бенчмарку\n\n")
    md.append("| amount | greedy (s) | dp (s) |\n|------:|-----------:|-------:|\n")
    for a,tg,td in rows:
        md.append(f"| {a} | {tg:.6f} | {td:.6f} |\n")
    md.append("\n## Висновки\n")
    md.append("- Для канонічного набору номіналів [50,25,10,5,2,1] greedy завжди дає оптимум і працює значно швидше при великих сумах.\n")
    md.append("- DP універсальний і потрібен для довільних наборів монет, де greedy може бути неоптимальним; але його час і памʼять зростають лінійно з сумою.\n")
    Path("readme.md").write_text("".join(md), encoding="utf-8")
    print("Звіт записано у readme.md")

if __name__ == "__main__":
    demo()
    bench()
