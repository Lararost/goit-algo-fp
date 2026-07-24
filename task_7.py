import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ANALYTICAL_COUNTS = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1,
}


def simulate_dice_rolls(
    rolls: int,
    seed: int = 42,
) -> dict[int, float]:
    """Імітує кидки двох кубиків методом Монте-Карло."""
    if rolls <= 0:
        raise ValueError("Кількість кидків має бути додатною.")

    rng = np.random.default_rng(seed)
    first_die = rng.integers(1, 7, size=rolls)
    second_die = rng.integers(1, 7, size=rolls)
    sums = first_die + second_die

    counts = Counter(sums.tolist())

    return {
        total: counts.get(total, 0) / rolls
        for total in range(2, 13)
    }


def analytical_probabilities() -> dict[int, float]:
    """Повертає точні ймовірності сум двох кубиків."""
    return {
        total: count / 36
        for total, count in ANALYTICAL_COUNTS.items()
    }


def print_table(
    monte_carlo: dict[int, float],
    analytical: dict[int, float],
) -> None:
    print(
        f"{'Сума':>6}"
        f"{'Monte Carlo':>16}"
        f"{'Аналітична':>16}"
        f"{'Різниця':>14}"
    )
    print("-" * 52)

    for total in range(2, 13):
        difference = abs(
            monte_carlo[total] - analytical[total]
        )

        print(
            f"{total:>6}"
            f"{monte_carlo[total] * 100:>15.3f}%"
            f"{analytical[total] * 100:>15.3f}%"
            f"{difference * 100:>13.3f}%"
        )


def create_chart(
    monte_carlo: dict[int, float],
    analytical: dict[int, float],
    output_path: Path,
) -> None:
    """Створює порівняльний графік ймовірностей."""
    sums = np.arange(2, 13)
    width = 0.38

    monte_values = [
        monte_carlo[total] * 100
        for total in sums
    ]
    analytical_values = [
        analytical[total] * 100
        for total in sums
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        sums - width / 2,
        monte_values,
        width,
        label="Monte Carlo",
    )
    ax.bar(
        sums + width / 2,
        analytical_values,
        width,
        label="Аналітичні значення",
    )

    ax.set_title("Ймовірності сум при киданні двох кубиків")
    ax.set_xlabel("Сума")
    ax.set_ylabel("Ймовірність, %")
    ax.set_xticks(sums)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Моделювання кидків двох кубиків методом Монте-Карло."
        )
    )
    parser.add_argument(
        "--rolls",
        type=int,
        default=1_000_000,
        help="Кількість кидків. За замовчуванням: 1 000 000.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed генератора випадкових чисел.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    monte_carlo = simulate_dice_rolls(
        rolls=args.rolls,
        seed=args.seed,
    )
    analytical = analytical_probabilities()

    print(f"Кількість кидків: {args.rolls}\n")
    print_table(monte_carlo, analytical)

    max_error = max(
        abs(monte_carlo[total] - analytical[total])
        for total in range(2, 13)
    )

    output_path = (
        Path(__file__).resolve().parent / "dice_probabilities.png"
    )
    create_chart(monte_carlo, analytical, output_path)

    print(
        "\nМаксимальна абсолютна різниця: "
        f"{max_error * 100:.4f}%"
    )
    print(f"Графік збережено у файлі: {output_path.name}")


if __name__ == "__main__":
    main()
