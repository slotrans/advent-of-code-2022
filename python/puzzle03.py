
def split_compartments(rucksack):
    halfway = len(rucksack) // 2
    return (rucksack[:halfway], rucksack[halfway:])


def find_erroneous_item(rucksack):
    first_half, second_half = split_compartments(rucksack)
    items_in_common = set(first_half).intersection(set(second_half))
    if len(items_in_common) == 1:
        return list(items_in_common)[0]
    else:
        raise ValueError(f"multiple items found in both compartments: {items_in_common}")


def get_priority(item):
    # ord("a") -> 97
    # ord("A") -> 65
    if "a" <= item <= "z":
        return ord(item) - 96
    elif "A" <= item <= "Z":
        return ord(item) - 64 + 26
    else:
        raise ValueError(f"invalid item: '{item}'")


def rucksacks_from_input(input_string):
    return [x for x in input_string.split("\n") if x != ""]


def sum_of_priorities(rucksacks):
    return sum([get_priority(find_erroneous_item(k)) for k in rucksacks])


def group_rucksacks(rucksacks):
    if len(rucksacks) % 3 != 0:
        raise ValueError(f"rucksacks count {len(rucksacks)} not divisible by 3")
    out = []
    i = 0
    while i < len(rucksacks):
        out.append(rucksacks[i:i+3])
        i += 3
    return out


def find_badge_type(rucksack_group):
    first, second, third = rucksack_group
    items_in_common = set.intersection(set(first), set(second), set(third))
    if len(items_in_common) == 1:
        return list(items_in_common)[0]
    else:
        raise ValueError(f"multiple items found in all rucksacks: {items_in_common}")


def sum_of_badge_priorities(rucksack_groups):
    return sum([get_priority(find_badge_type(rg)) for rg in rucksack_groups])


if __name__ == "__main__":
    input03 = open("../input/input03").read()

    rucksacks = rucksacks_from_input(input03)
    priority_total = sum_of_priorities(rucksacks)
    print(f"(p1 answer) sum of erroneous item priorities: {priority_total}") # 7967

    grouped_rucksacks = group_rucksacks(rucksacks)
    badge_priority_total = sum_of_badge_priorities(grouped_rucksacks)
    print(f"(p2 answer) sum of badge priorities: {badge_priority_total}") # 2716


####################################

SAMPLE_INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def test_split_compartments():
    rucksack = "vJrwpWtwJgWrhcsFMMfFFhFp"
    expected = ("vJrwpWtwJgWr", "hcsFMMfFFhFp")
    actual = split_compartments(rucksack)
    assert expected == actual


def test_find_erroneous_item():
    rucksack = "vJrwpWtwJgWrhcsFMMfFFhFp"
    expected = "p"
    actual = find_erroneous_item(rucksack)
    assert expected == actual


def test_get_priority():
    pairs = [
        ("p", 16),
        ("L", 38),
        ("P", 42),
        ("v", 22),
        ("t", 20),
        ("s", 19),
        ("a", 1),
        ("z", 26),
        ("A", 27),
        ("Z", 52),
    ]
    for item, expected in pairs:
        actual = get_priority(item)
        assert expected == actual


def test_rucksacks_from_input():
    expected = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    actual = rucksacks_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_sum_of_priorities():
    expected = 157
    actual = sum_of_priorities(rucksacks_from_input(SAMPLE_INPUT))
    assert expected == actual


def test_group_rucksacks():
    expected = [
        ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"],
        ["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"],
    ]
    actual = group_rucksacks(rucksacks_from_input(SAMPLE_INPUT))
    assert expected == actual


def test_find_badge_type():
    expected = "r"
    actual = find_badge_type(["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"])
    assert expected == actual

    expected = "Z"
    actual = find_badge_type(["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"])
    assert expected == actual


def test_sum_of_badge_priorities():
    expected = 70
    rucksacks = rucksacks_from_input(SAMPLE_INPUT)
    grouped_rucksacks = group_rucksacks(rucksacks)
    actual = sum_of_badge_priorities(grouped_rucksacks)
    assert expected == actual
