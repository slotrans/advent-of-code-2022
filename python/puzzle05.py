from collections import namedtuple

Command = namedtuple("Command", ["move_crates", "from_stack", "to_stack"])


def parse_input(input_string):
    stack_part, command_part = input_string.split("\n\n")

    stacks = parse_stacks(stack_part)
    commands = parse_commands(command_part)

    return (stacks, commands)


def parse_stacks(stack_string):
    lines = stack_string.rstrip().split("\n")
    num_stacks = max([int(x) for x in lines[-1].split(" ") if x.isdigit()])

    stacks = {n: [] for n in range(1, num_stacks+1)}

    for line in list(reversed(lines))[1:]:
        for i in range(num_stacks):
            letter = line[1+(4*i):2+(4*i)]
            if "A" <= letter <= "Z":
                stacks[i+1].append(letter)

    return stacks


def parse_commands(command_string):
    out = []
    for line in command_string.strip().split("\n"):
        pieces = line.split(" ")
        move_crates = int(pieces[1])
        from_stack = int(pieces[3])
        to_stack = int(pieces[5])
        out.append(Command(move_crates, from_stack, to_stack))
    return out


def run_commands_destructively_p1(stacks, commands):
    for cmd in commands:
        for _ in range(cmd.move_crates):
            crate = stacks[cmd.from_stack].pop()
            stacks[cmd.to_stack].append(crate)


def run_commands_destructively_p2(stacks, commands):
    for cmd in commands:
        crates_to_move_together = stacks[cmd.from_stack][(-1*cmd.move_crates):]
        for _ in range(cmd.move_crates):
            stacks[cmd.from_stack].pop()
        stacks[cmd.to_stack] += crates_to_move_together


def crates_on_top(stacks):
    crates = []
    for k in sorted(stacks.keys()):
        crates.append(stacks[k][-1])
    return "".join(crates)


if __name__ == "__main__":
    input05 = open("../input/input05").read()

    stacks, commands = parse_input(input05)
    run_commands_destructively_p1(stacks, commands)
    p1_answer = crates_on_top(stacks)
    print(f"(p1 answer) crates on top spell: {p1_answer}") # QGTHFZBHV

    stacks, commands = parse_input(input05)
    run_commands_destructively_p2(stacks, commands)
    p2_answer = crates_on_top(stacks)
    print(f"(p2 answer) crates on top spell: {p2_answer}") # MGDMPSZTM



#########################################

SAMPLE_INPUT = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def test_parse_command_string():
    expected = [
        Command(1, 2, 1),
        Command(3, 1, 3),
        Command(2, 2, 1),
        Command(1, 1, 2),
    ]
    actual = parse_commands("""\
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2    
    """)
    print(actual)
    assert expected == actual


def test_parse_stacks():
    expected = {
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }
    actual = parse_stacks("""\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3         
    """)
    print(actual)
    assert expected == actual


def test_parse_input():
    expected_stacks = {
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }
    expected_commands = [
        Command(1, 2, 1),
        Command(3, 1, 3),
        Command(2, 2, 1),
        Command(1, 1, 2),
    ]
    actual_stacks, actual_commands = parse_input(SAMPLE_INPUT)
    assert expected_stacks == actual_stacks
    assert expected_commands == actual_commands


def test_run_commands_destructively_p1():
    stacks = {
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }
    commands = [
        Command(1, 2, 1),
        Command(3, 1, 3),
        Command(2, 2, 1),
        Command(1, 1, 2),
    ]
    expected = {
        1: ["C"],
        2: ["M"],
        3: ["P", "D", "N", "Z"],        
    }
    run_commands_destructively_p1(stacks, commands)
    print(stacks)
    assert expected == stacks


def test_run_commands_destructively_p2():
    stacks = {
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }
    commands = [
        Command(1, 2, 1),
        Command(3, 1, 3),
        Command(2, 2, 1),
        Command(1, 1, 2),
    ]
    expected = {
        1: ["M"],
        2: ["C"],
        3: ["P", "Z", "N", "D"],        
    }
    run_commands_destructively_p2(stacks, commands)
    print(stacks)
    assert expected == stacks    


def test_crates_on_top():
    stacks = {
        1: ["C"],
        2: ["M"],
        3: ["P", "D", "N", "Z"],
    }
    expected = "CMZ"
    actual = crates_on_top(stacks)
    assert expected == actual