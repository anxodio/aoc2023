import re
from pathlib import Path
from dataclasses import dataclass

GEAR_AREA_WIDTH = 3
GEAR_AREA_HEIGHT = 3
NUMBER_AREA_HEIGHT = 1

EngineSchematic = list[str]


@dataclass
class EngineNumber:
    x: int
    y: int
    value: int

    def __len__(self):
        return len(str(self.value))


def get_gear_ratios_sum(schematic: EngineSchematic) -> int:
    gear_ratios_sum = 0
    numbers = get_numbers_from_schematic(schematic)
    for y, line in enumerate(schematic):
        for match in re.finditer(r"(\*)", line):
            adjacent_numbers = get_adjacent_numbers(numbers, match.start(), y)
            if len(adjacent_numbers) == 2:
                gear_ratios_sum += adjacent_numbers[0].value * adjacent_numbers[1].value
    return gear_ratios_sum


def get_numbers_from_schematic(schematic: EngineSchematic) -> list[EngineNumber]:
    numbers = []
    for y, line in enumerate(schematic):
        for match in re.finditer(r"(\d+)", line):
            numbers.append(EngineNumber(x=match.start(), y=y, value=int(match.group())))
    return numbers


def get_adjacent_numbers(
    numbers: list[EngineNumber], x: int, y: int
) -> list[EngineNumber]:
    gear_area_x = max(0, x - 1)
    gear_area_y = max(0, y - 1)

    adjacent_numbers: list[EngineNumber] = []
    for number in numbers:
        if (
            gear_area_x < number.x + len(number)
            and gear_area_x + GEAR_AREA_WIDTH > number.x
            and gear_area_y < number.y + NUMBER_AREA_HEIGHT
            and gear_area_y + GEAR_AREA_HEIGHT > number.y
        ):
            adjacent_numbers.append(number)
    return adjacent_numbers


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


def test_get_adjacent_numbers() -> None:
    numbers = [
        EngineNumber(x=0, y=0, value=467),
        EngineNumber(x=5, y=0, value=114),
        EngineNumber(x=2, y=2, value=35),
        EngineNumber(x=6, y=2, value=633),
    ]
    assert get_adjacent_numbers(numbers, 3, 1) == [
        EngineNumber(x=0, y=0, value=467),
        EngineNumber(x=2, y=2, value=35),
    ]


def test_get_gear_ratios_sum() -> None:
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
    assert get_gear_ratios_sum(schematic) == 467835


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        schematic = [line.rstrip("\n") for line in f]
    print(get_gear_ratios_sum(schematic))
