import argparse
import logging
from functools import lru_cache


def count_matches(line: str) -> int:
    print(line)
    s, arr_str = line.split()

    arr = [int(x) for x in arr_str.split(",")]
    s = '?'.join([s] * 5)
    arr *= 5

    def logged(f):
        def wrapper(i_s, i_arr, part):
            res = f(i_s, i_arr, part)
            logging.debug(
                f"  line: '{s[:i_s]}', arr: {arr[:i_arr]}, suff: {part}, count: {res}"
            )
            return res

        return wrapper

    @lru_cache(maxsize=None)
    @logged
    def dp(i_s: int, i_arr: int, part: int) -> int:
        """
        Counts number of strings s[:i_s] that:
        - prefix matching arr[:i_arr]
        - after it has some blank spance
        - ends with part.
        """

        assert 0 <= i_s <= len(s)

        if i_s == 0:
            return i_arr == 0 and part == 0

        if part != 0:
            if part > i_s or any(c == "." for c in s[i_s - part : i_s]):
                return 0

            if part == i_s:
                return 0 if i_arr != 0 else 1

            if i_arr == 0:
                return 0 if any(c == "#" for c in s[: i_s - part]) else 1

            return dp(i_s - part, i_arr, 0)

        if i_arr == 0:  # part == 0 by this point
            return 0 if any(c == "#" for c in s[:i_s]) else 1

        # Makes the whole dp one N^2 heavier.
        # Who cares as long as it runs in a few seconds time?
        return sum(
            dp(i_p, i_arr - 1, arr[i_arr - 1])
            for i_p in range(i_s)
            if all(s[i] != '#' for i in range(i_p, i_s))
        )

    ans = dp(len(s), len(arr), 0) + dp(len(s), len(arr) - 1, arr[-1])
    logging.info(f"line: '{s}', arr: {arr}, ans: {ans}")

    return ans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    with open("12-hot-springs/input.txt") as f:
        print(sum(count_matches(l) for line in f if (l := line.strip())))


if __name__ == "__main__":
    main()
