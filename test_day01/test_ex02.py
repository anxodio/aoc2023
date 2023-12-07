import re
from pathlib import Path


_SPELL_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_calibration_values(line: str) -> int:
    for spelled, number in _SPELL_MAP.items():
        line = line.replace(spelled, spelled + number + spelled)
    numbers = re.sub(r"\D+", "", line)
    return int(numbers[0] + numbers[-1])


def test_sum_calibration_values():
    assert get_calibration_values("two1nine") == 29
    assert get_calibration_values("eightwothree") == 83
    assert get_calibration_values("abcone2threexyz") == 13
    assert get_calibration_values("xtwone3four") == 24
    assert get_calibration_values("4nineeightseven2") == 42
    assert get_calibration_values("zoneight234") == 14
    assert get_calibration_values("7pqrstsixteen") == 76


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    print(sum(get_calibration_values(line) for line in lines))
