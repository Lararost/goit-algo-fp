import argparse
import heapq
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def build_heap(values: list[int]) -> list[int]:
    """Перетворює список на мінімальну бінарну купу."""
    heap = values.copy()
    heapq.heapify(heap)
    return heap


def calculate_positions(
    size: int,
) -> dict[int, tuple[float, float]]:
    """Обчислює координати вузлів бінарної купи."""
    positions: dict[int, tuple[float, float]] = {}

    def place(index: int, x: float, y: float, offset: float) -> None:
        if index >= size:
            return

        positions[index] = (x, y)
        place(2 * index + 1, x - offset, y - 1, offset / 2)
        place(2 * index + 2, x + offset, y - 1, offset / 2)

    place(0, 0, 0, 4)
    return positions


def draw_heap(
    heap: list[int],
    output_path: Path,
    show: bool = True,
) -> None:
    """Візуалізує бінарну купу у вигляді дерева."""
    graph = nx.DiGraph()

    for index, value in enumerate(heap):
        graph.add_node(index, label=str(value))

        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(heap):
            graph.add_edge(index, left)

        if right < len(heap):
            graph.add_edge(index, right)

    positions = calculate_positions(len(heap))
    labels = nx.get_node_attributes(graph, "label")

    fig, ax = plt.subplots(figsize=(10, 6))

    nx.draw(
        graph,
        pos=positions,
        labels=labels,
        arrows=False,
        node_size=2200,
        font_size=11,
        ax=ax,
    )

    ax.set_title("Візуалізація мінімальної бінарної купи")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")

    if show:
        plt.show()

    plt.close(fig)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Побудова й візуалізація мінімальної бінарної купи."
    )
    parser.add_argument(
        "values",
        nargs="*",
        type=int,
        default=[9, 4, 7, 1, 3, 6, 2, 8, 5],
        help="Числа для побудови купи.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Не відкривати графічне вікно.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    values = args.values or [9, 4, 7, 1, 3, 6, 2, 8, 5]
    heap = build_heap(values)

    output_path = (
        Path(__file__).resolve().parent / "binary_heap.png"
    )

    draw_heap(
        heap=heap,
        output_path=output_path,
        show=not args.no_show,
    )

    print(f"Початкові дані: {values}")
    print(f"Мінімальна купа: {heap}")
    print(f"Зображення збережено у файлі: {output_path.name}")


if __name__ == "__main__":
    main()
