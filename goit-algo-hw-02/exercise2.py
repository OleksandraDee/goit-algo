"""
Перевірка, чи є рядок паліндромом.
Використано deque з модуля collections. Функція не чутлива до регістру,
ігнорує пробіли та небуквенно-цифрові символи. Коректно працює з парною та
непарною кількістю символів.
"""

from collections import deque

def is_palindrome(s: str) -> bool:
    # Залишаємо лише буквено-цифрові символи та приводимо до нижнього регістру
    filtered = (ch.lower() for ch in s if ch.isalnum())
    d = deque(filtered)

    # Порівнюємо символи з обох кінців
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


if __name__ == "__main__":
    tests = [
        "А роза упала на лапу Азора",
        "Madam, I'm Adam",
        "No lemon, no melon!",
        "Step on no pets",
        "palindrome",
        "12321",
        "Was it a car or a cat I saw?",
    ]
    for t in tests:
        print(f"{t!r} -> {is_palindrome(t)}")
