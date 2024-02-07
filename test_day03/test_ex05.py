import re
from pathlib import Path
from dataclasses import dataclass

EngineSchematic = list[str]


@dataclass
class EngineNumber:
    x: int
    y: int
    value: int

    def __len__(self):
        return len(str(self.value))


def get_part_number_sum(schematic: EngineSchematic) -> int:
    numbers = get_numbers_from_schematic(schematic)
    return sum(number.value for number in numbers if is_part_number(schematic, number))


def get_numbers_from_schematic(schematic: EngineSchematic) -> list[EngineNumber]:
    numbers = []
    for y, line in enumerate(schematic):
        for match in re.finditer(r"(\d+)", line):
            numbers.append(EngineNumber(x=match.start(), y=y, value=int(match.group())))
    return numbers


def is_part_number(schematic: EngineSchematic, number: EngineNumber) -> bool:
    min_x = max(0, number.x - 1)
    max_x = min(len(schematic[number.y]) - 1, number.x + len(number))
    min_y = max(0, number.y - 1)
    max_y = min(len(schematic) - 1, number.y + 1)
    for y in range(min_y, max_y + 1):
        if re.search(r"([^\.\d\n])", schematic[y][min_x : max_x + 1]):
            return True
    return False


def test_get_numbers_from_schematic() -> None:
    schematic: EngineSchematic = [
        "467..114..",
        "...*......",
        "..35..633.",
    ]
    assert get_numbers_from_schematic(schematic) == [
        EngineNumber(x=0, y=0, value=467),
        EngineNumber(x=5, y=0, value=114),
        EngineNumber(x=2, y=2, value=35),
        EngineNumber(x=6, y=2, value=633),
    ]


def test_is_part_number() -> None:
    schematic: EngineSchematic = [
        "467..114..",
        "...*......",
        "..35..633.",
    ]
    assert is_part_number(schematic, EngineNumber(x=0, y=0, value=467))
    assert not is_part_number(schematic, EngineNumber(x=5, y=0, value=114))
    assert is_part_number(schematic, EngineNumber(x=2, y=2, value=35))
    assert not is_part_number(schematic, EngineNumber(x=6, y=2, value=633))


def test_get_part_number_sum() -> None:
    schematic: EngineSchematic = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    assert get_part_number_sum(schematic) == 4361


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        schematic = [line.rstrip("\n") for line in f]
    print(get_part_number_sum(schematic))
