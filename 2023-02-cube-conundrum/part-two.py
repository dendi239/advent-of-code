import dataclasses
import os
import re


@dataclasses.dataclass
class Game:
    id_: int
    red: int
    green: int
    blue: int


def parse_game(game: str) -> Game:
    game_pattern = re.compile(r"Game (\d+):")
    record_pattern = re.compile(r"\s*(\d+) (red|green|blue)\s*")

    g = Game(id_=int(game_pattern.match(game).group(1)), red=0, green=0, blue=0)
    records = [
        p for draw in game.split(":")[1].strip().split(";") for p in draw.split(",")
    ]

    for r in records:
        try:
            cnt, type_ = record_pattern.match(r).groups()
        except:
            print(f"failed to parse '{r}'")
            raise
        setattr(g, type_, max(getattr(g, type_), int(cnt)))

    return g


def main() -> None:
    with open(os.path.join(os.path.dirname("2023-02-cube-conundrum/part-two.py"), "input.txt")) as f:
        print(
            sum(
                g.red * g.blue * g.green
                for line in f
                if (g := parse_game(line)) is not None
            )
        )


if __name__ == "__main__":
    main()
