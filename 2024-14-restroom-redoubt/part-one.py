from collections import defaultdict


def parse_pair(line):
    return tuple(map(int, line.split(",")))


def parse_robot(line):
    pos, dir = line.strip().split(" ")
    return parse_pair(pos[2:]), parse_pair(dir[2:])


with open("2024-14-restroom-redoubt/input.txt", "r") as f:
    robots = [parse_robot(line) for line in f if line.strip()]

h, w, t = 101, 103, 100

quadrants = defaultdict(int)

for r in robots:
    x = ((r[0][0] + r[1][0] * t) % h + h) % h
    y = ((r[0][1] + r[1][1] * t) % w + w) % w

    if x != h // 2 and y != w // 2:
        quadrants[(x < h // 2, y < w // 2)] += 1

res = 1
for a in (True, False):
    for b in (True, False):
        res *= quadrants[a, b]

print(res)
