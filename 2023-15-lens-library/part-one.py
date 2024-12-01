def Hash(s: str) -> int:
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res %= 256
    return res


def main() -> None:
    with open("2023-15-lens-library/input.txt") as f:
        l = f.read()

    print(sum(Hash(s) for st in l.split(",") if (s := st.strip())))


if __name__ == "__main__":
    main()
