with open("2024-19-linen-layout/input.txt") as f:
    base = [b.strip() for b in next(f).split(",")]
    next(f)
    tests = [l.strip() for l in f]


def test_line(line):
    is_good = [int(_ == 0) for _ in range(len(line) + 1)]
    for i in range(len(line)):
        if not is_good[i]:
            continue

        for p in base:
            if line[i:][: len(p)] == p:
                is_good[i + len(p)] = True

    return is_good[len(line)]


print(sum(test_line(line) for line in tests))
