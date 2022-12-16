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


def sensor_beacon_pairs_from_input(input_string):
    pairs = []

    for line in input_string.strip().split("\n"):
        sensor_part, beacon_part = line.split(": ")

        sensor_point = point_from_coord_string(sensor_part[10:])
        beacon_point = point_from_coord_string(beacon_part[21:])
        pairs.append((sensor_point, beacon_point))

    return pairs


def count_excluded_points_in_row(sensor_beacon_pairs, fixed_y):
    row_points = {}
    for sensor, beacon in sensor_beacon_pairs:
        print(f"checking S={sensor} B={beacon}")
        if sensor.y == fixed_y:
            row_points[sensor] = "S"
        if beacon.y == fixed_y:
            row_points[beacon] = "B"

        sensor_beacon_mdist = get_manhattan_distance(sensor, beacon)

        for x in range(sensor.x-sensor_beacon_mdist, sensor.x+sensor_beacon_mdist+1):
            p = Point(x=x, y=fixed_y)
            if get_manhattan_distance(p, sensor) <= sensor_beacon_mdist:
                row_points[p] = row_points.get(p, "#")

    #for k,v in sorted(row_points.items()):
    #    print(f"{k}={v}")

    return len([1 for k,v in row_points.items() if v in ["#", "S"]])


if __name__ == "__main__":
    input15 = open("../input/input15").read()

    sensor_beacon_pairs = sensor_beacon_pairs_from_input(input15)
    excluded_points = count_excluded_points_in_row(sensor_beacon_pairs, 2000000)
    print(f"(p1 answer) In the row where y=2000000, how many positions cannot contain a beacon? {excluded_points}") # 4502208


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


def test_sensor_beacon_pairs_from_input():
    expected = [
        (Point(x=2, y=18), Point(x=-2, y=15)),
        (Point(x=9, y=16), Point(x=10, y=16)),
        (Point(x=13, y=2), Point(x=15, y=3)),
        (Point(x=12, y=14), Point(x=10, y=16)),
        (Point(x=10, y=20), Point(x=10, y=16)),
        (Point(x=14, y=17), Point(x=10, y=16)),
        (Point(x=8, y=7), Point(x=2, y=10)),
        (Point(x=2, y=0), Point(x=2, y=10)),
        (Point(x=0, y=11), Point(x=2, y=10)),
        (Point(x=20, y=14), Point(x=25, y=17)),
        (Point(x=17, y=20), Point(x=21, y=22)),
        (Point(x=16, y=7), Point(x=15, y=3)),
        (Point(x=14, y=3), Point(x=15, y=3)),
        (Point(x=20, y=1), Point(x=15, y=3)),
    ]
    actual = sensor_beacon_pairs_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_count_excluded_points_in_row():
    expected = 26
    sensor_beacon_pairs = sensor_beacon_pairs_from_input(SAMPLE_INPUT)
    actual = count_excluded_points_in_row(sensor_beacon_pairs, 10)
    assert expected == actual
