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


def is_point_in_any_sensor_range(sensor_beacon_pairs, point):
    for sensor, beacon in sensor_beacon_pairs:
        sensor_beacon_mdist = get_manhattan_distance(sensor, beacon)
        sensor_point_mdist = get_manhattan_distance(sensor, point)
        if sensor_point_mdist <= sensor_beacon_mdist:
            return True

    return False


def points_just_outside_range(sensor, beacon):
    points = []

    sensor_beacon_mdist = get_manhattan_distance(sensor, beacon)
    target_distance = sensor_beacon_mdist + 1

    # W corner to N corner
    for i in range(-1*target_distance, 0):
        p = Point(x=sensor.x+i, y=sensor.y-(target_distance+i))
        points.append(p)
    # N corner to E corner
    for i in range(0, target_distance+1):
        p = Point(x=sensor.x+i, y=sensor.y-(target_distance-i))
        points.append(p)
    # E corner to S corner
    for i in range(target_distance, 0, -1):
        p = Point(x=sensor.x+i, y=sensor.y+(target_distance-i))
        points.append(p)
    # S corner to W corner
    for i in range(0, -1*target_distance-1, -1):
        p = Point(x=sensor.x+i, y=sensor.y+(target_distance+i))
        points.append(p)

    return points


def find_distress_beacon(sensor_beacon_pairs, min_coord, max_coord):
    candidate_points = set()
    for sensor, beacon in sensor_beacon_pairs:
        print(f"looking just beyond S={sensor} B={beacon}")
        candidate_points.update(points_just_outside_range(sensor, beacon))
        for p in list(candidate_points):
            if min(p.x, p.y) < min_coord or max(p.x, p.y) > max_coord: # idk how necessary this is
                candidate_points.discard(p)
            elif is_point_in_any_sensor_range(sensor_beacon_pairs, p):
                candidate_points.discard(p)

    if len(candidate_points) == 1:
        return candidate_points.pop()
    else:
        raise Exception(f"candidate_points length != 1: {candidate_points}")


if __name__ == "__main__":
    input15 = open("../input/input15").read()

    sensor_beacon_pairs = sensor_beacon_pairs_from_input(input15)
    #excluded_points = count_excluded_points_in_row(sensor_beacon_pairs, 2000000)
    #print(f"(p1 answer) In the row where y=2000000, how many positions cannot contain a beacon? {excluded_points}") # 4502208

    distress_beacon_location = find_distress_beacon(sensor_beacon_pairs, 0, 4000000)
    tuning_frequency = 4000000*distress_beacon_location.x + distress_beacon_location.y
    print(f"(p2 answer) What is the distress beacon's tuning frequency? {tuning_frequency}") # 13784551204480


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


def test_is_point_in_any_sensor_range():
    sensor_beacon_pairs = sensor_beacon_pairs_from_input(SAMPLE_INPUT)

    for point, expected in [
        (Point(13,10), True),
        (Point(13,11), True),
        (Point(13,12), True),
        (Point(14,10), True),
        (Point(14,11), False), # solution point for sample
        (Point(14,12), True),
        (Point(15,10), True),
        (Point(15,11), True),
        (Point(15,12), True),
    ]:
        actual = is_point_in_any_sensor_range(sensor_beacon_pairs, point)
        assert expected == actual


def test_points_just_outside_range():
    sensor = Point(0, 0)
    beacon = Point(0, 2)
    expected = [
        Point(0, -3),
        Point(1, -2),
        Point(2, -1),
        Point(3, 0),
        Point(2, 1),
        Point(1, 2),
        Point(0, 3),
        Point(-1, 2),
        Point(-2, 1),
        Point(-3, 0),
        Point(-2, -1),
        Point(-1, -2),
    ]
    actual = points_just_outside_range(sensor, beacon)
    assert set(expected) == set(actual)


def test_find_distress_beacon():
    expected = Point(x=14, y=11)
    sensor_beacon_pairs = sensor_beacon_pairs_from_input(SAMPLE_INPUT)
    actual = find_distress_beacon(sensor_beacon_pairs, 0, 20)
    assert expected == actual
