from dataclasses import dataclass


ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


@dataclass
class SelectionResult:
    items: list[str]
    total_cost: int
    total_calories: int


def greedy_algorithm(
    items: dict[str, dict[str, int]],
    budget: int,
) -> SelectionResult:
    """
    Вибирає страви за спаданням співвідношення калорій до вартості.
    """
    if budget < 0:
        raise ValueError("Бюджет не може бути від'ємним.")

    sorted_items = sorted(
        items.items(),
        key=lambda item: (
            item[1]["calories"] / item[1]["cost"],
            item[1]["calories"],
        ),
        reverse=True,
    )

    selected = []
    total_cost = 0
    total_calories = 0

    for name, properties in sorted_items:
        cost = properties["cost"]

        if total_cost + cost <= budget:
            selected.append(name)
            total_cost += cost
            total_calories += properties["calories"]

    return SelectionResult(
        items=selected,
        total_cost=total_cost,
        total_calories=total_calories,
    )


def dynamic_programming(
    items: dict[str, dict[str, int]],
    budget: int,
) -> SelectionResult:
    """
    Знаходить набір із максимальною калорійністю в межах бюджету.

    Реалізація задачі 0/1 knapsack.
    """
    if budget < 0:
        raise ValueError("Бюджет не може бути від'ємним.")

    names = list(items)
    count = len(names)

    dp = [
        [0] * (budget + 1)
        for _ in range(count + 1)
    ]

    for index in range(1, count + 1):
        name = names[index - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]

        for current_budget in range(budget + 1):
            dp[index][current_budget] = dp[index - 1][current_budget]

            if cost <= current_budget:
                with_item = (
                    dp[index - 1][current_budget - cost]
                    + calories
                )
                dp[index][current_budget] = max(
                    dp[index][current_budget],
                    with_item,
                )

    selected = []
    current_budget = budget

    for index in range(count, 0, -1):
        if dp[index][current_budget] != dp[index - 1][current_budget]:
            name = names[index - 1]
            selected.append(name)
            current_budget -= items[name]["cost"]

    selected.reverse()
    total_cost = sum(items[name]["cost"] for name in selected)

    return SelectionResult(
        items=selected,
        total_cost=total_cost,
        total_calories=dp[count][budget],
    )


def print_result(name: str, result: SelectionResult) -> None:
    print(name)
    print(f"  Страви: {result.items}")
    print(f"  Вартість: {result.total_cost}")
    print(f"  Калорійність: {result.total_calories}")


def main() -> None:
    budget = 100

    greedy_result = greedy_algorithm(ITEMS, budget)
    dp_result = dynamic_programming(ITEMS, budget)

    print(f"Бюджет: {budget}\n")
    print_result("Жадібний алгоритм:", greedy_result)
    print()
    print_result("Динамічне програмування:", dp_result)


if __name__ == "__main__":
    main()
