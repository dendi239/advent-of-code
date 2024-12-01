def light_board(start: tuple[int, int, int, int], board: list[str]) -> None:
    n, m = len(board), len(board[0])

    def valid(x, y):
        return 0 <= x < n and 0 <= y < m

    seen = set()
    curr, next_ = [start], []
    while curr:
        new = False
        for state in curr:
            x, y, dx, dy = state
            if not valid(x, y):
                continue

            if state not in seen:
                seen.add(state)
                new = True
            else:
                continue

            if board[x][y] == "-":
                for dy in (-1, +1):
                    next_.append((x, y + dy, 0, dy))
            elif board[x][y] == "|":
                for dx in (-1, +1):
                    next_.append((x + dx, y, dx, 0))
            elif board[x][y] == "/":
                next_.append((x - dy, y - dx, -dy, -dx))
            elif board[x][y] == "\\":
                next_.append((x + dy, y + dx, +dy, +dx))
            else:
                next_.append((x + dx, y + dy, dx, dy))

        if not new:
            break
        curr, next_ = next_, []

    return len(set((x, y) for x, y, _, _ in seen))


def main():
    with open("2023-16-floor-will-be-lava/input.txt") as f:
        board = [l for line in f if (l := line.strip())]

    n, m = len(board), len(board[0])
    print(
        max(
            light_board((x + i * ddx, y + i * ddy, dx, dy), board)
            for x, y, dx, dy, ddx, ddy, l in [
                (0, 0, +0, +1, +1, +0, n),
                (0, 0, +1, +0, +0, +1, m),
                (0, m - 1, +0, -1, +1, +0, n),
                (n - 1, 0, -1, +0, +0, +1, m),
            ]
            for i in range(l)
        )
    )


if __name__ == "__main__":
    main()
