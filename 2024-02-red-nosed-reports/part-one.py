#! /usr/bin/env python3


def main() -> None:
    goods = 0

    with open("2024-02-red-nosed-reports/input.txt") as f:
        for line in f:
            if not line.strip():
                continue
            xs = list(map(int, line.strip().split()))
            goods += all(x1 < x2 <= x1 + 3 for x1, x2 in zip(xs[:-1], xs[1:])) or all(
                x1 - 3 <= x2 < x1 for x1, x2 in zip(xs[:-1], xs[1:])
            )

    print(goods)


if __name__ == "__main__":
    main()
