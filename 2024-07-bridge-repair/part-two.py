def reachable(xs: list[int]) -> set[int]:
    results = {xs[0]}
    for x in xs[1:]:
        results = (
            {x + y for y in results}
            | {x * y for y in results}
            | {int(str(y) + str(x)) for y in results}
        )
    return results


def main() -> None:
    with open("2024-07-bridge-repair/input.txt") as f:
        data = {
            int(lhs): [int(x) for x in rhs.split()]
            for line in f
            if line
            if (parts := line.strip().split(":"))[0]
            if (lhs := parts[0]) and (rhs := parts[1])
        }

    print(
        sum(target for target, numbers in data.items() if target in reachable(numbers))
    )


if __name__ == "__main__":
    main()
