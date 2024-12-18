with open("2024-18-ram-run/input.txt") as f:
    memory_cells = [tuple(map(int, x.split(","))) for x in f]

n, m = 71, 71


cell_to_busted = {}
for i, (x, y) in enumerate(memory_cells):
    cell_to_busted[(x, y)] = i


def is_broken(fallen):
    cell_to_shortest: dict[tuple[int, int], int] = {(0, 0): 0}
    queue: list[tuple[int, int, int]] = [(0, 0, 0)]

    while queue:
        d, x, y = queue.pop(0)

        if (x, y) in cell_to_shortest and cell_to_shortest[(x, y)] < d:
            continue

        if x == n - 1 and y == m - 1:
            return False

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

            cell_to_shortest[(x + dx, y + dy)] = d + 1
            queue.append((d + 1, x + dx, y + dy))

    return True


l, r = 0, len(memory_cells)
while r - l > 1:
    M = (l + r) // 2
    if is_broken(M):
        r = M
    else:
        l = M

print(*memory_cells[l], sep=",")
