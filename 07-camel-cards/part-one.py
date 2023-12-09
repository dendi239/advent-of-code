import argparse
import os
import itertools


BY_STRENGTH = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
POWER = {k: f"{i:02}" for i, k in enumerate(reversed(BY_STRENGTH))}


def the_same(s: str) -> bool:
    return s[:-1] == s[1:]


def canonical_hand(hand: str) -> str:
    power = "".join(POWER[c] for c in hand)
    hand = "".join(reversed(sorted(hand, key=lambda x: POWER[x])))
    if the_same(hand):
        return f"7{power}"
    if the_same(hand[:-1]) or the_same(hand[1:]):
        return f"6{power}"
    if (the_same(hand[:2]) and the_same(hand[2:])) or (
        the_same(hand[:3]) and the_same(hand[3:])
    ):
        return f"5{power}"
    if the_same(hand[:3]) or the_same(hand[1:4]) or the_same(hand[2:]):
        return f"4{power}"
    if (the_same(hand[:2]) and (the_same(hand[2:4]) or the_same(hand[3:]))) or (
        the_same(hand[1:3]) and the_same(hand[3:])
    ):
        return f"3{power}"
    if any(a == b for a, b in zip(hand, hand[1:])):
        return f"2{power}"
    return f"1{power}"


def pick_jockers(hand: str) -> str:
    indices = [i for i in range(len(hand)) if hand[i] == "i"]
    def replace(replacements):
        chars = list(hand)
        for i, r in zip(indices, replacements):
            chars[i] = r
        return ''.join(chars)

    return max(
        map(replace, itertools.combinations(BY_STRENGTH, len(indices))),
        key=canonical_hand
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=f"{os.path.dirname(__file__)}/input.txt")
    args = parser.parse_args()
    with open(args.input) as f:
        hand_bids = [(ts[0], int(ts[1])) for line in f if (ts := line.split())]
        hand_bids = sorted(hand_bids, key=lambda x: canonical_hand(x[0]))
        for h, b in hand_bids:
            print(h, canonical_hand(h), b)
        print(sum((i + 1) * b for i, (_, b) in enumerate(hand_bids)))


if __name__ == "__main__":
    main()
