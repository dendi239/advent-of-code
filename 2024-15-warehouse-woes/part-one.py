with open("2024-15-warehouse-woes/input.txt") as f:
    grid = []
    for line in f:
        if not line.strip():
            break
        grid.append(list(line.strip()))

    commands = ""
    for line in f:
        commands += line.strip()


rx, ry = 0, 0

for x, row in enumerate(grid):
    for y, cell in enumerate(row):
        if cell == "@":
            rx, ry = x, y
            break


def get_move(direction):
    if direction == "^":
        return -1, 0
    elif direction == "v":
        return 1, 0
    elif direction == "<":
        return 0, -1
    else:
        return 0, 1


def move(dx, dy):
    global rx, ry, grid

    x, y = rx + dx, ry + dy
    while grid[x][y] == "O":
        x += dx
        y += dy

    if grid[x][y] == "#":
        return False

    grid[rx][ry] = "."
    grid[x][y] = "O"
    rx, ry = rx + dx, ry + dy
    grid[rx][ry] = "@"
    return True


for direction in commands:
    move(*get_move(direction))


print(
    sum(
        100 * x + y
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell == "O"
    )
)
