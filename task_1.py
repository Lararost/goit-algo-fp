from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class Node:
    """Вузол однозв'язного списку."""

    data: int
    next: Node | None = None


class LinkedList:
    """Однозв'язний список із базовими операціями."""

    def __init__(self, values: Iterable[int] | None = None) -> None:
        self.head: Node | None = None

        if values is not None:
            for value in values:
                self.insert_at_end(value)

    def insert_at_beginning(self, data: int) -> None:
        """Додає новий вузол на початок списку."""
        self.head = Node(data, self.head)

    def insert_at_end(self, data: int) -> None:
        """Додає новий вузол у кінець списку."""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def reverse(self) -> None:
        """Реверсує список, змінюючи посилання між вузлами."""
        previous: Node | None = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def insertion_sort(self) -> None:
        """Сортує список вставками, перевстановлюючи посилання вузлів."""
        sorted_head: Node | None = None
        current = self.head

        while current is not None:
            next_node = current.next

            if sorted_head is None or current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                search = sorted_head

                while (
                    search.next is not None
                    and search.next.data <= current.data
                ):
                    search = search.next

                current.next = search.next
                search.next = current

            current = next_node

        self.head = sorted_head

    def __iter__(self) -> Iterator[int]:
        current = self.head

        while current is not None:
            yield current.data
            current = current.next

    def to_list(self) -> list[int]:
        return list(self)

    def __str__(self) -> str:
        return " -> ".join(map(str, self)) or "Порожній список"


def merge_sorted_lists(
    first: LinkedList,
    second: LinkedList,
) -> LinkedList:
    """
    Об'єднує два відсортовані однозв'язні списки.

    Вузли перевстановлюються без створення копій елементів.
    """
    dummy = Node(0)
    tail = dummy
    left = first.head
    right = second.head

    while left is not None and right is not None:
        if left.data <= right.data:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next

        tail = tail.next

    tail.next = left if left is not None else right

    result = LinkedList()
    result.head = dummy.next

    # Після злиття вузли належать новому списку.
    first.head = None
    second.head = None

    return result


def main() -> None:
    linked_list = LinkedList([4, 2, 1, 3, 5])

    print("Початковий список:")
    print(linked_list)

    linked_list.reverse()
    print("\nПісля реверсування:")
    print(linked_list)

    linked_list.insertion_sort()
    print("\nПісля сортування вставками:")
    print(linked_list)

    first = LinkedList([1, 3, 5, 7])
    second = LinkedList([2, 4, 6, 8])

    merged = merge_sorted_lists(first, second)
    print("\nОб'єднаний відсортований список:")
    print(merged)


if __name__ == "__main__":
    main()
