import functools


def packet_pairs_from_input(input_string):
    pairs = []
    for pair_chunk in input_string.strip().split("\n\n"):
        left_string, right_string = pair_chunk.split("\n")
        left, right = eval(left_string), eval(right_string) # that's right, eval()! suck it!
        pairs.append((left, right))
    return pairs


def are_packets_correctly_ordered(left, right):
    i = 0
    lvalue_present = False
    rvalue_present = False
    while True:
        try:
            lvalue = left[i]
            lvalue_present = True
        except IndexError:
            lvalue_present = False

        try:
            rvalue = right[i]
            rvalue_present = True
        except IndexError:
            rvalue_present = False

        if lvalue_present == False and rvalue_present == False:
            return None
        if lvalue_present == False:
            return True
        if rvalue_present == False:
            return False

        #print(f"comparing: {lvalue} vs {rvalue}")
        if type(lvalue) == int and type(rvalue) == int:
            if lvalue == rvalue:
                pass # "Otherwise, the inputs are the same integer; continue checking the next part of the input."
            else:
                return lvalue < rvalue
        elif type(lvalue) == list and type(rvalue) == list:
            res = are_packets_correctly_ordered(lvalue, rvalue)
            if res is not None:
                return res
        elif type(lvalue) == int and type(rvalue) == list:
            lvalue = [lvalue]
            res = are_packets_correctly_ordered(lvalue, rvalue)
            if res is not None:
                return res
        elif type(lvalue) == list and type(rvalue) == int:
            rvalue = [rvalue]
            res = are_packets_correctly_ordered(lvalue, rvalue)
            if res is not None:
                return res
        else:
            raise Exception("unreachable")

        i += 1


def indices_of_correctly_ordered_pairs(pair_list):
    indices = []
    for i, pair in enumerate(pair_list):
        left, right = pair
        if are_packets_correctly_ordered(left, right):
            indices.append(i+1) # "The first pair has index 1"
    return indices


# https://docs.python.org/3/library/functools.html#functools.cmp_to_key
def cmp_func(left, right):
    res = are_packets_correctly_ordered(left, right)
    if res == True:
        return -1
    if res == False:
        return 1
    else:
        return 0


def all_packets_from_input(input_string):
    packets = []
    for pair_chunk in input_string.strip().split("\n\n"):
        left_string, right_string = pair_chunk.split("\n")
        left, right = eval(left_string), eval(right_string) # that's right, eval()! suck it!
        packets.append(left)
        packets.append(right)
    return packets


def sort_packets(packets):
    return sorted(packets, key=functools.cmp_to_key(cmp_func))


if __name__ == "__main__":
    input13 = open("../input/input13").read()

    pairs = packet_pairs_from_input(input13)
    indices = indices_of_correctly_ordered_pairs(pairs)
    p1_answer = sum(indices)
    print(f"(p1 answer) What is the sum of the indices of those pairs? {p1_answer}") # 4809

    all_packets = all_packets_from_input(input13)
    all_packets.append( [[2]] )
    all_packets.append( [[6]] )
    sorted_packets_with_dividers = sort_packets(all_packets)
    index_of_2 = sorted_packets_with_dividers.index( [[2]] ) + 1 # "The first packet is at index 1..."
    index_of_6 = sorted_packets_with_dividers.index( [[6]] ) + 1
    decoder_key = index_of_2 * index_of_6
    print(f"(p2 answer) What is the decoder key for the distress signal? {decoder_key}") # 22600
    

############################

SAMPLE_INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def test_packet_pairs_from_input():
    expected = [
        ( [1,1,3,1,1], [1,1,5,1,1] ),
        ( [[1],[2,3,4]], [[1],4] ),
        ( [9], [[8,7,6]] ),
        ( [[4,4],4,4], [[4,4],4,4,4] ),
        ( [7,7,7,7], [7,7,7] ),
        ( [], [3] ),
        ( [[[]]], [[]] ),
        ( [1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9] ),
    ]
    actual = packet_pairs_from_input(SAMPLE_INPUT)
    print(actual)
    assert expected == actual


def test_are_packets_correctly_ordered():
    expected_outcomes = [True, True, False, True, False, True, False, False]
    i = 1
    for pair, expected in zip(packet_pairs_from_input(SAMPLE_INPUT), expected_outcomes):
        print(f"{i}: ", end="")

        left, right = pair
        actual = are_packets_correctly_ordered(left, right)

        print(f"left={left} / right={right} : actual={actual}")
        assert expected == actual
        
        i += 1


def test_indices_of_correctly_ordered_pairs():
    expected = [1, 2, 4, 6]
    actual = indices_of_correctly_ordered_pairs(packet_pairs_from_input(SAMPLE_INPUT))
    assert expected == actual


def test_all_packets_from_input():
    expected = [
        [1,1,3,1,1],
        [1,1,5,1,1],
        [[1],[2,3,4]],
        [[1],4],
        [9],
        [[8,7,6]],
        [[4,4],4,4],
        [[4,4],4,4,4],
        [7,7,7,7],
        [7,7,7],
        [],
        [3],
        [[[]]],
        [[]],
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
    ]
    actual = all_packets_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_sort_packets():
    expected = [
        [],
        [[]],
        [[[]]],
        [1,1,3,1,1],
        [1,1,5,1,1],
        [[1],[2,3,4]],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [[1],4],
        [[2]],
        [3],
        [[4,4],4,4],
        [[4,4],4,4,4],
        [[6]],
        [7,7,7],
        [7,7,7,7],
        [[8,7,6]],
        [9],
    ]
    packets = all_packets_from_input(SAMPLE_INPUT)
    packets.append( [[2]] )
    packets.append( [[6]] )
    actual = sort_packets(packets)
    assert expected == actual
