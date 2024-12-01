from typing import Optional


class Map:
    ranges: list[tuple[int, int, int]]

    def __init__(self, ranges: list[tuple[int, int, int]]):
        self.ranges = sorted(ranges, key=lambda x: x[1])

    def add_range(self, range: tuple[int, int, int]) -> None:
        self.ranges.append(range)

    def map(self, value: int) -> int:
        for dest, start, len_ in self.ranges:
            if start <= value < start + len_:
                return value + dest - start
        return value


def map_seed(seed: int, maps: list[Map]) -> int:
    for map in maps:
        seed = map.map(seed)
    return seed


def main() -> None:
    maps = []
    current: Optional[Map] = None

    with open("2023-05-if-you-give-a-seed-a-fertilizer/input.txt") as f:
        seeds = [int(x) for x in next(f)[len("seeds: ") :].split()]

        for line in f:
            if not line.strip():
                current = None
                continue
            if line[0].isdigit():
                assert current is not None
                current.add_range(tuple(map(int, line.split())))
                continue
            current = Map([])
            maps.append(current)

    print(min(map_seed(seed, maps) for seed in seeds))


if __name__ == "__main__":
    main()
