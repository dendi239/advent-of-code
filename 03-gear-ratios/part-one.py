import dataclasses
from typing import Optional


@dataclasses.dataclass
class Number:
    start: tuple[int, int]
    end: tuple[int, int]
    enabled = False


def main() -> None:
    with open("03-gear-ratios/input.txt") as f:
        board = [l for line in f if (l := line.strip())]

    cell_to_number: dict[tuple[int, int], Number] = {}

    for i, row in enumerate(board):
        number: Optional[Number] = None
        for j, cell in enumerate(row):
            if cell.isdigit():
                if number is None:
                    number = Number(start=(i, j), end=(i, j))
                number.end = (i, j + 1)
                cell_to_number[(i, j)] = number
            else:
                number = None

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.isdigit() or cell == ".":
                continue
            for di in (-1, 0, +1):
                for dj in (-1, 0, +1):
                    pos = (i + di, j + dj)
                    if pos in cell_to_number:
                        cell_to_number[pos].enabled = True

    print(
        sum(
            int(board[number.start[0]][number.start[1] : number.end[1]])
            for cell, number in cell_to_number.items()
            if number.start == cell and number.enabled
        )
    )


if __name__ == "__main__":
    main()
