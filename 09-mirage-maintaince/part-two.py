import argparse
import os

import numpy as np


def guess_prev(xs: list[int]) -> int:
    _xs = xs
    xs = np.array(xs)
    x = 0
    flag = False
    while (xs != 0).any():
        if flag:
            x -= xs[0]
        else:
            x += xs[0]
        flag = not flag
        xs = xs[1:] - xs[:-1]
    print(f"before {_xs} is {x}")
    return x


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=f"{os.path.dirname(__file__)}/input.txt")
    args = parser.parse_args()
    with open(args.input) as f:
        print(sum(guess_prev(list(map(int, line.split()))) for line in f))


if __name__ == "__main__":
    main()
