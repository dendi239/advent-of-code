from dataclasses import dataclass


with open("2024-21-keypad-conundrum/input.txt") as f:
    codes = [l for line in f if (l := line.strip())]


class Keypad:
    def __init__(self, buttons):
        self.buttons = buttons

    def is_valid(self, pos):
        return pos in self.buttons

    def action(self, pos):
        return self.buttons[pos]

    def perform(self, pos, action) -> tuple[tuple[int, int], str] | None:
        match action:
            case "<":
                next_pos = pos[0] - 1, pos[1]
                if not self.is_valid(next_pos):
                    return None
            case "^":
                next_pos = pos[0], pos[1] + 1
                if not self.is_valid(next_pos):
                    return None
            case ">":
                next_pos = pos[0] + 1, pos[1]
                if not self.is_valid(next_pos):
                    return None
            case "v":
                next_pos = pos[0], pos[1] - 1
                if not self.is_valid(next_pos):
                    return None
            case _:
                assert action == "A"
                return pos, self.action(pos)

        return next_pos, ""

    def print(self, hover=None):
        n, m = map(lambda i: max(c[i] for c in self.buttons) + 1, [0, 1])
        for y in range(m - 1, -1, -1):
            print(
                "".join(
                    "x "
                    if (x, y) == hover
                    else f"{self.buttons[x, y]:2}"
                    if (x, y) in self.buttons
                    else ".."
                    for x in range(n)
                )
            )


dpad = Keypad(
    {
        (0, 0): "<",
        (1, 0): "v",
        (2, 0): ">",
        (1, 1): "^",
        (2, 1): "A",
    }
)

keypad = Keypad(
    {
        (0, 1): "1",
        (0, 2): "4",
        (0, 3): "7",
        (1, 0): "0",
        (1, 1): "2",
        (1, 2): "5",
        (1, 3): "8",
        (2, 0): "A",
        (2, 1): "3",
        (2, 2): "6",
        (2, 3): "9",
    }
)


@dataclass(frozen=True)
class State:
    dpos1: tuple[int, int] = (2, 1)
    dpos2: tuple[int, int] = (2, 1)
    kpos: tuple[int, int] = (2, 0)
    code: str = ""

    def print(self):
        print(f"Written code: {self.code}")
        dpad.print(self.dpos1)
        dpad.print(self.dpos2)
        keypad.print(self.kpos)


def perform_action(state, action) -> State | None:
    poses = [state.dpos1, state.dpos2, state.kpos]
    for i, pos in enumerate(poses):
        pad = keypad if i == 2 else dpad
        next_pos_action = pad.perform(pos, action)
        if next_pos_action is None:
            return None
        poses[i], action = next_pos_action
        if not action:
            break
    return State(*poses, code=state.code + action)


def find_code(code) -> int:
    queue = [(0, State())]
    state_to_dist = {}

    while queue:
        d, s = queue.pop(0)
        if s in state_to_dist and state_to_dist[s] <= d:
            continue

        state_to_dist[s] = d
        if s.code == code:
            return d

        for action in "<>^vA":
            next_state = perform_action(s, action)
            if (
                next_state is None
                or (next_state in state_to_dist and state_to_dist[next_state] <= d + 1)
                or not code.startswith(next_state.code)
            ):
                continue
            if next_state.code == code:
                return d + 1

            queue.append((d + 1, next_state))
    assert False


print(sum(find_code(code) * int(code[:-1]) for code in codes))
