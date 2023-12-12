import re
from pathlib import Path
from dataclasses import dataclass, field


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


def possible_games_sum(games: list[Game]) -> int:
    result = 0
    for game in games:
        for set in game.sets:
            if set.red > 12 or set.green > 13 or set.blue > 14:
                break
        else:
            result += game.id
    return result


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


def test_possible_games_sum():
    games = [
        parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"),
        parse_line("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"),
        parse_line(
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
        ),
        parse_line(
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
        ),
        parse_line("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"),
    ]
    assert possible_games_sum(games) == 8


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        games = [parse_line(line.rstrip("\n")) for line in f]
    print(possible_games_sum(games))
