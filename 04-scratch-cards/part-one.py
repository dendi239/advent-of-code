import re


def calc_hand(line: str) -> int:
    p = re.compile("Card\s+\\d+:([0-9\s]*)\|([0-9\\s]*)")
    m = p.fullmatch(line)

    try:
        win = [int(x) for x in m.group(1).split()]
        me = [int(x) for x in m.group(2).split()]
    except:
        print(line, m)
        raise

    return 2 ** sum(1 if x in win else 0 for x in me) // 2


def main():
    with open("04-scratch-cards/input.txt") as f:
        print(sum(calc_hand(h) for line in f if (h := line.strip())))


if __name__ == "__main__":
    main()
