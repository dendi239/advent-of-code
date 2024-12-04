def main() -> None:
    with open("2024-04-ceres-search/input.txt", "r") as f:
        data = [line.strip() for line in f if line.strip()]

    n, m = len(data), len(data[0])
    res = 0

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if data[i][j] != "A":
                continue
            if (
                {data[i + 1][j + 1], data[i - 1][j - 1]}
                == set("MS")
                == {data[i + 1][j - 1], data[i - 1][j + 1]}
            ):
                res += 1

    print(res)


if __name__ == "__main__":
    main()
