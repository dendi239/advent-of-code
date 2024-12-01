import dataclasses
from typing import Optional


@dataclasses.dataclass
class Number:
    id_: int
    start: tuple[int, int]
    end: tuple[int, int]
    enabled = False


def product(xs):
    res = 1
    for x in xs:
        res *= x
    return res


def main() -> None:
    with open("2023-03-gear-ratios/input.txt") as f:
        board = [l for line in f if (l := line.strip())]

    cell_to_number: dict[tuple[int, int], Number] = {}

    for i, row in enumerate(board):
        number: Optional[Number] = None
        for j, cell in enumerate(row):
            if cell.isdigit():
                if number is None:
                    number = Number(id_=len(cell_to_number), start=(i, j), end=(i, j))
                number.end = (i, j + 1)
                cell_to_number[(i, j)] = number
            else:
                number = None

    total = 0
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.isdigit() or cell != "*":
                continue

            numbers = [
                cell_to_number[pos]
                for di in (-1, 0, +1)
                for dj in (-1, 0, +1)
                if (pos := (i + di, j + dj)) in cell_to_number
            ]

            uns = [
                number
                for prev, number in zip([None] + numbers, numbers)
                if prev is None or prev.id_ != number.id_
            ]

            if len(uns) == 2:
                total += product(
                    int(board[number.start[0]][number.start[1] : number.end[1]])
                    for number in uns
                )

    print(total)


if __name__ == "__main__":
    main()
