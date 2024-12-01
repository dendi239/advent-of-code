#! /usr/bin/env python3


def main() -> None:
    xs, ys = [], []
    with open("2024-01-historian-hysteria/input.txt", "r") as f:
        for line in f:
            x, y = map(int, line.split())
            xs.append(x)
            ys.append(y)
    xs.sort()
    ys.sort()

    print(sum(abs(x - y) for x, y in zip(xs, ys)))

if __name__ == "__main__":
    main()