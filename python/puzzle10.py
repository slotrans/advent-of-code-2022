
def instructions_from_input(input_string):
    out = []
    for line in input_string.strip().split("\n"):
        if line == "noop":
            out.append(("noop", 0))
        else:
            op, v = line.split(" ")
            out.append((op, int(v)))
    return out


def increment_cycle(current_cycle, x, reports): # mutating an argument! gross!
    FIRST_REPORT_AT = 20
    REPORT_INTERVAL = 40

    out_cycle = current_cycle + 1
    if out_cycle == FIRST_REPORT_AT or (out_cycle - FIRST_REPORT_AT) % REPORT_INTERVAL == 0:
        reports.append(out_cycle * x)

    return out_cycle


def increment_cycle2(current_cycle, x, line_buffer, screen): # again: gross
    SCREEN_WIDTH = 40

    out_cycle = current_cycle + 1
    x_position = (out_cycle - 1) % SCREEN_WIDTH
    if x-1 <= x_position <= x+1: # 3 pixels covered by the sprite
        line_buffer[x_position] = "#"

    if out_cycle % SCREEN_WIDTH == 0:
        screen.append("".join(line_buffer))
        for i in range(len(line_buffer)):
            line_buffer[i] = "."

    return out_cycle


def run_and_report_signal_strengths(instruction_list):
    x = 1
    cycle = 0
    signal_strength_reports = []
    for instruction in instruction_list:
        if instruction[0] == "noop":
            cycle = increment_cycle(cycle, x, signal_strength_reports)
        elif instruction[0] == "addx":
            cycle = increment_cycle(cycle, x, signal_strength_reports)
            cycle = increment_cycle(cycle, x, signal_strength_reports)
            
            v = instruction[1]
            x = x + v

    return signal_strength_reports


def render_instructions(instruction_list):
    screen = []
    line_buffer = list("." * 40)
    x = 1
    cycle = 0
    for instruction in instruction_list:
        if instruction[0] == "noop":
            cycle = increment_cycle2(cycle, x, line_buffer, screen)
        elif instruction[0] == "addx":
            cycle = increment_cycle2(cycle, x, line_buffer, screen)
            cycle = increment_cycle2(cycle, x, line_buffer, screen)

            v = instruction[1]
            x = x + v

    out = ""
    for line in screen:
        out += line + "\n"
    return out


if __name__ == "__main__":
    input10 = open("../input/input10").read()

    instructions = instructions_from_input(input10)
    signal_strength_reports = run_and_report_signal_strengths(instructions)
    sum_of_signal_strengths = sum(signal_strength_reports)
    print(f"(p1 answer) sum of signal strength reports: {sum_of_signal_strengths}") # 11820

    rendered_screen = render_instructions(instructions)
    print(f"(p2 answer found in the following...) What eight capital letters appear on your CRT?")
    print(rendered_screen) # EPJBRKAH


####################################

SMALL_SAMPLE_INPUT = """\
noop
addx 3
addx -5
"""

LARGE_SAMPLE_INPUT = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def test_instructions_from_input():
    expected = [
        ("noop", 0),
        ("addx", 3),
        ("addx", -5),
    ]
    actual = instructions_from_input(SMALL_SAMPLE_INPUT)
    assert expected == actual


def test_run_and_report_signal_strengths():
    expected = [
        420,
        1140,
        1800,
        2940,
        2880,
        3960
    ]
    actual = run_and_report_signal_strengths(instructions_from_input(LARGE_SAMPLE_INPUT))
    assert expected == actual


def test_increment_cycle_at_1():
    cycle = 1
    x = 1
    reports = []
    cycle = increment_cycle(cycle, x, reports)
    assert 2 == cycle
    assert 1 == x
    assert [] == reports


def test_increment_cycle_at_19():
    cycle = 19
    x = 1
    reports = []
    cycle = increment_cycle(cycle, x, reports)
    assert 20 == cycle
    assert 1 == x
    assert [20] == reports


def test_increment_cycle_at_59():
    cycle = 59
    x = 1
    reports = [20]
    cycle = increment_cycle(cycle, x, reports)
    assert 60 == cycle
    assert 1 == x
    assert [20, 60] == reports


def test_render_instructions():
    expected = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
    actual = render_instructions(instructions_from_input(LARGE_SAMPLE_INPUT))
    print(actual)
    assert expected == actual
