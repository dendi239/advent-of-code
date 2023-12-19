def get_directions() -> set[tuple[int, int]]:
    return {(+1, +0), (-1, +0), (+0, -1), (+0, +1)}


def main() -> None:
    with open("17-clumsy-crucible/input.txt") as f:
        board = [list(map(int, l)) for line in f if (l := line.strip())]

    n, m = len(board), len(board[0])

    # state: (dist, (x, y, dx, dy, cnt))
    states_by_dist = [[] for _ in range(40 * n * m)]
    dist_by_state = {}
    prev_state = {}

    def add_state(dist, x, y, dx, dy, cnt, add_dest: bool = False, prev=None):
        if not (0 <= x < n and 0 <= y < m):
            return

        if add_dest:
            dist += board[x][y]

        if (s := (x, y, dx, dy, cnt)) in dist_by_state:
            if dist_by_state[s] <= dist:
                return
            states_by_dist[dist_by_state[s]].remove(s)

        dist_by_state[s] = dist
        states_by_dist[dist].append(s)
        prev_state[s] = prev

    add_state(0, 0, 0, dx=0, dy=1, cnt=0, add_dest=False)
    add_state(0, 0, 0, dx=1, dy=0, cnt=0, add_dest=False)
    for dist, states in enumerate(states_by_dist):
        for x, y, dx, dy, c in states:
            if (s := (x, y, dx, dy, c)) in dist_by_state and dist_by_state[s] < dist:
                continue

            moves = {(dx, dy)} if c < 4 else get_directions()
            moves -= {(-dx, -dy)}
            if c >= 10:
                moves -= {(dx, dy)}

            for ddx, ddy in moves:
                add_state(
                    dist,
                    x + ddx,
                    y + ddy,
                    ddx,
                    ddy,
                    c * (ddx == dx and ddy == dy) + 1,
                    add_dest=True,
                    prev=s,
                )

    final_state = min(
        (
            s
            for dx in (-1, 0, +1)
            for dy in (-1, 0, +1)
            for c in range(4, 20)
            if (s := (n - 1, m - 1, dx, dy, c)) in dist_by_state
        ),
        key=dist_by_state.__getitem__,
    )

    printed_board = [[str(board[i][j]) for j in range(m)] for i in range(n)]
    states = [final_state]
    while prev_state[states[-1]] is not None:
        states.append(prev_state[states[-1]])

    for state in states:
        print(state)

    for x, y, _, _, c in states:
        printed_board[x][y] = "X" if 4 <= c <= 10 else "."

    print("\n".join("".join(row) for row in printed_board))
    print(dist_by_state[final_state])


if __name__ == "__main__":
    main()
