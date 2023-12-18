import re

import numpy as np


def calc_hand(line: str) -> int:
    p = re.compile("Card\s+\\d+:([0-9\s]*)\|([0-9\\s]*)")
    m = p.fullmatch(line)

    try:
        win = [int(x) for x in m.group(1).split()]
        me = [int(x) for x in m.group(2).split()]
    except:
        print(line, m)
        raise

    return sum(1 for x in me if x in win)


def main():
    with open("04-scratch-cards/input.txt") as f:
        hands = [l for line in f if (l := line.strip())]

    counts = np.ones(len(hands), dtype=int)
    for i, h in enumerate(hands):
        counts[i + 1 : i + calc_hand(h) + 1] += counts[i]

    print(counts.sum())


if __name__ == "__main__":
    main()
