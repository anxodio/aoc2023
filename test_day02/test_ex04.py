import re
import math
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Game:
    id: int
    sets: list["GameSet"] = field(default_factory=list)


@dataclass
class GameSet:
    red: int = 0
    green: int = 0
    blue: int = 0


def parse_line(line: str) -> Game:
    match_obj = re.match(r"Game (?P<id>\d+): (?P<raw_sets>.*)", line)
    if not match_obj:
        raise Exception("Invalid game line")
    group_id, raw_sets = int(match_obj["id"]), match_obj["raw_sets"].split("; ")
    return Game(
        id=group_id,
        sets=[
            GameSet(
                **{
                    cubes.split()[1]: int(cubes.split()[0])
                    for cubes in raw_set.split(", ")
                }
            )
            for raw_set in raw_sets
        ],
    )


def get_game_power(game: Game) -> int:
    maximums: dict[str, int] = defaultdict(int)
    for set in game.sets:
        maximums["red"] = max(maximums["red"], set.red)
        maximums["green"] = max(maximums["green"], set.green)
        maximums["blue"] = max(maximums["blue"], set.blue)
    return math.prod(n for n in maximums.values())


def test_parse_line():
    assert parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == Game(
        id=1,
        sets=[
            GameSet(blue=3, red=4),
            GameSet(red=1, green=2, blue=6),
            GameSet(green=2),
        ],
    )
    assert parse_line(
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    ) == Game(
        id=3,
        sets=[
            GameSet(green=8, blue=6, red=20),
            GameSet(red=4, green=13, blue=5),
            GameSet(green=5, red=1),
        ],
    )


def test_get_game_power():
    assert (
        get_game_power(
            parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
        )
        == 48
    )
    assert (
        get_game_power(
            parse_line(
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
            )
        )
        == 1560
    )


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        games = [parse_line(line.rstrip("\n")) for line in f]
    print(sum(get_game_power(game) for game in games))
