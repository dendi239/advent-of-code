#! /usr/bin/env python3


def is_good(xs: list[int]) -> bool:
    return all(x1 < x2 <= x1 + 3 for x1, x2 in zip(xs[:-1], xs[1:])) or all(
                x1 - 3 <= x2 < x1 for x1, x2 in zip(xs[:-1], xs[1:])
            )


def main() -> None:
    goods = 0

    with open("2024-02-red-nosed-reports/input.txt") as f:
        for line in f:
            if not line.strip():
                continue
            xs = list(map(int, line.strip().split()))
            goods += is_good(xs) or any(is_good(xs[:i] + xs[i+1:]) for i in range(len(xs)))

    print(goods)


if __name__ == "__main__":
    main()
