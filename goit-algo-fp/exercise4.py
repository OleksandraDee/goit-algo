import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
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
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, figsize=(8, 5), title=None):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=figsize)
    if title:
        plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.axis('off')
    plt.show()


# --------- НОВЕ: побудова дерева з купи (масиву) ---------
def build_tree_from_heap_array(arr, highlight_index=None):
    """
    Приймає масив-купу (list) і будує дерево з об'єктів Node.
    highlight_index — індекс елемента, який виділити іншим кольором (опційно).
    """
    if not arr:
        return None

    # створюємо вузли
    nodes = []
    for i, val in enumerate(arr):
        color = "tomato" if (highlight_index is not None and i == highlight_index) else "skyblue"
        nodes.append(Node(val, color=color))

    # з’єднуємо батьків з дітьми
    n = len(arr)
    for i in range(n):
        left_i = 2 * i + 1
        right_i = 2 * i + 2
        if left_i < n:
            nodes[i].left = nodes[left_i]
        if right_i < n:
            nodes[i].right = nodes[right_i]

    return nodes[0]  # корінь


def visualize_heap(values, heap_type="min", highlight_last=True, title=None):
    """
    values       — вихідні значення
    heap_type    — 'min' або 'max'
    highlight_last — виділити останній вставлений елемент
    """
    data = list(values)

    if heap_type == "min":
        heap = data[:]
        heapq.heapify(heap)          # стандартна мін-купа
        title = title or "Мін-купа"
        highlight_index = len(heap) - 1 if highlight_last and heap else None

    elif heap_type == "max":
        # перетворюємо у макс-купу через інверсію знаку
        heap = [-x for x in data]
        heapq.heapify(heap)
        heap = [-x for x in heap]
        title = title or "Макс-купа"
        highlight_index = len(heap) - 1 if highlight_last and heap else None

    else:
        raise ValueError("heap_type має бути 'min' або 'max'")

    root = build_tree_from_heap_array(heap, highlight_index=highlight_index)
    draw_tree(root, title=title)


# ------------------ приклади запуску ------------------
if __name__ == "__main__":
    values = [10, 4, 7, 15, 3, 20, 9, 1]

    # Візуалізація мін-купи
    visualize_heap(values, heap_type="min")

    # Візуалізація макс-купи
    visualize_heap(values, heap_type="max")
