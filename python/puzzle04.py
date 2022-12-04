
def parse_range(range_string):
    low, high = [int(x) for x in range_string.split("-")]
    return (low, high)


def parse_line(line):
    elf_one, elf_two = line.split(",")
    return (parse_range(elf_one), parse_range(elf_two))


def does_one_range_fully_contain_the_other(one, two): # lol naming
    if one[0] >= two[0] and one[1] <= two[1]:
        return True
    elif two[0] >= one[0] and two[1] <= one[1]:
        return True
    return False


def count_fully_contained_ranges(input_string):
    lines = [x for x in input_string.split("\n") if x != ""]
    result = 0
    for line in lines:
        ranges = parse_line(line)
        if does_one_range_fully_contain_the_other(*ranges):
            result += 1
    return result


if __name__ == "__main__":
    input04 = open("../input/input04").read()
    p1_answer = count_fully_contained_ranges(input04)
    print(f"(p1 answer) assignments where one range fully contains the other: {p1_answer}") # 459


###########################

SAMPLE_INPUT = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def test_parse_range():
    for input_string, expected in [
        ("2-4", (2,4)),
        ("6-8", (6,8)),
        ("2-3", (2,3)),
        ("4-5", (4,5)),
        ("5-7", (5,7)),
        ("7-9", (7,9)),
        ("2-8", (2,8)),
        ("3-7", (3,7)),
        ("6-6", (6,6)),
        ("4-6", (4,6)),
        ("2-6", (2,6)),
        ("4-8", (4,8)),
    ]:
        actual = parse_range(input_string)
        assert expected == actual


def test_parse_line():
    for line, expected in [
        ("2-4,6-8", ((2,4), (6,8))),
        ("2-3,4-5", ((2,3), (4,5))),
        ("5-7,7-9", ((5,7), (7,9))),
        ("2-8,3-7", ((2,8), (3,7))),
        ("6-6,4-6", ((6,6), (4,6))),
        ("2-6,4-8", ((2,6), (4,8))),
    ]:
        actual = parse_line(line)
        assert expected == actual


def test_does_one_range_fully_contain_the_other():
    for ranges, expected in [
        (((2,4), (6,8)), False),
        (((2,3), (4,5)), False),
        (((5,7), (7,9)), False),
        (((2,8), (3,7)), True),
        (((6,6), (4,6)), True),
        (((2,6), (4,8)), False),
    ]:
        one, two = ranges
        actual = does_one_range_fully_contain_the_other(one, two)
        assert expected == actual


def test_count_fully_contained_ranges():
    expected = 2
    actual = count_fully_contained_ranges(SAMPLE_INPUT)
    assert expected == actual
