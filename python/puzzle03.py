
def split_compartments(knapsack):
    halfway = len(knapsack) // 2
    return (knapsack[:halfway], knapsack[halfway:])


def find_erroneous_item(knapsack):
    first_half, second_half = split_compartments(knapsack)
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


def knapsacks_from_input(input_string):
    return [x for x in input_string.split("\n") if x != ""]


def sum_of_priorities(knapsacks):
    return sum([get_priority(find_erroneous_item(k)) for k in knapsacks])


if __name__ == "__main__":
    input03 = open("../input/input03").read()

    knapsacks = knapsacks_from_input(input03)
    priority_total = sum_of_priorities(knapsacks)
    print(f"(p1 answer) sum of priorities: {priority_total}") # 7967


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
    knapsack = "vJrwpWtwJgWrhcsFMMfFFhFp"
    expected = ("vJrwpWtwJgWr", "hcsFMMfFFhFp")
    actual = split_compartments(knapsack)
    assert expected == actual


def test_find_erroneous_item():
    knapsack = "vJrwpWtwJgWrhcsFMMfFFhFp"
    expected = "p"
    actual = find_erroneous_item(knapsack)
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


def test_knapsacks_from_input():
    expected = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    actual = knapsacks_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_sum_of_priorities():
    expected = 157
    actual = sum_of_priorities(knapsacks_from_input(SAMPLE_INPUT))
    assert expected == actual
