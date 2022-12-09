from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
# X,Y coordinates, lower-left origin


def movements_from_input(input_string):
    out = []
    for line in input_string.strip().split("\n"):
        direction, units = line.split(" ")
        out.append((direction, int(units)))
    return out


def move_head(current, direction):
    if "U" == direction:
        return Point(x=current.x, y=current.y+1)
    elif "D" == direction:
        return Point(x=current.x, y=current.y-1)
    elif "L" == direction:
        return Point(x=current.x-1, y=current.y)
    elif "R" == direction:
        return Point(x=current.x+1, y=current.y)
    else:
        raise ValueError(f"invalid direction: {direction}")


def move_tail(head, tail):
    if -1 <= (tail.y - head.y) <= 1 and -1 <= (tail.x - head.x) <= 1:
        # head and tail are already "touching"
        return tail

    if tail.y < head.y:
        dy = 1
    elif tail.y > head.y:
        dy = -1
    else:
        dy = 0

    if tail.x < head.x:
        dx = 1
    elif tail.x > head.x:
        dx = -1
    else:
        dx = 0

    return Point(x=tail.x+dx, y=tail.y+dy)


def find_points_visited_by_tail(movements):
    head = Point(x=0, y=0)
    tail = Point(x=0, y=0)
    visited_by_tail = {tail}
    for direction, units in movements:
        for i in range(units):
            head = move_head(head, direction)
            tail = move_tail(head, tail)
            visited_by_tail.add(tail)
    return visited_by_tail


if __name__ == "__main__":
    input09 = open("../input/input09").read()

    movements = movements_from_input(input09)
    points_visited_by_tail = len(find_points_visited_by_tail(movements))
    print(f"(p1 answer) How many positions does the tail of the rope visit at least once? {points_visited_by_tail}") # 6030


##############################

SAMPLE_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


def test_movements_from_input():
    expected = [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]
    actual = movements_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_move_head():
    assert Point(x=0, y=1)  == move_head(Point(x=0, y=0), "U")
    assert Point(x=0, y=-1) == move_head(Point(x=0, y=0), "D")
    assert Point(x=-1, y=0) == move_head(Point(x=0, y=0), "L")
    assert Point(x=1, y=0)  == move_head(Point(x=0, y=0), "R")


def test_move_tail():
    # straight examples
    assert Point(x=2, y=1) == move_tail(head=Point(x=3, y=1), tail=Point(x=1, y=1))
    assert Point(x=1, y=2) == move_tail(head=Point(x=1, y=1), tail=Point(x=1, y=3))
    # diagonal examples
    assert Point(x=2, y=2) == move_tail(head=Point(x=3, y=2), tail=Point(x=1, y=1))
    assert Point(x=2, y=2) == move_tail(head=Point(x=3, y=2), tail=Point(x=1, y=1))
    # trival no-move example
    assert Point(x=0, y=0 == move_tail(head=Point(x=0, y=0), tail=Point(x=0, y=0)))


def test_find_points_visited_by_tail():
    expected = set([
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=0),
        Point(x=3, y=0),
        #
        Point(x=4, y=1),
        #
        Point(x=1, y=2),
        Point(x=2, y=2),
        Point(x=3, y=2),
        Point(x=4, y=2),
        #
        Point(x=3, y=3),
        Point(x=4, y=3),
        #
        Point(x=2, y=4),
        Point(x=3, y=4),
    ])
    actual = find_points_visited_by_tail(movements_from_input(SAMPLE_INPUT))
    assert expected == actual
