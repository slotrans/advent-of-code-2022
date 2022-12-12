
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
    return out


def play_round(state): # destructive!
    for this_monkey_id in sorted(state.keys()):
        active_monkey = state[this_monkey_id]
        while len(active_monkey["items"]) > 0:
            initial_worry_level = active_monkey["items"].pop(0)

            worry_after_inspection = active_monkey["operation"](initial_worry_level)
            worry_after_boredom = worry_after_inspection // 3
            divisibility_check_result = worry_after_boredom % active_monkey["divisibility_test_number"] == 0
            target_monkey_id = active_monkey["target_monkey_map"][divisibility_check_result]

            state[target_monkey_id]["items"].append(worry_after_boredom)

            active_monkey["inspections"] = active_monkey.get("inspections", 0) + 1


def get_monkey_business(state):
    inspection_counts = sorted([monkey["inspections"] for monkey in state.values()], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


if __name__ == "__main__":
    input11 = open("../input/input11").read()

    state = parse_all_monkeys(input11)
    for i in range(20):
        play_round(state)
    monkey_business_after_20 = get_monkey_business(state)
    print(f"(p1 answer) What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans? {monkey_business_after_20}") # 56120

    


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


def test_play_round_state_checks():
    state = parse_all_monkeys(SAMPLE_INPUT)
    
    play_round(state)
    assert [20, 23, 27, 26] == state[0]["items"]
    assert [2080, 25, 167, 207, 401, 1046] == state[1]["items"]
    assert [] == state[2]["items"]
    assert [] == state[3]["items"]

    play_round(state)
    assert [695, 10, 71, 135, 350] == state[0]["items"]
    assert [43, 49, 58, 55, 362] == state[1]["items"]
    assert [] == state[2]["items"]
    assert [] == state[3]["items"]

    play_round(state)
    assert [16, 18, 21, 20, 122] == state[0]["items"]
    assert [1468, 22, 150, 286, 739] == state[1]["items"]
    assert [] == state[2]["items"]
    assert [] == state[3]["items"]

    # 3 rounds is probably enough


def test_play_rounds_inspect_counts():
    state = parse_all_monkeys(SAMPLE_INPUT)

    for i in range(20):
        play_round(state)

    assert 101 == state[0]["inspections"]
    assert 95  == state[1]["inspections"]
    assert 7   == state[2]["inspections"]
    assert 105 == state[3]["inspections"]


def test_get_monkey_business():
    state = parse_all_monkeys(SAMPLE_INPUT)

    for i in range(20):
        play_round(state)

    expected = 10605
    actual = get_monkey_business(state)
    assert expected == actual
