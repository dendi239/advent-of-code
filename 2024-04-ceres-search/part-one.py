def num_of_xmas(data: list[str]) -> int:
    return sum(line.count("XMAS") for line in data)


TRANSFORMS = [(dx, dy) for dx in (-1, 0, +1) for dy in (-1, 0, +1) if dx or dy]


def apply_transform(transform: tuple[int, int], data: list[str]) -> list[str]:
    n, m = len(data), len(data[0])
    dx, dy = transform
    prev, next_ = {}, {}

    for i in range(n):
        for j in range(m):
            prev[(i + dx, j + dy)] = (i, j)
            if 0 <= i + dx < n and 0 <= j + dy < m:
                next_[(i, j)] = (i + dx, j + dy)

    result = []
    for i in range(n):
        for j in range(m):
            if (i, j) in prev:
                continue
            c = (i, j)
            s = [data[i][j]]
            while c in next_:
                c = next_[c]
                s.append(data[c[0]][c[1]])

            result.append("".join(s))
    return result


def main() -> None:
    with open("2024-04-ceres-search/input.txt", "r") as f:
        data = [line.strip() for line in f if line.strip()]
    print(
        sum(num_of_xmas(apply_transform(transform, data)) for transform in TRANSFORMS)
    )


if __name__ == "__main__":
    main()
