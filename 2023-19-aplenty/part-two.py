import dataclasses
import re
from collections import defaultdict
from typing import Optional


Record = dict[str, int]
RecordRange = dict[str, tuple[int, int]]


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

    def split(
        self, record_range: RecordRange
    ) -> tuple[Optional[RecordRange], Optional[RecordRange]]:
        [b, e] = record_range[self.key]
        if (self.less and e <= self.threashold) or (
            not self.less and self.threashold < b
        ):
            return record_range, None
        if (not self.less and e <= self.threashold) or (
            self.less and self.threashold < b
        ):
            return None, record_range
        if self.less:
            return (
                record_range | {self.key: (b, self.threashold)},
                record_range | {self.key: (self.threashold, e)},
            )
        else:
            return (
                record_range | {self.key: (self.threashold + 1, e)},
                record_range | {self.key: (b, self.threashold + 1)},
            )


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

    def split(self, record_range: RecordRange) -> dict[str, list[RecordRange]]:
        result = defaultdict(list)
        ranges = [record_range]
        for r in self.rules:
            next_ranges = []
            for rr in ranges:
                a, b = r.split(rr)
                if a is not None:
                    result[r.destination].append(a)
                if b is not None:
                    next_ranges.append(b)
            ranges = next_ranges
        result[self.fallback] += ranges
        return dict(result)


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


def count_variants(r: RecordRange) -> int:
    res = 1
    for b, e in r.values():
        res *= e - b
    return res


def split_rules(
    record: RecordRange, rules: dict[str, Rules]
) -> dict[str, list[RecordRange]]:
    state = defaultdict(list)
    state["in"] = [record]

    while not set(state.keys()).issubset({"A", "R"}):
        next_state = defaultdict(list)
        for k, rs in state.items():
            if k not in rules:
                next_state[k] += rs
                continue
            for r in rs:
                for nk, rrs in rules[k].split(r).items():
                    next_state[nk] += rrs
        state = next_state

    return state


def main() -> None:
    rules: dict[str, Rules] = {}
    records: list[dict[str, int]] = []

    with open("2023-19-aplenty/input.txt") as f:
        for line in f:
            if not line.strip():
                break
            n, r = parse_rules(line.strip())
            rules[n] = r

        records = [parse_record(l) for line in f if (l := line.strip())]

    full_range = RecordRange(
        {"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)}
    )
    final_states = split_rules(full_range, rules)

    print(sum(count_variants(r) for r in final_states.get("A", [])))


if __name__ == "__main__":
    main()
