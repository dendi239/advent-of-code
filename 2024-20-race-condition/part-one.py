from collections import defaultdict


with open("2024-20-race-condition/input.txt", "r") as f:
    grid = [line.strip() for line in f if line.strip()]


n, m = len(grid), len(grid[0])


def distance_map(start):
    result = [[n * m for j in range(m)] for i in range(n)]
    result[start[0]][start[1]] = 0
    queue = [start]
    while queue:
        i, j = queue.pop()
        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if ni < 0 or nj < 0 or ni >= n or nj >= m or grid[ni][nj] == "#":
                continue
            if result[ni][nj] <= result[i][j] + 1:
                continue

            result[ni][nj] = result[i][j] + 1
            queue.append((ni, nj))

    return result


def find_cell(c):
    for i, line in enumerate(grid):
        if c in line:
            return (i, line.index(c))

    raise NotImplementedError


start, end = find_cell("S"), find_cell("E")
dstart, dend = distance_map(start), distance_map(end)
inf = n * m

dd = [(+1, 0), (-1, 0), (0, +1), (0, -1)]


def is_valid(x, y):
    return x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != "#"


res = {}


for i in range(n):
    for j in range(m):
        if grid[i][j] != "#":
            continue

        best = inf
        for pdi, pdj in dd:
            pi, pj = i + pdi, j + pdj
            if not is_valid(pi, pj):
                continue

            for ndi, ndj in dd:
                ni, nj = i + ndi, j + ndj
                if not is_valid(ni, nj):
                    continue

                best = min(best, dstart[pi][pj] + dend[ni][nj] + 2)

        res[(i, j)] = best


counted = defaultdict(int)
for k in res.values():
    counted[k] += 1

for k, v in sorted(counted.items()):
    print(f"{v} times can save {dstart[end[0]][end[1]] - k}")


print(sum(x for k, x in counted.items() if dstart[end[0]][end[1]] - k >= 100))
