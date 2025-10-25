#!/usr/bin/env python3
import sys
from typing import List

def mk(fl: int) -> str:
    "Создаёт текст ёлки"
    if fl < 1:
        raise ValueError("У нашей елки должен быть хотя бы один этаж, иначе это пень, а нам нужна елка.")

    lines: List[str] = []

    max = 2 * fl - 1  # ряды с листьями
    max_st = 4 * max - 3
    max_width = len(" ".join(["*"] * max_st)) + 1

    # Центрируем верх
    lines.append("W".center(max_width))

    # Листья
    for k in range(1, max + 1):
        lists_count = 4 * k - 3
        lists = " ".join(["*"] * lists_count)

        if k == 1:
            row = lists
        elif k % 2 == 0:
            row = "@" + lists
        else:
            row = lists + "@"

        lines.append(row.center(max_width))

    # основа
    osn = "TTTTT"
    lines.append(osn.center(max_width))
    lines.append(osn.center(max_width))

    return "\n".join(lines) + "\n"


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        print("Чтобы нарисовать елку впишите кол-во этажей и имя конечного файла: python tree.py <кол-во этажей> <конечный файл>", file=sys.stderr)
        sys.exit(2)

    try:
        floors = int(argv[0])
    except ValueError:
        print("Ошибка: Кол-во этажей должно быть целым числом", file=sys.stderr)
        sys.exit(2)

    output_path = argv[1]
    tree_text = mk(floors)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tree_text)

    print(f"Ёлка с {floors} этажами записана в {output_path}")


if __name__ == "__main__":
    main()
