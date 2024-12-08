from collections import defaultdict


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

            i, j = i1 + 2 * (i2 - i1), j1 + 2 * (j2 - j1)

            if 0 <= i < n and 0 <= j < m:
                result.add((i, j))


print(len(result))
