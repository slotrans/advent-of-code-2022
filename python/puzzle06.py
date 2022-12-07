# this is weird but it's the first technique that came to mind for some reason
def find_marker(stream):
    i = 4
    while i < len(stream):
        possible_marker = stream[i-4:i]
        if len(set(possible_marker)) == 4:
            return i
        i += 1

    raise ValueError("marker not found")


if __name__ == "__main__":
    input06 = open("../input/input06").read()

    marker_position = find_marker(input06)
    print(f"(p1 answer) marker position: {marker_position}") #
    

##########################################################

SAMPLE_INPUT_ONE = "mjqjpqmgbljsphdztnvjfqwrcgsmlb" # 7

ADDITIONAL_SAMPLE_INPUTS = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]


def test_find_marker_one():
    expected = 7
    actual = find_marker(SAMPLE_INPUT_ONE)
    assert expected == actual


def test_find_marker_addl():
    for stream, expected in ADDITIONAL_SAMPLE_INPUTS:
        actual = find_marker(stream)
        assert expected == actual
