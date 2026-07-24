import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt


def draw_branch(
    ax,
    x: float,
    y: float,
    length: float,
    angle_degrees: float,
    level: int,
) -> None:
    """Рекурсивно малює гілки фрактала «дерево Піфагора»."""
    if level == 0:
        return

    angle = math.radians(angle_degrees)
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)

    ax.plot([x, end_x], [y, end_y], linewidth=max(0.5, level / 2))

    next_length = length * math.sqrt(2) / 2

    draw_branch(
        ax,
        end_x,
        end_y,
        next_length,
        angle_degrees + 45,
        level - 1,
    )
    draw_branch(
        ax,
        end_x,
        end_y,
        next_length,
        angle_degrees - 45,
        level - 1,
    )


def create_pythagoras_tree(
    level: int,
    output_path: Path,
    show: bool = True,
) -> None:
    """Створює та зберігає зображення фрактала."""
    if level < 0:
        raise ValueError("Рівень рекурсії не може бути від'ємним.")

    fig, ax = plt.subplots(figsize=(8, 8))

    draw_branch(
        ax=ax,
        x=0,
        y=-1.8,
        length=1.7,
        angle_degrees=90,
        level=level,
    )

    ax.set_title(f"Фрактал «дерево Піфагора», рівень {level}")
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")

    if show:
        plt.show()

    plt.close(fig)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Візуалізація фрактала «дерево Піфагора»."
    )
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        help="Рівень рекурсії.",
    )
    parser.add_argument(
        "--output",
        default="pythagoras_tree.png",
        help="Назва файлу з результатом.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Не відкривати графічне вікно.",
    )
    return parser.parse_args()


def read_level() -> int:
    while True:
        try:
            level = int(input("Введіть рівень рекурсії: "))

            if level < 0:
                print("Введіть невід'ємне число.")
                continue

            return level
        except ValueError:
            print("Потрібно ввести ціле число.")


def main() -> None:
    args = parse_arguments()
    level = args.level if args.level is not None else read_level()

    output_path = Path(__file__).resolve().parent / args.output

    create_pythagoras_tree(
        level=level,
        output_path=output_path,
        show=not args.no_show,
    )

    print(f"Зображення збережено у файлі: {output_path.name}")


if __name__ == "__main__":
    main()
