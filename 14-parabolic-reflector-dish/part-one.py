import argparse
import logging


def load_row(row: str) -> int:
    pivvots = [0] + [i + 1 for i, c in enumerate(row) if c == '#'] + [len(row)]
    total = 0

    for start, end in zip(pivvots, pivvots[1:]):
        i_write = start
        for i in range(start, end):
            if row[i] == 'O':
                total += len(row) - i_write
                i_write += 1
                logging.debug(f"row: '{row}', writen: {i_write} for {i}")

    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    with open("14-parabolic-reflector-dish/input.txt") as f:
        board = [l for line in f if (l := line.strip())]

    board = [
        "".join(board[i][j] for i in range(len(board))) for j in range(len(board[0]))
    ]

    print(sum(load_row(row) for row in board))


if __name__ == "__main__":
    main()
