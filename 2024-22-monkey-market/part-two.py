from collections import defaultdict
import itertools


with open("2024-22-monkey-market/input.txt", "r") as f:
    numbers = [int(line.strip()) for line in f]


def prune(x):
    return x % 16777216


def mix(secret, other):
    return secret ^ other


def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def diffs_to_bought(x) -> dict[tuple[int, int, int, int], int]:
    bought = {}
    xs = list(
        itertools.accumulate(itertools.repeat(x, 2001), lambda y, _: next_secret(y))
    )
    xs = [x % 10 for x in xs]

    for i in range(4, len(xs)):
        key = tuple(xs[i - j] - xs[i - j - 1] for j in range(3, -1, -1))
        value = xs[i]

        if key not in bought:
            bought[key] = value

    return bought


total = defaultdict(int)

for n in numbers:
    for k, v in diffs_to_bought(n).items():
        total[k] += v


target = max(total.values())

for k, v in total.items():
    if v == target or k == (-2, 1, -1, 3):
        print(k)
        for n in numbers:
            print(f" {n}: {diffs_to_bought(n).get(k, None)}")

print(target)
