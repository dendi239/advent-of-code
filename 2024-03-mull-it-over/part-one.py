import re
from typing import Iterable

def parse_mults(line: str) -> Iterable[int]:
    for m in re.findall(r"mul\((\d+),(\d+)\)", line):
        yield int(m[0]) * int(m[1])


def main() -> None:
    with open("2024-03-mull-it-over/input.txt", "r") as f:
        print(sum(value for line in f for value in parse_mults(line)))


if __name__ == "__main__":
    main()
