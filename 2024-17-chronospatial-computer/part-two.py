class Program:
    def __init__(self, commands: list[tuple[int, int]]) -> None:
        self.commands = commands
        self.pc = 0

    def command(self) -> tuple[int, int]:
        return self.commands[self.pc]

    def advance(self, jump: int | None = None) -> None:
        if jump is not None:
            self.pc = jump // 2
        else:
            self.pc += 1

    def is_halt(self) -> bool:
        return self.pc >= len(self.commands)


class Interpreter:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a, self.b, self.c = a, b, c

    def __repr__(self) -> str:
        return f"(a={self.a}, b={self.b}, c={self.c})"

    def combo(self, val: int) -> int:
        return val if val < 4 else [self.a, self.b, self.c][val - 4]


def print_state(cpu: Interpreter, mem: Program) -> None:
    print(f"Registers: A={cpu.a:b}, B={cpu.b}, C={cpu.c}")
    print(f"Program: {' '.join(f'{op}{val}' for op, val in mem.commands)}")
    print("         " + "   " * mem.pc + "^^")


with open("2024-17-chronospatial-computer/input.txt", "r") as f:
    a, b, c = [int(l.split(":")[-1].strip()) for l in [next(f), next(f), next(f)]]
    next(f)
    commands = list(map(int, next(f).lstrip("Program: ").split(",")))
    commands = list(zip(commands[::2], commands[1::2]))

cpu = Interpreter(a, b, c)
mem = Program(commands)
outs = []

target = sum(commands, tuple())
print(target)


def run_to_jump(cpu: Interpreter, mem: Program) -> tuple[int, bool]:
    seen_value, jumped = 0, False
    while not mem.is_halt():
        op, val = mem.command()
        jump = None

        match op:
            case 0:
                cpu.a //= 2 ** cpu.combo(val)
            case 1:
                cpu.b ^= val
            case 2:
                cpu.b = cpu.combo(val) & 7
            case 3:
                if cpu.a:
                    jump = val
            case 4:
                cpu.b ^= cpu.c
            case 5:
                seen_value = cpu.combo(val) & 7
            case 6:
                cpu.b = cpu.a // 2 ** cpu.combo(val)
            case 7:
                cpu.c = cpu.a // 2 ** cpu.combo(val)

        mem.advance(jump)
        if jump is not None:
            jumped = True
            break

    return seen_value, jumped


to_look = {(0, (0, 0, 0))}

while True:
    to_look = sorted(to_look)
    i, cpu_start = to_look[0]
    to_look = set(to_look[1:])
    cpu_start = Interpreter(*cpu_start)

    if i == len(target):
        print(cpu_start.a)
        break

    for _ in range(1024):
        cpu, mem.pc, jumped = type(cpu_start)(**cpu_start.__dict__), 0, False
        for j in range(i + 1):
            final, jumped = run_to_jump(cpu, mem)
            if final != target[j]:
                final = -1
                break
            if not jumped:
                break

        if jumped == (i + 1 != len(target)) and final != -1:
            to_look.add((i + 1, (cpu_start.a, cpu_start.b, cpu_start.c)))

        cpu_start.a += 8**i
