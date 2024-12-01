import argparse
import re
import logging
from typing import Iterable

logging.basicConfig(level=logging.INFO)


def get_digits(line: str) -> Iterable[int]:
    p = re.compile(r"(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])")
    pos = 0
    str_to_int = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        **{f"{i}": i for i in range(10)},
    }

    logging.info(f"entering string '{line.strip()}'")

    while (m := p.search(line, pos=pos)) is not None:
        start, end = m.span()
        pos = start + 1
        logging.info(f"  found {line[start:end]}")
        yield str_to_int[line[start:end]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="2023-01-trebuchet/input.txt")
    args = parser.parse_args()

    with open(args.input) as f:
        print(
            sum(
                int(f"{d[0]}{d[-1]}")
                for line in f
                if len((d := list(get_digits(line)))) >= 1
            )
        )


if __name__ == "__main__":
    main()
