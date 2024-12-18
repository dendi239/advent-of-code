with open("2024-18-ram-run/input.txt") as f:
    memory_cells = [tuple(map(int, x.split(","))) for x in f]

n, m, fallen = 71, 71, 1024


cell_to_busted = {}
for i, (x, y) in enumerate(memory_cells):
    cell_to_busted[(x, y)] = i


def print_grid(d, path):
    print(
        "\n".join(
            "".join(
                "O"
                if (i, j) in path
                else "."
                if (i, j) not in cell_to_busted or cell_to_busted[(i, j)] > d
                else "#"
                for j in range(m)
            )
            for i in range(n)
        )
    )


cell_to_shortest = {(0, 0): 0}
prev = {}
queue = []


def recover_path(cell):
    path = []
    while cell in prev:
        path.append(cell)
        cell = prev[cell]
    path.append(cell)
    return list(reversed(path))


queue.append((0, 0, 0))
pd = -1
while True:
    (d, x, y) = queue.pop(0)

    if pd != d:
        pd = d

    if (x, y) in cell_to_shortest and cell_to_shortest[(x, y)] < d:
        continue

    if x == n - 1 and y == m - 1:
        print(d)
        break

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (
            x + dx >= n
            or y + dy >= m
            or x + dx < 0
            or y + dy < 0
            or (
                (x + dx, y + dy) in cell_to_busted
                and cell_to_busted[(x + dx, y + dy)] < fallen
            )
            or (
                (x + dx, y + dy) in cell_to_shortest
                and cell_to_shortest[(x + dx, y + dy)] <= d + 1
            )
        ):
            continue

        prev[(x + dx, y + dy)] = (x, y)
        cell_to_shortest[(x + dx, y + dy)] = d + 1
        queue.append((d + 1, x + dx, y + dy))
