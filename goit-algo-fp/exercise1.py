from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Callable, Any


# ---------- Базові структури ----------

@dataclass
class Node:
    value: Any
    next: Optional["Node"] = None


class SinglyLinkedList:
    def __init__(self, iterable: Optional[Iterable[Any]] = None):
        self.head: Optional[Node] = None
        if iterable:
            for x in iterable:
                self.append(x)

    # Утиліти
    def append(self, value: Any) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def extend(self, it: Iterable[Any]) -> None:
        for x in it:
            self.append(x)

    def to_list(self) -> list[Any]:
        res, cur = [], self.head
        while cur:
            res.append(cur.value)
            cur = cur.next
        return res

    def clear(self) -> None:
        self.head = None

    # 1) Реверсування
    def reverse(self) -> None:
        prev, cur = None, self.head
        while cur:
            nx = cur.next
            cur.next = prev
            prev = cur
            cur = nx
        self.head = prev

    # 2a) Сортування злиттям
    def sort_merge(self, key: Optional[Callable[[Any], Any]] = None) -> None:
        self.head = _merge_sort(self.head, key)

    # 2b) Сортування вставками
    def sort_insertion(self, key: Optional[Callable[[Any], Any]] = None) -> None:
        self.head = _insertion_sort(self.head, key)

    # 3) Злиття двох відсортованих
    def merge_sorted_with(self, other: "SinglyLinkedList",
                          key: Optional[Callable[[Any], Any]] = None) -> "SinglyLinkedList":
        out = SinglyLinkedList()
        out.head = _merge_two_sorted_lists(self.head, other.head, key)
        return out


# ---------- Допоміжні функції для сортувань/злиття ----------

def _split_middle(head: Optional[Node]) -> tuple[Optional[Node], Optional[Node]]:
    if head is None or head.next is None:
        return head, None
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    right = slow.next
    slow.next = None
    return head, right


def _merge_by_key(a: Optional[Node], b: Optional[Node],
                  key: Optional[Callable[[Any], Any]]) -> Optional[Node]:
    key_fn = key if key else (lambda x: x)
    dummy = Node(None)
    tail = dummy
    while a and b:
        if key_fn(a.value) <= key_fn(b.value):
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


def _merge_sort(head: Optional[Node],
                key: Optional[Callable[[Any], Any]] = None) -> Optional[Node]:
    if head is None or head.next is None:
        return head
    left, right = _split_middle(head)
    left = _merge_sort(left, key)
    right = _merge_sort(right, key)
    return _merge_by_key(left, right, key)


def _insertion_sort(head: Optional[Node],
                    key: Optional[Callable[[Any], Any]] = None) -> Optional[Node]:
    key_fn = key if key else (lambda x: x)
    dummy = Node(None)
    cur = head
    while cur:
        nxt = cur.next
        # вставляємо cur у відсортовану частину [dummy.next ...]
        prev, it = dummy, dummy.next
        while it and key_fn(it.value) <= key_fn(cur.value):
            prev, it = it, it.next
        cur.next = it
        prev.next = cur
        cur = nxt
    return dummy.next


def _merge_two_sorted_lists(a: Optional[Node], b: Optional[Node],
                            key: Optional[Callable[[Any], Any]] = None) -> Optional[Node]:
    return _merge_by_key(a, b, key)


# ---------- Інтерактивне меню ----------

def parse_values(line: str) -> list[int]:
    line = line.strip()
    if not line:
        return []
    parts = line.replace(",", " ").split()
    vals = []
    for p in parts:
        try:
            vals.append(int(p))
        except ValueError:
            raise ValueError(f"Не можу перетворити «{p}» на ціле число.")
    return vals


def print_list(name: str, sll: SinglyLinkedList) -> None:
    print(f"{name}: {sll.to_list()}")


def menu():
    print("Односесійне меню роботи з однозв’язним списком")
    print("Введіть початкові значення (через пробіл). Приклад: 7 3 5 2 9 1")
    while True:
        try:
            initial = parse_values(input("> "))
            break
        except ValueError as e:
            print(e)

    sll = SinglyLinkedList(initial)
    print_list("Поточний список", sll)

    while True:
        print("\nМеню:")
        print(" 1) Показати список")
        print(" 2) Реверсувати")
        print(" 3) Сортувати (злиттям)")
        print(" 4) Сортувати (вставками)")
        print(" 5) Злити з іншим ВІДСОРТОВАНИМ списком")
        print(" 6) Додати елементи в кінець")
        print(" 7) Очистити й ввести новий список")
        print(" 0) Вийти")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            print_list("Поточний список", sll)

        elif choice == "2":
            sll.reverse()
            print("Готово. Після reverse:")
            print_list("Список", sll)

        elif choice == "3":
            sll.sort_merge()
            print("Відсортовано злиттям:")
            print_list("Список", sll)

        elif choice == "4":
            sll.sort_insertion()
            print("Відсортовано вставками:")
            print_list("Список", sll)

        elif choice == "5":
            print("Введіть другий список (ВІН МАЄ БУТИ ВІДСОРТОВАНИЙ!):")
            try:
                vals = parse_values(input("> "))
            except ValueError as e:
                print(e)
                continue
            other = SinglyLinkedList(vals)
            merged = sll.merge_sorted_with(other)  # стабільне злиття
            print("Результат злиття:")
            print_list("Merged", merged)

        elif choice == "6":
            print("Введіть елементи для додавання (через пробіл):")
            try:
                vals = parse_values(input("> "))
            except ValueError as e:
                print(e)
                continue
            sll.extend(vals)
            print("Додано. Поточний стан:")
            print_list("Список", sll)

        elif choice == "7":
            print("Введіть нові значення списку:")
            try:
                vals = parse_values(input("> "))
            except ValueError as e:
                print(e)
                continue
            sll.clear()
            sll.extend(vals)
            print("Оновлено.")
            print_list("Список", sll)

        elif choice == "0":
            print("Бувай!")
            break
        else:
            print("Невірний пункт меню. Спробуйте ще раз.")


if __name__ == "__main__":
    menu()
