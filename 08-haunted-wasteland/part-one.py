import os
import re


def main() -> None:
    graph: dict[str, dict[str, str]] = {}

    with open("08-haunted-wasteland/input.txt") as f:
        commands = next(f).strip()
        pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")

        for line in f:
            if (m := pattern.fullmatch(line.strip())):
                node = m.group(1)
                left = m.group(2)
                right = m.group(3)
                graph[node] = {"L": left, "R": right}

    compact: dict[str, str | int] = {}
    for node in graph:
        curr = node
        for i, c in enumerate(commands):
            curr = graph[curr][c]
            if curr == "ZZZ":
                compact[node] = i + 1
                break
        else:
            compact[node] = curr

    answer = 0
    curr = "AAA"
    used = set()

    while True:
        used.add(curr)
        next_node = compact[curr]

        if isinstance(next_node, int):
            answer += next_node
            break

        if next_node in used:
            break
        
        answer += len(commands)
        curr = next_node
    
    print(answer)


if __name__ == "__main__":
    main()