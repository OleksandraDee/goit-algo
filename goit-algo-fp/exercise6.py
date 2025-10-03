items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


# Жадібний алгоритм
def greedy_algorithm(items, budget):
    # сортуємо за калорійністю на 1 одиницю вартості
    sorted_items = sorted(items.items(), key=lambda x: x[1]["calories"] / x[1]["cost"], reverse=True)

    total_calories = 0
    chosen_items = []
    for item, data in sorted_items:
        if budget >= data["cost"]:
            budget -= data["cost"]
            total_calories += data["calories"]
            chosen_items.append(item)

    return chosen_items, total_calories


# Динамічне програмування (Knapsack)
def dynamic_programming(items, budget):
    names = list(items.keys())
    n = len(names)

    # DP-таблиця: dp[i][b] = макс. калорій при використанні перших i страв з бюджетом b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for b in range(budget + 1):
            if cost <= b:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - cost] + calories)
            else:
                dp[i][b] = dp[i - 1][b]

    # Відновлюємо вибрані страви
    chosen_items = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen_items.append(name)
            b -= items[name]["cost"]

    return chosen_items, dp[n][budget]


# 🔹 Тест
budget = 100
print("Greedy:", greedy_algorithm(items, budget))
print("Dynamic Programming:", dynamic_programming(items, budget))
