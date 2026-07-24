from __future__ import annotations

import heapq
from math import inf


Graph = dict[str, list[tuple[str, float]]]


def dijkstra(
    graph: Graph,
    start: str,
) -> tuple[dict[str, float], dict[str, str | None]]:
    """
    Знаходить найкоротші відстані від початкової вершини.

    Для вибору вершини з найменшою поточною відстанню
    використовується бінарна купа heapq.
    """
    if start not in graph:
        raise KeyError(f"Вершини '{start}' немає у графі.")

    distances = {vertex: inf for vertex in graph}
    previous: dict[str, str | None] = {
        vertex: None for vertex in graph
    }

    distances[start] = 0
    priority_queue: list[tuple[float, str]] = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            if weight < 0:
                raise ValueError(
                    "Алгоритм Дейкстри не підтримує від'ємні ваги."
                )

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(
                    priority_queue,
                    (distance, neighbor),
                )

    return distances, previous


def restore_path(
    previous: dict[str, str | None],
    start: str,
    target: str,
) -> list[str]:
    """Відновлює найкоротший шлях від start до target."""
    path = []
    current: str | None = target

    while current is not None:
        path.append(current)

        if current == start:
            return list(reversed(path))

        current = previous[current]

    return []


def create_graph() -> Graph:
    """Створює приклад зваженого неорієнтованого графа."""
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    graph: Graph = {
        vertex: [] for vertex in "ABCDEF"
    }

    for first, second, weight in edges:
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    return graph


def main() -> None:
    graph = create_graph()
    start = "A"

    distances, previous = dijkstra(graph, start)

    print(f"Найкоротші шляхи від вершини {start}:\n")

    for vertex in sorted(graph):
        path = restore_path(previous, start, vertex)
        path_text = " -> ".join(path) if path else "шлях відсутній"

        print(
            f"{vertex}: відстань = {distances[vertex]}, "
            f"шлях = {path_text}"
        )


if __name__ == "__main__":
    main()
