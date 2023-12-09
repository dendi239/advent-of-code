import argparse
import os

import numpy as np


def guess_next(xs: list[int]) -> int:
    xs = np.array(xs)
    x = 0
    while (xs != 0).any():
        x += xs[-1]
        xs = xs[1:] - xs[:-1]
    return x


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=f"{os.path.dirname(__file__)}/input.txt")
    args = parser.parse_args()
    with open(args.input) as f:
        print(sum(guess_next(list(map(int, line.split()))) for line in f))


if __name__ == "__main__":
    main()
