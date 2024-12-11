with open("2024-11-plutonian-pebbles/input.txt") as f:
    numbers = [int(x) for line in f for x in line.split()]


def next_(x: int) -> list[int]:
    if x == 0:
        return [1]
    if len(x_str := str(x)) % 2 == 0:
        return [int(x_str[: len(x_str) // 2]), int(x_str[len(x_str) // 2 :])]
    return [x * 2024]


for i in range(25):
    numbers = sum((next_(x) for x in numbers), [])

print(len(numbers))
