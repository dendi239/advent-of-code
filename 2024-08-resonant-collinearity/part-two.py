from collections import defaultdict


def gcd(x, y):
    while x and y:
        x, y = y, x % y
    return x + y


with open("2024-08-resonant-collinearity/input.txt") as f:
    grid = [line.strip() for line in f if line.strip()]

n, m = len(grid), len(grid[0])

symbol_to_indices = defaultdict(list)
for i in range(m):
    for j in range(n):
        if grid[j][i] != ".":
            symbol_to_indices[grid[j][i]].append((j, i))


result = set()
for _, indices in symbol_to_indices.items():
    for i1, j1 in indices:
        for i2, j2 in indices:
            if i1 == i2 or j1 == j2:
                continue

            di, dj = i2 - i1, j2 - j1
            di, dj = di / gcd(di, dj), dj / gcd(di, dj)

            i, j = i2 + di, j2 + dj
            while 0 <= i < n and 0 <= j < m:
                result.add((i, j))
                i, j = i + i2 - i1, j + j2 - j1


print(len(result))
