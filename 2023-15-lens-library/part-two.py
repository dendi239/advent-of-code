def hash_(s: str) -> int:
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res %= 256
    return res


class Lens:
    def __init__(self, label: str, power: int | str = 0) -> None:
        self.label = label
        self.power = int(power)

    def __str__(self) -> str:
        return f"[{self.label} {self.power}]"

    def __repr__(self) -> str:
        return f"[{self.label} {self.power}]"

    def __hash__(self) -> int:
        return hash_(self.label)


class Box:
    def __init__(self):
        self.order = []
        self.lens_to_index = {}

    def add(self, lens: Lens) -> None:
        for i, l in enumerate(self.order):
            if l.label == lens.label:
                self.order[i] = lens
                break
        else:
            self.order.append(lens)

    def remove(self, lens: Lens) -> None:
        for i, l in enumerate(self.order):
            if l.label == lens.label:
                self.order = self.order[:i] + self.order[i + 1 :]

    def total_power(self) -> int:
        return sum((i + 1) * lens.power for i, lens in enumerate(self.order))

    def __bool__(self):
        return bool(self.order)


def main() -> None:
    with open("2023-15-lens-library/input.txt") as f:
        commands = [s for st in f.read().split(",") if (s := st.strip())]

    boxes = [Box() for _ in range(256)]
    for cmd in commands:
        if cmd[-1] == "-":
            lens = Lens(label=cmd[:-1])
            print(f"removing lens {lens} from box {hash(lens)}")
            boxes[hash(lens)].remove(lens)
        else:
            lens = Lens(*cmd.split("="))
            boxes[hash(lens)].add(lens)

        print(f'After "{cmd}":')

        for i, box in enumerate(boxes):
            if box:
                print(f"Box {i}: {', '.join(str(lens) for lens in box.order)}")
        print()

    print(sum((i + 1) * box.total_power() for i, box in enumerate(boxes)))


if __name__ == "__main__":
    main()
