import dataclasses
import re


@dataclasses.dataclass
class Rule:
    key: str
    destination: str
    threashold: int
    less: bool

    def accepts(self, record: dict[str, int]) -> bool:
        if self.key in record and (
            (record[self.key] > self.threashold and not self.less)
            or (record[self.key] < self.threashold and self.less)
        ):
            return True
        return False


def parse_rule(line: str) -> Rule:
    p = re.compile(r"(\w+)([<>])(\d+):(\w+)")
    key, sign, threashold, destination = p.match(line).groups()
    return Rule(
        key=key,
        threashold=int(threashold),
        less=(sign == "<"),
        destination=destination,
    )


@dataclasses.dataclass
class Rules:
    rules: list[Rule]
    fallback: str

    def eval(self, record: dict[str, int]) -> str:
        for rule in self.rules:
            if rule.accepts(record):
                return rule.destination
        return self.fallback


def parse_rules(line: str) -> tuple[str, Rules]:
    p = re.compile(r"(\w+)\{(.*)\}")
    name, inner = p.match(line).groups()
    rules = inner.split(",")
    return name, Rules(rules=[parse_rule(r) for r in rules[:-1]], fallback=rules[-1])


def parse_record(line: str) -> dict[str, int]:
    return {
        kv[0]: int(kv[1])
        for part in line.strip()[1:-1].split(",")
        if (kv := part.split("="))
    }


def apply_rules(record: dict[str, str], rules: dict[str, Rules]) -> str:
    rn = "in"
    while rn in rules:
        rn = rules[rn].eval(record)
    return rn


def main() -> None:
    rules: dict[str, Rules] = {}
    records: list[dict[str, int]] = []

    with open("19-aplenty/input.txt") as f:
        for line in f:
            if not line.strip():
                break
            n, r = parse_rules(line.strip())
            rules[n] = r

        records = [parse_record(l) for line in f if (l := line.strip())]

    print(sum(sum(r.values()) for r in records if apply_rules(r, rules) == "A"))


if __name__ == "__main__":
    main()
