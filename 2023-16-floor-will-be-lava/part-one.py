def main():
    with open("2023-16-floor-will-be-lava/input.txt") as f:
        board = [l for line in f if (l := line.strip())]

    n, m = len(board), len(board[0])

    def valid(x, y):
        return 0 <= x < n and 0 <= y < m

    seen = set()
    curr, next_ = [(0, 0, +0, +1)], []
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

        # light = {(x, y) for x, y, _, _ in seen}
        # curr_board = [
        #     "".join("#" if (i, j) in light else board[i][j] for j in range(m))
        #     for i in range(n)
        # ]
        # print('\n'.join(curr_board), end="\n\n")

    print(len(set((x, y) for x, y, _, _ in seen)))


if __name__ == "__main__":
    main()
