import re

pattern = re.compile(
    r"Button A: X\+(\d+), Y\+(\d+)\s*"
    r"Button B: X\+(\d+), Y\+(\d+)\s*"
    r"Prize: X=(\d+), Y=(\d+)"
)


with open("2024-13-claw-contraption/input.txt") as f:
    inputs = [list(map(int, line)) for line in pattern.findall(f.read())]

total = 0
for x1, y1, x2, y2, x, y in inputs:
    x += 10000000000000
    y += 10000000000000

    t1 = (y2 * x - x2 * y) // (y2 * x1 - x2 * y1)
    t2 = (y1 * x - x1 * y) // (y1 * x2 - x1 * y2)

    if x1 * t1 + x2 * t2 == x and y1 * t1 + y2 * t2 == y:
        total += 3 * t1 + t2


print(total)
