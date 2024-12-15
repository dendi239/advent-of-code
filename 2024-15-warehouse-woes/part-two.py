with open("2024-15-warehouse-woes/input.txt") as f:
    grid = []
    for line in f:
        if not line.strip():
            break
        grid.append(
            sum(
                (
                    list({"#": "##", "O": "[]", ".": "..", "@": "@."}[c])
                    for c in line.strip()
                ),
                [],
            )
        )

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

    cells_to_move = []
    my_row = [(rx, ry)]

    while my_row:
        next_row = []
        for x, y in my_row:
            cells_to_move.append((x, y))
            if grid[x + dx][y + dy] == "#":
                return False
            if grid[x + dx][y + dy] in "[]":
                next_row.append((x + dx, y + dy))
                if dy == 0:
                    next_row.append(
                        (x + dx, y + dy + (1 if grid[x + dx][y + dy] == "[" else -1))
                    )
        my_row = list(set(next_row))

    for x, y in reversed(cells_to_move):
        grid[x + dx][y + dy], grid[x][y] = grid[x][y], "."

    rx, ry = rx + dx, ry + dy
    return True


# print("\n".join("".join(row) for row in grid))

for direction in commands:
    move(*get_move(direction))
    # print(direction)
    # old = grid[rx][ry]
    # grid[rx][ry] = "X"
    # print("\n".join("".join(row) for row in grid))
    # grid[rx][ry] = old


print(
    sum(
        100 * x + y
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell == "["
    )
)

print("\n".join("".join(row) for row in grid))
