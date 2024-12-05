#!/usr/bin/env python3


from collections import defaultdict


def parse_restriction(line):
    try:
        return tuple(map(int, line.strip().split("|")))
    except:
        print("LINE:", line)
        raise


def parse_sequence(line):
    return tuple(map(int, line.strip().split(",")))


def parse_input(f):
    rs = []
    for line in f:
        if not line.strip():
            break
        rs.append(parse_restriction(line))
    ss = []
    for line in f:
        ss.append(parse_sequence(line))
    return rs, ss


def find_worthy(rs, ss):
    rs = set(rs)
    for s in ss:
        if all(
            (s[i2], s[i1]) not in rs
            for i1 in range(len(s))
            for i2 in range(i1 + 1, len(s))
        ):
            continue

        rest = defaultdict(int)
        for c in s:
            rest[c] += 1

        res = []
        while len(res) < len(s):
            for c, v in rest.items():
                if not v:
                    continue
                if all(
                    not v2 or c == c2 or (c2, c) not in rs for c2, v2 in rest.items()
                ):
                    res.append(c)
                    rest[c] -= 1
                    break
        yield res


def main():
    with open("2024-05-print-queue/input.txt") as f:
        rs, ss = parse_input(f)
    print(sum(ws[len(ws) // 2] for ws in find_worthy(rs, ss)))


if __name__ == "__main__":
    main()
