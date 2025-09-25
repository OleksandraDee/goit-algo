import re, heapq

def parse_numbers(s):
    if not s.strip():
        return []
    return [int(x) for x in re.split(r"[,\s]+", s.strip()) if x]

def min_merge_cost(lengths):
    if not lengths:
        return 0, []
    h = list(lengths)
    heapq.heapify(h)
    total = 0
    steps = []
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        c = a + b
        total += c
        steps.append((a, b, c))
        heapq.heappush(h, c)
    return total, steps

if __name__ == "__main__":
    demo = [8, 4, 6, 12]
    t, st = min_merge_cost(demo)
    print(f"Для довжин = {demo} мінімальна вартість {t}")
    for a, b, c in st:
        print(f"Об’єднати {a}+{b}={c}")
    while True:
        try:
            raw = input("Введіть довжини кабелів через пробіл або кому (Enter — вихід): ").strip()
            if raw == "":
                print("Готово.")
                break
            nums = parse_numbers(raw)
            if not nums:
                print("Порожній список. Спробуйте ще раз.")
                continue
            t, st = min_merge_cost(nums)
            print(f"Для довжин = {nums} мінімальна вартість {t}")
            print("Кроки:")
            for a, b, c in st:
                print(f"{a}+{b}={c}")
        except ValueError:
            print("Є нечислові значення. Спробуйте ще раз.")
