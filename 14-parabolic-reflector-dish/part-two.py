import argparse
import functools
import logging


NORTH = 3
WEST = 0
EAST = 2
SOUTH = 1


def load_row(row: str) -> int:
    return sum(i for i, c in zip(range(len(row), -1, -1), row) if c == 'O')


def tilt_row(row: str) -> str:
    pivvots = [0] + [i + 1 for i, c in enumerate(row) if c == "#"] + [len(row)]
    result = [c if c == "#" else "." for c in row]

    for start, end in zip(pivvots, pivvots[1:]):
        i_write = start
        for i in range(start, end):
            if row[i] == "O":
                result[i_write] = "O"
                i_write += 1

    return "".join(result)


def rotate(board: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        "".join(board[i][j] for i in range(len(board) - 1, -1, -1))
        for j in range(len(board[0]))
    )


def tilt(board: tuple[str, ...], direction: int) -> tuple[str, ...]:
    for _ in range(direction):
        board = rotate(board)
    board = tuple(tilt_row(row) for row in board)
    for _ in range(4 - direction):
        board = rotate(board)
    return board


def load(board: tuple[str, ...], direction: int) -> int:
    for _ in range(direction):
        board = rotate(board)
    return sum(load_row(row) for row in board)


@functools.lru_cache(maxsize=None)
def cycle(board: tuple[str, ...]) -> tuple[str, ...]:
    board = tilt(board, NORTH)
    board = tilt(board, WEST)
    board = tilt(board, SOUTH)
    board = tilt(board, EAST)
    return board


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    with open("14-parabolic-reflector-dish/input.txt") as f:
        board = tuple(l for line in f if (l := line.strip()))

    board_to_i = {board: 0}
    boards = [board]
    dest = 1000000000

    for i in range(1, 1000000000):
        board = cycle(board)

        if board in board_to_i:
            cycle_start = board_to_i[board]
            cycle_len = i - board_to_i[board]

            if dest > cycle_start:
                dest = cycle_start + (dest - cycle_start) % cycle_len
            break

        boards.append(board)
        board_to_i[board] = i

    print(load(boards[dest], NORTH))


if __name__ == "__main__":
    main()
