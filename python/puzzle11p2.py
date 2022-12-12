# I don't usually make a separate file for part 2 but it seemed appropriate here


def parse_items(input_line):
    label, items = input_line.split(": ")
    return [int(x) for x in items.split(",")]


# this is not at all necessary but let's have some fun
def parse_operation_to_function(input_line):
    label, equation = input_line.split(": ")
    new, expression = input_line.split(" = ")
    parts = expression.split(" ")
    # parts will be e.g. ["old", "*", "19"] or ["old", "+", "old"]
    # first element is always "old"
    # second element is the operator
    # third element is either a literal or "old"
    operator = parts[1]
    last_element = parts[2]

    if last_element.isdigit():
        parsed_last_element = int(last_element)
        if operator == "*":
            return lambda old: old * parsed_last_element
        elif operator == "+":
            return lambda old: old + parsed_last_element
        else:
            raise ValueError(f"unexpected operator: {operator}")
    elif last_element == "old":
        if operator == "*":
            return lambda old: old * old
        elif operator == "+":
            return lambda old: old + old
        else:
            raise ValueError(f"unexpected operator: {operator}")
    else:
        raise ValueError(f"could not parse expression: {expression}")


def parse_divisibility_test(input_line):
    # "  Test: divisible by 23"
    label, expression = input_line.split(": ")
    junk, value = expression.split(" by ")
    return int(value)


def parse_target_monkey_map(input_line_true, input_line_false):
    # "    If true: throw to monkey 2"
    # "    If false: throw to monkey 3"
    true_target = int(input_line_true[29:])
    false_target = int(input_line_false[30:])
    return {True: true_target, False: false_target}


def parse_monkey(input_chunk):
    lines = input_chunk.split("\n")

    # Monkey 0:
    monkey_id = int(lines[0].rstrip(":")[7:])

    #   Starting items: 79, 98
    items = parse_items(lines[1])

    #   Operation: new = old * 19
    operation = parse_operation_to_function(lines[2])

    #   Test: divisible by 23
    divisibility_test_number = parse_divisibility_test(lines[3])

    #     If true: throw to monkey 2
    #     If false: throw to monkey 3
    target_monkey_map = parse_target_monkey_map(lines[4], lines[5])

    return {
        monkey_id: {
            "items": items,
            "operation": operation,
            "divisibility_test_number": divisibility_test_number,
            "target_monkey_map": target_monkey_map,
        }
    }


def parse_all_monkeys(input_string):
    chunks = input_string.strip().split("\n\n")
    out = {}
    for monkey in [parse_monkey(c) for c in chunks]:
        out.update(monkey)

    all_divisibility_test_numbers = set([m["divisibility_test_number"] for m in out.values()])

    for m in out.values():
        item_mod_maps = []
        for item in m["items"]:
            imm = {dtn: item % dtn for dtn in list(all_divisibility_test_numbers)}
            item_mod_maps.append(imm)
        m.pop("items")
        m["item_mod_maps"] = item_mod_maps

    return out


def play_round(state): # destructive!
    for this_monkey_id in sorted(state.keys()):
        active_monkey = state[this_monkey_id]
        while len(active_monkey["item_mod_maps"]) > 0:
            item_mod_map = active_monkey["item_mod_maps"].pop(0)

            for modulus_number, worry_level in list(item_mod_map.items()): # list() because we're going to mutate the map
                item_mod_map[modulus_number] = active_monkey["operation"](worry_level) % modulus_number

            divisibility_test_number = active_monkey["divisibility_test_number"]
            divisibility_check_result = item_mod_map[divisibility_test_number] == 0
            target_monkey_id = active_monkey["target_monkey_map"][divisibility_check_result]

            state[target_monkey_id]["item_mod_maps"].append(item_mod_map)

            active_monkey["inspections"] = active_monkey.get("inspections", 0) + 1


def get_monkey_business(state):
    inspection_counts = sorted([monkey["inspections"] for monkey in state.values()], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


if __name__ == "__main__":
    input11 = open("../input/input11").read()

    state = parse_all_monkeys(input11)
    for i in range(10000):
        play_round(state)
    monkey_business_after_10k = get_monkey_business(state)
    print(f"(p2 answer) what is the level of monkey business after 10000 rounds? {monkey_business_after_10k}") # 




####################################

SAMPLE_INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def test_parse_items():
    for input_line, expected in [
        ("  Starting items: 79, 98",         [79, 98]),
        ("  Starting items: 54, 65, 75, 74", [54, 65, 75, 74]),
        ("  Starting items: 79, 60, 97",     [79, 60, 97]),
        ("  Starting items: 74",             [74]),
    ]:
        actual = parse_items(input_line)
        assert expected == actual


def test_parse_operation_to_function():
    for input_line, expected in [
        ("  Operation: new = old * 19",  lambda x: x * 19),
        ("  Operation: new = old + 6",   lambda x: x + 6),
        ("  Operation: new = old * old", lambda x: x * x),
        ("  Operation: new = old + 3",   lambda x: x + 3),
    ]:
        for i in range(20): # idk test each function with a handful of values
            actual = parse_operation_to_function(input_line)
            assert expected(i) == actual(i)


def test_parse_divisibility_test():
    for input_line, expected in [
        ("  Test: divisible by 23", 23),
        ("  Test: divisible by 19", 19),
        ("  Test: divisible by 13", 13),
        ("  Test: divisible by 17", 17),
    ]:
        actual = parse_divisibility_test(input_line)
        assert expected == actual


def test_parse_target_monkey_map():
    for input_line1, input_line2, expected in [
        ("    If true: throw to monkey 2", "    If false: throw to monkey 3", {True: 2, False: 3}),
        ("    If true: throw to monkey 2", "    If false: throw to monkey 0", {True: 2, False: 0}),
        ("    If true: throw to monkey 1", "    If false: throw to monkey 3", {True: 1, False: 3}),
        ("    If true: throw to monkey 0", "    If false: throw to monkey 1", {True: 0, False: 1}),
    ]:
        actual = parse_target_monkey_map(input_line1, input_line2)
        assert expected == actual


def test_parse_monkey():
    expected = {
        0: {
            "items": [79, 98], 
            "operation": lambda x: x * 19,
            "divisibility_test_number": 23,
            "target_monkey_map": {
                True: 2,
                False: 3,
            }
        }
    }
    actual = parse_monkey(SAMPLE_INPUT.split("\n\n")[0])
    assert 0 in actual
    assert expected[0]["items"] == actual[0]["items"]
    assert expected[0]["operation"](17) == actual[0]["operation"](17)
    assert expected[0]["divisibility_test_number"] == actual[0]["divisibility_test_number"]
    assert expected[0]["target_monkey_map"] == actual[0]["target_monkey_map"]


def test_parse_all_monkeys():
    # half-hearted
    actual = parse_all_monkeys(SAMPLE_INPUT)
    assert {0, 1, 2, 3} == actual.keys()

    # can't test item_mod_maps at the individual monkey level
    assert actual[0]["item_mod_maps"] == [
        {23: 10, 19: 3, 13: 1, 17: 11}, # 79 % 23 -> 10, 79 % 19 -> 3, 79 % 13 -> 1, 79 % 17 -> 11
        {23: 6, 19: 3, 13: 7, 17: 13},
    ]

    # make sure every item mod map has every divisibility test number in it
    all_div_numbers = set([m["divisibility_test_number"] for m in actual.values()])
    for m in actual.values():
        for imm in m["item_mod_maps"]:
            assert all_div_numbers == set(imm.keys())


def test_play_rounds_inspect_counts():
    state = parse_all_monkeys(SAMPLE_INPUT)

    play_round(state)
    rounds = 1

    #== After round 1 ==
    assert state[0]["inspections"] == 2
    assert state[1]["inspections"] == 4
    assert state[2]["inspections"] == 3
    assert state[3]["inspections"] == 6

    while rounds < 20:
        play_round(state)
        rounds += 1

    #== After round 20 ==
    assert state[0]["inspections"] == 99
    assert state[1]["inspections"] == 97
    assert state[2]["inspections"] == 8
    assert state[3]["inspections"] == 103

    while rounds < 1000:
        play_round(state)
        rounds += 1

    #== After round 1000 ==
    assert state[0]["inspections"] == 5204
    assert state[1]["inspections"] == 4792
    assert state[2]["inspections"] == 199
    assert state[3]["inspections"] == 5192

    while rounds < 2000:
        play_round(state)
        rounds += 1

    #== After round 2000 ==
    assert state[0]["inspections"] == 10419
    assert state[1]["inspections"] == 9577
    assert state[2]["inspections"] == 392
    assert state[3]["inspections"] == 10391

    while rounds < 3000:
        play_round(state)
        rounds += 1

    #== After round 3000 ==
    assert state[0]["inspections"] == 15638
    assert state[1]["inspections"] == 14358
    assert state[2]["inspections"] == 587
    assert state[3]["inspections"] == 15593

    while rounds < 4000:
        play_round(state)
        rounds += 1

    #== After round 4000 ==
    assert state[0]["inspections"] == 20858
    assert state[1]["inspections"] == 19138
    assert state[2]["inspections"] == 780
    assert state[3]["inspections"] == 20797

    while rounds < 5000:
        play_round(state)
        rounds += 1

    #== After round 5000 ==
    assert state[0]["inspections"] == 26075
    assert state[1]["inspections"] == 23921
    assert state[2]["inspections"] == 974
    assert state[3]["inspections"] == 26000

    while rounds < 6000:
        play_round(state)
        rounds += 1

    #== After round 6000 ==
    assert state[0]["inspections"] == 31294
    assert state[1]["inspections"] == 28702
    assert state[2]["inspections"] == 1165
    assert state[3]["inspections"] == 31204

    while rounds < 7000:
        play_round(state)
        rounds += 1

    #== After round 7000 ==
    assert state[0]["inspections"] == 36508
    assert state[1]["inspections"] == 33488
    assert state[2]["inspections"] == 1360
    assert state[3]["inspections"] == 36400

    while rounds < 8000:
        play_round(state)
        rounds += 1

    #== After round 8000 ==
    assert state[0]["inspections"] == 41728
    assert state[1]["inspections"] == 38268
    assert state[2]["inspections"] == 1553
    assert state[3]["inspections"] == 41606

    while rounds < 9000:
        play_round(state)
        rounds += 1

    #== After round 9000 ==
    assert state[0]["inspections"] == 46945
    assert state[1]["inspections"] == 43051
    assert state[2]["inspections"] == 1746
    assert state[3]["inspections"] == 46807

    while rounds < 10000:
        play_round(state)
        rounds += 1

    #== After round 10000 ==
    assert state[0]["inspections"] == 52166
    assert state[1]["inspections"] == 47830
    assert state[2]["inspections"] == 1938
    assert state[3]["inspections"] == 52013


def test_get_monkey_business():
    state = parse_all_monkeys(SAMPLE_INPUT)

    for i in range(10000):
        play_round(state)

    expected = 2713310158
    actual = get_monkey_business(state)
    assert expected == actual
