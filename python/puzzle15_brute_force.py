from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def point_from_coord_string(input_string):
    # "x=2, y=18"
    x_part, y_part = input_string.split(", ")
    x_part = x_part.split("=")[1]
    y_part = y_part.split("=")[1]
    return Point(x=int(x_part), y=int(y_part))


def get_manhattan_distance(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


def points_within_manhattan_distance(center, distance):
    out = []
    for dx in range(-1*distance, distance+1):
        for dy in range(-1*distance, distance+1):
            if abs(dx)+abs(dy) > distance or (dx == 0 and dy == 0):
                # there's probably a smarter looping strategy but let's see if the dumb way is fast enough
                continue
            out.append(Point(x=center.x+dx, y=center.y+dy))
    return out


def sparse_grid_from_input(input_string):
    grid = {}
    
    for line in input_string.strip().split("\n"):
        sensor_part, beacon_part = line.split(": ")

        sensor_point = point_from_coord_string(sensor_part[10:])
        beacon_point = point_from_coord_string(beacon_part[21:])
        manhattan_distance = get_manhattan_distance(sensor_point, beacon_point)

        nope_points = points_within_manhattan_distance(sensor_point, manhattan_distance)
        for p in nope_points:
            grid[p] = grid.get(p, "#") # avoid overwriting

        grid[sensor_point] = "S"
        grid[beacon_point] = "B"

    return grid


if __name__ == "__main__":
    input15 = open("../input/input15").read()

    grid = sparse_grid_from_input(input15)
    excluded_points = 0
    for point, contents in grid.items():
        if point.y == 2000000:
            if contents in ["#", "S"]:
                excluded_points += 1
    print(f"(p1 answer) In the row where y=2000000, how many positions cannot contain a beacon? {excluded_points}")

    # too slow...


##############################

SAMPLE_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def test_point_from_coord_string():
    for input_string, expected in [
        ("x=2, y=18", Point(2, 18)),
        ("x=9, y=16", Point(9, 16)),
        ("x=13, y=2", Point(13, 2)),
        ("x=-2, y=15", Point(-2,15)),
        ("x=10, y=16", Point(10,16)),
        ("x=15, y=3", Point(15,3)),
    ]:
        actual = point_from_coord_string(input_string)
        assert expected == actual


def test_points_within_manhattan_distance():
    expected = [
        Point(-3,0),
        Point(-2,-1),
        Point(-2,0),
        Point(-2,1),
        Point(-1,-2),
        Point(-1,-1),
        Point(-1,0),
        Point(-1,1),
        Point(-1,2),
        Point(0,-3),
        Point(0,-2),
        Point(0,-1),
        Point(0,1),
        Point(0,2),
        Point(0,3),
        Point(1,-2),
        Point(1,-1),
        Point(1,0),
        Point(1,1),
        Point(1,2),
        Point(2,-1),
        Point(2,0),
        Point(2,1),
        Point(3,0),
    ]
    actual = points_within_manhattan_distance(Point(0,0), 3)
    print(actual)
    assert set(expected) == set(actual)


def test_sparse_grid_from_input():
    expected_sensors_and_beacons = {
        Point(x=2, y=18): "S",
        Point(x=9, y=16): "S",
        Point(x=13, y=2): "S",
        Point(x=12, y=14): "S",
        Point(x=10, y=20): "S",
        Point(x=14, y=17): "S",
        Point(x=8, y=7): "S",
        Point(x=2, y=0): "S",
        Point(x=0, y=11): "S",
        Point(x=20, y=14): "S",
        Point(x=17, y=20): "S",
        Point(x=16, y=7): "S",
        Point(x=14, y=3): "S",
        Point(x=20, y=1): "S",
        #
        Point(x=-2, y=15): "B",
        Point(x=10, y=16): "B",
        Point(x=15, y=3): "B",
        Point(x=10, y=16): "B",
        Point(x=10, y=16): "B",
        Point(x=10, y=16): "B",
        Point(x=2, y=10): "B",
        Point(x=2, y=10): "B",
        Point(x=2, y=10): "B",
        Point(x=25, y=17): "B",
        Point(x=21, y=22): "B",
        Point(x=15, y=3): "B",
        Point(x=15, y=3): "B",
        Point(x=15, y=3): "B",
    }
    actual = sparse_grid_from_input(SAMPLE_INPUT)
    for point, contents in expected_sensors_and_beacons.items():
        assert contents == actual[point]


def test_sample():
    grid = sparse_grid_from_input(SAMPLE_INPUT)

    expected = 26
    actual = 0
    for point, contents in grid.items():
        if point.y == 10:
            if contents in ["#", "S"]:
                actual += 1
    assert expected == actual
