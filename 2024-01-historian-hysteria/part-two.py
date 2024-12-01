#! /usr/bin/env python3

import os
from collections import defaultdict

def main() -> None:
    xs, ys = [], []
    with open("2024-01-historian-hysteria/input.txt", "r") as f:
        for line in f:
            x, y = map(int, line.split())
            xs.append(x)
            ys.append(y)

    y_count = defaultdict(int)
    for y in ys:
        y_count[y] += 1

    print(sum(x * y_count[x] for x in xs))

if __name__ == "__main__":
    main()