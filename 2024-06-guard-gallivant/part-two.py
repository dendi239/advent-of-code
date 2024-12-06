def is_loop(grid):
    i, j = next(
        (i, j)
        for i, row in enumerate(grid)
        for j, cell in enumerate(row)
        if cell == "^"
    )

    di, dj = -1, 0
    seen, seen_dir = set(), set()

    while 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        seen.add((i, j))
        if (i, j, di, dj) in seen_dir:
            break
        seen_dir.add((i, j, di, dj))
        if (
            0 <= i + di < len(grid)
            and 0 <= j + dj < len(grid[i])
            and grid[i + di][j + dj] == "#"
        ):
            di, dj = dj, -di
        else:
            i += di
            j += dj

    return (i, j, di, dj) in seen_dir, seen


def main() -> None:
    with open("2024-06-guard-gallivant/input.txt") as f:
        grid = [line.strip() for line in f if line.strip()]

    _, seen = is_loop(grid)
    ans = 0

    for i, j in seen:
        if grid[i][j] == ".":
            new_grid = [line for line in grid]
            new_grid[i] = new_grid[i][:j] + "#" + new_grid[i][j + 1 :]
            ans += is_loop(new_grid)[0]

    print(ans)


if __name__ == "__main__":
    main()
