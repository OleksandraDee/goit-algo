import random
import matplotlib.pyplot as plt
import pandas as pd

def monte_carlo_dice(n_trials=1000000):
    # Лічильник сум
    sums = {i: 0 for i in range(2, 13)}
    for _ in range(n_trials):
        roll = random.randint(1, 6) + random.randint(1, 6)
        sums[roll] += 1

    # Ймовірності
    probabilities = {s: (count / n_trials) for s, count in sums.items()}
    return probabilities

def main():
    # Симуляція
    trials = 200000
    probs = monte_carlo_dice(trials)

    # Аналітичні результати
    analytical = {
        2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
        7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
    }

    # Таблиця
    df = pd.DataFrame({
        "Сума": list(probs.keys()),
        "Monte Carlo (%)": [round(probs[s]*100, 2) for s in probs],
        "Аналітична (%)": [round(analytical[s]*100, 2) for s in analytical]
    })

    print(df)

    # Графік
    plt.bar(df["Сума"], df["Monte Carlo (%)"], alpha=0.6, label="Monte Carlo")
    plt.plot(df["Сума"], df["Аналітична (%)"], color="red", marker="o", label="Аналітична")
    plt.xlabel("Сума на кубиках")
    plt.ylabel("Ймовірність (%)")
    plt.title("Ймовірність сум при киданні двох кубиків (Метод Монте-Карло)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
