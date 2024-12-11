from collections import defaultdict


with open("2024-10-hoof-it/input.txt") as f:
    grid = [line.strip() for line in f if line.strip()]

n, m = len(grid), len(grid[0])


def is_valid(i, j):
    return 0 <= i < n and 0 <= j < m


starts = {
    (i, j): {(i, j)}
    for i, row in enumerate(grid)
    for j, c in enumerate(row)
    if c == "9"
}

for digit in range(8, -1, -1):
    next_ = defaultdict(set)
    for (i, j), c in starts.items():
        for di, dj in ((0, -1), (-1, 0), (+1, 0), (0, +1)):
            i1, j1 = i + di, j + dj

            if not is_valid(i1, j1) or grid[i1][j1] != str(digit):
                continue

            next_[(i1, j1)] |= c

    starts = next_


print(sum(len(s) for s in starts.values()))
