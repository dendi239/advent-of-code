import re

import numpy as np


def parse_command(line: str) -> tuple[np.ndarray, str]:
    p = re.compile(r"(R|U|L|D)\s+(\d+)\s+\(#(.+)\)")
    m = p.fullmatch(line)

    assert m is not None, line

    dir_len, dir_ch = int(m.group(3)[:-1], base=16), "RDLU"[int(m.group(3)[-1])]

    direction = np.array(
        (+1, +0)
        if dir_ch == "R"
        else (+0, +1)
        if dir_ch == "D"
        else (-1, +0)
        if dir_ch == "L"
        else (+0, -1)
    ) * int(dir_len)

    return direction, m.group(3)


def get_area(points: np.ndarray) -> np.float64:
    x, y = points[:, 0], points[:, 1]
    return np.abs((x[1:] * y[:-1] - x[:-1] * y[1:]).sum()) / 2


def main() -> None:
    with open("2023-18-lavaduct-lagoon/input.txt") as f:
        commands = [parse_command(l) for line in f if (l := line.strip())]

    shifts = np.stack([cmd for cmd, _ in commands], axis=0)
    points = shifts.cumsum(axis=0)

    perimeter = np.abs(shifts).sum()
    area = get_area(points)
    outer = (perimeter + 2) / 2
    print(int(area + outer))


if __name__ == "__main__":
    main()
