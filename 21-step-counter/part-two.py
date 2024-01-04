"""step counter solution"""

def main() -> None:
    """Main function."""

    with open("21-step-counter/input.txt", encoding="utf-8") as f:
        grid = [line for line in f.read().splitlines() if line]
        n, m = len(grid), len(grid[0])

    def valid(x, y):
        return grid[x % n][y % m] != "#"

    starts = [
        (x, y) for x, line in enumerate(grid) for y, c in enumerate(line) if c == "S"
    ]

    def next_starts(starts):
        next_starts = []
        for x, y in starts:
            for dx, dy in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
                if valid(x1 := x + dx, y1 := y + dy):
                    next_starts.append((x1, y1))
        return list(set(next_starts))

    steps = 26_501_365
    for _ in range(steps % len(grid)):
        starts = next_starts(starts)

    xi = [len(starts)]
    for _ in range(2):
        for _ in range(n):
            starts = next_starts(starts)
        xi.append(len(starts))

    c = xi[0]
    a = (xi[2] - 2 * xi[1] + xi[0]) // 2
    b = xi[1] - a - c

    x = steps // n
    print(a * x**2 + b * x + c)


if __name__ == "__main__":
    main()
