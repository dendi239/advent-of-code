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

    def combo(self, val: int) -> int:
        return val if val < 4 else [self.a, self.b, self.c][val - 4]


def print_state(cpu: Interpreter, mem: Program) -> None:
    print(f"Registers: A={cpu.a}, B={cpu.b}, C={cpu.c}")
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

while not mem.is_halt():
    op, val = mem.command()
    jump: int | None = None

    if mem.pc == 0:
        print_state(cpu, mem)

    match op:
        case 0:
            cpu.a //= 2 ** cpu.combo(val)
        case 1:
            cpu.b ^= val
        case 2:
            cpu.b = cpu.combo(val) % 8
        case 3:
            if cpu.a:
                jump = val
        case 4:
            cpu.b ^= cpu.c
        case 5:
            outs.append(cpu.combo(val) & 7)
        case 6:
            cpu.b = cpu.a // 2 ** cpu.combo(val)
        case 7:
            cpu.c = cpu.a // 2 ** cpu.combo(val)

    mem.advance(jump)
    jump = None


print(",".join(map(str, outs)))
