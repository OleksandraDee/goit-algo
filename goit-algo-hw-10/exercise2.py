import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from time import perf_counter

try:
    import scipy.integrate as spi
except Exception:
    spi = None

def f(x):
    return x**2

def monte_carlo_integral(func, a, b, n, seed=None):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(a, b, size=n)
    vals = func(xs)
    mean = np.mean(vals)
    std = np.std(vals, ddof=1) if n > 1 else 0.0
    est = (b - a) * mean
    se = (b - a) * std / np.sqrt(n) if n > 1 else 0.0
    return est, se

def true_integral_fx2(a, b):
    return (b**3 - a**3) / 3.0

def quad_integral(func, a, b):
    if spi is None:
        return None, None
    val, err = spi.quad(func, a, b)
    return val, err

def plot_function(func, a, b):
    x = np.linspace(a - 0.5, b + 0.5, 400)
    y = func(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ix = np.linspace(a, b, 400)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)
    ax.axvline(x=a, color='gray', linestyle='--')
    ax.axvline(x=b, color='gray', linestyle='--')
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) * 1.05])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(f'Інтегрування f(x) від {a} до {b}')
    ax.grid(True)
    plt.show()

def main():
    a, b = 0.0, 2.0
    Ns = [1_000, 10_000, 100_000]
    true_val_quad, quad_err = quad_integral(f, a, b)
    true_val_analytic = true_integral_fx2(a, b)
    ref_val = true_val_quad if true_val_quad is not None else true_val_analytic
    rows = []
    for n in Ns:
        t0 = perf_counter()
        est, se = monte_carlo_integral(f, a, b, n, seed=12345)
        dt = perf_counter() - t0
        err = abs(est - ref_val)
        rows.append((n, est, se, err, dt))
        print(f"N={n:7d}  MC={est:.8f}  SE≈{se:.8f}  |err|={err:.8f}  time={dt:.4f}s")
    md = []
    md.append("# Інтегрування методом Монте-Карло\n\n")
    md.append(f"Функція: f(x)=x^2, інтервал: [{a}, {b}]\n\n")
    if true_val_quad is not None:
        md.append(f"Опорне значення (quad): {true_val_quad:.12f} (оцінка помилки {quad_err:.2e})\n\n")
    else:
        md.append(f"Опорне значення (аналітично): {true_val_analytic:.12f}\n\n")
    md.append("| N | Monte Carlo | StdErr | |error| vs reference | time (s) |\n|---:|------------:|-------:|---------------------:|---------:|\n")
    for n, est, se, err, dt in rows:
        md.append(f"| {n} | {est:.8f} | {se:.8f} | {err:.8f} | {dt:.4f} |\n")
    md.append("\n## Висновки\n")
    md.append("- Оцінка Монте-Карло збігається до істинного значення при зростанні N; похибка зменшується приблизно як O(1/√N).\n")
    if true_val_quad is not None:
        md.append("- Порівняння з SciPy quad показує близьку відповідність отриманих значень у межах статистичної похибки.\n")
    else:
        md.append("- Порівняння з аналітичним значенням показує близьку відповідність у межах статистичної похибки.\n")
    md.append("- Метод Монте-Карло простий і масштабований, але для високої точності потребує великих N; детерміничні методи на гладких функціях (quad) дають точніші результати значно швидше.\n")
    Path("readme.md").write_text("".join(md), encoding="utf-8")
    print("Звіт записано у readme.md")
    plot_function(f, a, b)

if __name__ == "__main__":
    main()
