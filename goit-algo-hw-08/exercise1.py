import re

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert_bst(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert_bst(root.left, key)
    elif key > root.key:
        root.right = insert_bst(root.right, key)
    return root

def min_value(root):
    if root is None:
        return None
    cur = root
    while cur.left is not None:
        cur = cur.left
    return cur.key

def build_bst(values):
    root = None
    for v in values:
        root = insert_bst(root, v)
    return root

def parse_numbers(s):
    if not s.strip():
        return []
    parts = re.split(r"[,\s]+", s.strip())
    return [int(p) for p in parts if p]

if __name__ == "__main__":
    demo = [5, 3, 7, 2, 4, 6, 8]
    print(f"Для values = {demo} відповідь {min_value(build_bst(demo))}")
    while True:
        try:
            raw = input("Введіть список цілих чисел через пробіл або кому (Enter — вихід): ").strip()
            if raw == "":
                print("Готово.")
                break
            nums = parse_numbers(raw)
            if not nums:
                print("Порожній список. Спробуйте ще раз.")
                continue
            ans = min_value(build_bst(nums))
            print(f"Для values = {nums} відповідь {ans}")
        except ValueError:
            print("Є нечислові значення. Спробуйте ще раз.")
