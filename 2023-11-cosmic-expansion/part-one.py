import os
import collections


def sum_dist(records: list[tuple[int, int]]) -> int:
    records = sorted(records)
    n = sum(c for x, c in records)
    ans, pref, px, add = 0, 0, -1, 0
    print(f"records: {records}")
    for x, c in records:
        add += x - px - 1
        print(f"Next seen point: {x + add:2}, x: {x:2}, px: {px:2}, add: {add:2}")
        suff = n - pref - c
        ans += (x + add) * c * (pref - suff)
        pref, px = pref + c, x
    print()
    return ans


def main() -> None:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        field = [l for line in f if (l := line.strip())]

    n, m = len(field), len(field[0])
    xs = {
        i: c for i in range(n) if (c := sum(1 for j in range(m) if field[i][j] == "#"))
    }
    ys = {
        j: c for j in range(m) if (c := sum(1 for i in range(n) if field[i][j] == "#"))
    }
    print(sum_dist(list(xs.items())) + sum_dist(list(ys.items())))


if __name__ == "__main__":
    main()
