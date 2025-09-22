"""
Система обробки заявок сервіс-центру.
Використано Queue з модуля queue. Програма автоматично генерує нові заявки,
додає їх у чергу, а потім послідовно видаляє/обробляє.
Структура коду відповідає наданому псевдокоду з ДЗ.
"""

from queue import Queue
from dataclasses import dataclass
from typing import Optional
import random
import time
import uuid


@dataclass
class Request:
    """Модель заявки з унікальним ідентифікатором та корисними даними."""
    id: str
    payload: str


class ServiceCenter:
    def __init__(self) -> None:
        self.queue: Queue[Request] = Queue()

    # Функція generate_request(): створити нову заявку і додати до черги
    def generate_request(self, payload: Optional[str] = None) -> Request:
        req = Request(id=str(uuid.uuid4())[:8], payload=payload or "general")
        self.queue.put(req)
        print(f"[NEW]  Заявка {req.id:>8} (тип: {req.payload}) додана до черги. Розмір черги: {self.queue.qsize()}")
        return req

    # Функція process_request(): якщо черга не пуста — видалити заявку і обробити
    def process_request(self) -> None:
        if self.queue.empty():
            print("[INFO] Черга порожня — немає заявок для обробки.")
            return
        req = self.queue.get()
        print(f"[PROC] Обробляю заявку {req.id:>8} (тип: {req.payload}) ... завершено.")
        # сигналізувати про завершення (для сумісності з Queue.task_done, якщо треба)
        # self.queue.task_done()

    def run_demo(self, steps: int = 20, p_add: float = 0.6, min_sleep: float = 0.0, max_sleep: float = 0.0) -> None:
        """
        Демонстраційний цикл (скінченний), що імітує потік подій:
        - з імовірністю p_add додає нову заявку,
        - інакше обробляє одну з черги (якщо є).
        Для швидкої перевірки затримки за замовчуванням вимкнені.
        """
        for i in range(1, steps + 1):
            action = "add" if random.random() < p_add else "proc"
            if action == "add":
                self.generate_request(payload=random.choice(["general", "repair", "consultation", "refund"]))
            else:
                self.process_request()

            # опційна пауза (за потреби можна вмикати)
            if max_sleep > 0:
                time.sleep(random.uniform(min_sleep, max_sleep))


if __name__ == "__main__":
    sc = ServiceCenter()
    sc.run_demo(steps=25, p_add=0.65)
    # Після демо дочистимо чергу, щоб показати послідовну обробку всіх заявок
    while not sc.queue.empty():
        sc.process_request()
