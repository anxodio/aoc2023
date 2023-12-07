import re
from pathlib import Path


def get_calibration_values(line: str) -> int:
    numbers = re.sub(r"\D+", "", line)
    return int(numbers[0] + numbers[-1])


def test_sum_calibration_values():
    assert get_calibration_values("1abc2") == 12
    assert get_calibration_values("pqr3stu8vwx") == 38
    assert get_calibration_values("a1b2c3d4e5f") == 15
    assert get_calibration_values("treb7uchet") == 77


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        lines = [line.rstrip("\n") for line in f]
    print(sum(get_calibration_values(line) for line in lines))
