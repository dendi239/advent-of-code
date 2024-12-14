from collections import defaultdict


def parse_pair(line):
    return tuple(map(int, line.split(",")))


def parse_robot(line):
    pos, dir = line.strip().split(" ")
    return parse_pair(pos[2:]), parse_pair(dir[2:])


with open("2024-14-restroom-redoubt/input.txt", "r") as f:
    robots = [parse_robot(line) for line in f if line.strip()]


print(robots)

h, w, t = 101, 103, 100

quadrants = defaultdict(int)


def in_t_sec(t):
    return [
        (((r[0][0] + r[1][0] * t) % h + h) % h, ((r[0][1] + r[1][1] * t) % w + w) % w)
        for r in robots
    ]


def render(positions):
    positions = set(positions)
    for y in range(w):
        for x in range(h):
            print("#" if (x, y) in positions else ".", end="")
        print()


def is_there_base(positions):
    positions = set(positions)
    columns = set()
    for x, y in positions:
        if (
            (x + 1, y) in positions
            and (x + 2, y) in positions
            and (x + 3, y) in positions
            and (x + 4, y) in positions
        ):
            columns.add(y)
    return len(columns) >= 2


for t in range(1_000_000):
    now = in_t_sec(t)
    if not is_there_base(now):
        continue

    render(now)

    if input("Continue? (y/n)") == "n":
        break


print(t)
