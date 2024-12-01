def find_sym_rows(board: list[str]) -> list[int]:
    return [
        i
        for i in range(1, len(board))
        if all(l == r for l, r in zip(board[i - 1 :: -1], board[i:]))
    ]


def transpose(board: list[str]) -> list[str]:
    n, m = len(board), len(board[0])
    return ["".join(board[i][j] for i in range(n)) for j in range(m)]


def main() -> None:
    boards = [[]]
    with open("2023-13-point-of-incidence/input.txt") as f:
        for line in f:
            l = line.strip()
            if not l:
                boards.append([])
            else:
                boards[-1].append(l)

    rows = sum((find_sym_rows(board) for board in boards), [])
    columns = sum((find_sym_rows(transpose(board)) for board in boards), [])

    print(100 * sum(rows) + sum(columns))


if __name__ == "__main__":
    main()
