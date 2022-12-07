# this is weird but it's the first technique that came to mind for some reason
def find_start_of_packet_marker(stream):
    i = 4
    while i < len(stream):
        possible_marker = stream[i-4:i]
        if len(set(possible_marker)) == 4:
            return i
        i += 1

    raise ValueError("marker not found")


def find_start_of_message_marker(stream):
    i = 14
    while i < len(stream):
        possible_marker = stream[i-14:i]
        if len(set(possible_marker)) == 14:
            return i
        i += 1

    raise ValueError("marker not found")


if __name__ == "__main__":
    input06 = open("../input/input06").read()

    packet_marker_position = find_start_of_packet_marker(input06)
    print(f"(p1 answer) packet marker position: {packet_marker_position}") # 1598

    message_marker_position = find_start_of_message_marker(input06)
    print(f"(p1 answer) message marker position: {message_marker_position}") # 1598


##########################################################

SAMPLE_INPUT_ONE = "mjqjpqmgbljsphdztnvjfqwrcgsmlb" # 7

ADDITIONAL_SAMPLE_INPUTS = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]

P2_SAMPLE_INPUTS = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
]


def test_find_start_of_packet_marker_one():
    expected = 7
    actual = find_start_of_packet_marker(SAMPLE_INPUT_ONE)
    assert expected == actual


def test_find_start_of_packet_marker_addl():
    for stream, expected in ADDITIONAL_SAMPLE_INPUTS:
        actual = find_start_of_packet_marker(stream)
        assert expected == actual


def test_find_start_of_message_marker():
    for stream, expected in P2_SAMPLE_INPUTS:
        actual = find_start_of_message_marker(stream)
        assert expected == actual
