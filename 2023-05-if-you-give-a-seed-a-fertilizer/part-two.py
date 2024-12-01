from typing import Optional


def intersect_ranges(
    lhs: tuple[int, int], rhs: tuple[int, int]
) -> Optional[tuple[int, int]]:
    b, e = max(lhs[0], rhs[0]), min(lhs[1], rhs[1])
    if b > e:
        return None
    return b, e


def subtract_range(lhs: tuple[int, int], rhs: tuple[int, int]) -> list[tuple[int, int]]:
    if rhs[0] <= lhs[0] and lhs[1] <= rhs[1]:
        return []
    if rhs[0] <= lhs[0]:
        return [(rhs[1], lhs[1])]
    if lhs[1] <= rhs[1]:
        return [(lhs[0], rhs[0])]
    return [(lhs[0], rhs[0]), (rhs[1], lhs[1])]


def shift_range(r: tuple[int, int], shift: int) -> tuple[int, int]:
    return r[0] + shift, r[1] + shift


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

    def __str__(self) -> str:
        return f"<Map ranges: [{', '.join(f'dest: {dest}, start: {start}, end: {start + len_}' for dest, start, len_ in self.ranges)}]>"

    def map_range(self, range: tuple[int, int]) -> list[tuple[int, int]]:
        source_ranges = [range]
        end_ranges = []
        for dest, start, count in self.ranges:
            next_source_ranges = []
            for s in source_ranges:
                if (r := intersect_ranges(s, (start, start + count))) is not None:
                    end_ranges.append(shift_range(r, dest - start))
                    next_source_ranges += subtract_range(s, r)
                else:
                    next_source_ranges.append(s)
            source_ranges = next_source_ranges

        return source_ranges + end_ranges


def map_seed(seed: int, maps: list[Map]) -> int:
    for map in maps:
        seed = map.map(seed)
    return seed


def map_seed_range(seeds: tuple[int, int], maps: list[Map]) -> list[tuple[int, int]]:
    seed_ranges = [seeds]
    for map_ in maps:
        seed_ranges = sum(
            (map_.map_range(seed_range) for seed_range in seed_ranges), []
        )
    return seed_ranges


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

    print(
        min(
            start
            for seed_b, seed_e in zip(seeds[::2], seeds[1::2])
            for start, end in map_seed_range((seed_b, seed_b + seed_e), maps)
        )
    )


if __name__ == "__main__":
    main()
