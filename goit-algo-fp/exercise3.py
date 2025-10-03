# dijkstra_heap.py
# Алгоритм Дейкстри з використанням бінарної купи (heapq)

from __future__ import annotations
from typing import Dict, List, Tuple, Any, Optional
import math
import heapq


class Graph:
    """Зважений орієнтований/неорієнтований граф на основі списку суміжності."""
    def __init__(self) -> None:
        self.adj: Dict[Any, List[Tuple[Any, float]]] = {}

    def add_edge(self, u: Any, v: Any, w: float, undirected: bool = True) -> None:
        """Додає ребро u -> v з вагою w. Якщо undirected=True — також v -> u."""
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])  # гарантуємо наявність вершини v у словнику
        if undirected:
            self.adj[v].append((u, w))

    def vertices(self):
        return self.adj.keys()

    def __repr__(self) -> str:
        lines = []
        for u, nbrs in self.adj.items():
            lines.append(f"{u}: {nbrs}")
        return "\n".join(lines)


def dijkstra_heap(
    g: Graph, source: Any
) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """
    Алгоритм Дейкстри з використанням бінарної купи (heapq).
    Повертає:
      - dist[v]: найкоротша відстань від source до v
      - parent[v]: попередник v у найкоротшому шляху (для відновлення маршруту)
    """

    # 1) ініціалізація
    dist = {v: math.inf for v in g.vertices()}
    parent: Dict[Any, Optional[Any]] = {v: None for v in g.vertices()}
    dist[source] = 0.0

    # бінарна купа (піраміда) для вибору вершини з найменшою поточною дистанцією
    # зберігаємо пари (поточна_відстань, вершина)
    heap: List[Tuple[float, Any]] = [(0.0, source)]

    # 2) ітерації
    while heap:
        d_u, u = heapq.heappop(heap)

        # "ледача" обробка старих записів у купі:
        # якщо це не найкраще відоме значення — пропускаємо
        if d_u != dist[u]:
            continue

        # релаксуємо всі ребра з u
        for v, w in g.adj[u]:
            cand = dist[u] + w
            if cand < dist[v]:
                dist[v] = cand
                parent[v] = u
                heapq.heappush(heap, (cand, v))

    return dist, parent


def reconstruct_path(parent: Dict[Any, Optional[Any]], target: Any) -> List[Any]:
    """Відновлює шлях до target за масивом parent."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


# -------------------------
# Демонстрація роботи модуля
# -------------------------
if __name__ == "__main__":
    # Створимо невеликий граф
    g = Graph()
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "Z", 6),
        ("E", "Z", 3),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w, undirected=True)

    source = "A"
    dist, parent = dijkstra_heap(g, source)

    print("Найкоротші відстані від вершини", source)
    for v in sorted(g.vertices()):
        print(f"  {v}: {dist[v]:.2f}")

    print("\nШляхи від джерела:")
    for v in sorted(g.vertices()):
        p = reconstruct_path(parent, v)
        # Якщо вершина недосяжна, dist[v] == inf і шлях буде просто [v] з None-попередниками
        if math.isinf(dist[v]):
            print(f"  {v}: недосяжно")
        else:
            pretty = " -> ".join(p)
            print(f"  {v}: {pretty}  (вартість {dist[v]:.2f})")
