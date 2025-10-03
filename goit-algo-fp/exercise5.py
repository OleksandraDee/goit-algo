"""
Як це працює:

Використовується той самий клас Node, що й у завданні 4.

Для обходу в DFS використовується стек (list.append, pop).

Для обходу в BFS використовується черга (collections.deque).

Після кожного відвідування вузол перефарбовується, і викликається функція візуалізації.

Кольори плавно змінюються (градієнт).
"""

import networkx as nx
import matplotlib.pyplot as plt
import uuid
from collections import deque


class Node:
    def __init__(self, key, color="#000000"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2000, node_color=colors)
    plt.show()


# Генерація кольору залежно від кроку
def get_color(step, total):
    intensity = int(255 * step / total)
    return f"#{intensity:02x}{(100+step*5)%255:02x}{(200-step*3)%255:02x}"


# DFS (ітеративно, стек)
def dfs(root):
    stack = [root]
    visited = []
    step = 0
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            node.color = get_color(step, 10)
            step += 1
            draw_tree(root)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)


# BFS (ітеративно, черга)
def bfs(root):
    queue = deque([root])
    visited = []
    step = 0
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            node.color = get_color(step, 10)
            step += 1
            draw_tree(root)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


# Приклад дерева
root = Node(0)
root.left = Node(4)
root.right = Node(1)
root.left.left = Node(5)
root.left.right = Node(10)
root.right.left = Node(3)

print("DFS:")
dfs(root)

# скидаємо кольори перед BFS
for node in [root, root.left, root.right, root.left.left, root.left.right, root.right.left]:
    node.color = "#000000"

print("BFS:")
bfs(root)
