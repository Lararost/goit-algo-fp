from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Node:
    """Вузол бінарного дерева."""

    value: int
    left: Node | None = None
    right: Node | None = None
    identifier: str = field(default_factory=lambda: str(uuid4()))


def create_tree() -> Node:
    """Створює демонстраційне бінарне дерево."""
    root = Node(0)
    root.left = Node(4)
    root.right = Node(1)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right.left = Node(3)
    root.right.right = Node(2)
    return root


def dfs_iterative(root: Node | None) -> list[Node]:
    """Обхід дерева в глибину за допомогою стека."""
    if root is None:
        return []

    order: list[Node] = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        # Правий вузол додається першим, щоб лівий обробився раніше.
        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return order


def bfs_iterative(root: Node | None) -> list[Node]:
    """Обхід дерева в ширину за допомогою черги."""
    if root is None:
        return []

    order: list[Node] = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        order.append(node)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return order


def build_graph(
    root: Node,
) -> tuple[nx.DiGraph, dict[str, tuple[float, float]]]:
    """Перетворює дерево на граф і обчислює позиції вузлів."""
    graph = nx.DiGraph()
    positions: dict[str, tuple[float, float]] = {}

    stack: list[tuple[Node, float, float, float]] = [
        (root, 0.0, 0.0, 4.0)
    ]

    while stack:
        node, x, y, offset = stack.pop()

        graph.add_node(
            node.identifier,
            label=str(node.value),
        )
        positions[node.identifier] = (x, y)

        if node.right is not None:
            graph.add_edge(node.identifier, node.right.identifier)
            stack.append(
                (node.right, x + offset, y - 1, offset / 2)
            )

        if node.left is not None:
            graph.add_edge(node.identifier, node.left.identifier)
            stack.append(
                (node.left, x - offset, y - 1, offset / 2)
            )

    return graph, positions


def draw_traversal(
    root: Node,
    order: list[Node],
    title: str,
    output_path: Path,
) -> None:
    """
    Візуалізує порядок обходу.

    Ранні вузли мають темніший відтінок, пізні — світліший.
    """
    graph, positions = build_graph(root)
    labels = nx.get_node_attributes(graph, "label")

    order_index = {
        node.identifier: index for index, node in enumerate(order)
    }

    color_values = [
        1 - order_index[node_id] / max(1, len(order) - 1)
        for node_id in graph.nodes
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    nx.draw(
        graph,
        pos=positions,
        labels=labels,
        arrows=False,
        node_size=2200,
        font_size=11,
        node_color=color_values,
        cmap=plt.cm.Blues,
        vmin=0,
        vmax=1,
        ax=ax,
    )

    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    root = create_tree()

    dfs_order = dfs_iterative(root)
    bfs_order = bfs_iterative(root)

    project_directory = Path(__file__).resolve().parent

    draw_traversal(
        root,
        dfs_order,
        "Обхід бінарного дерева в глибину (DFS)",
        project_directory / "dfs_traversal.png",
    )
    draw_traversal(
        root,
        bfs_order,
        "Обхід бінарного дерева в ширину (BFS)",
        project_directory / "bfs_traversal.png",
    )

    print("DFS:", [node.value for node in dfs_order])
    print("BFS:", [node.value for node in bfs_order])
    print("Створено файли dfs_traversal.png і bfs_traversal.png")


if __name__ == "__main__":
    main()
