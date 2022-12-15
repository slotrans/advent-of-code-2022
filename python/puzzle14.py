from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def points_on_line_segment(p1, p2):
    if p1.x == p2.x:
        if p1.y < p2.y:
            return set([Point(x=p1.x, y=p1.y+dy) for dy in range(1 + p2.y - p1.y)])
        else:
            return set([Point(x=p1.x, y=p2.y+dy) for dy in range(1 + p1.y - p2.y)])
    elif p1.y == p2.y:
        if p1.x < p2.x:
            return set([Point(x=p1.x+dx, y=p1.y) for dx in range(1 + p2.x - p1.x)])
        else:
            return set([Point(x=p2.x+dx, y=p1.y) for dx in range(1 + p1.x - p2.x)])
    else:
        raise ValueError("only horizontal and vertical lines supported")


def sparse_grid_from_input(input_string):
    grid = {}

    lines = input_string.strip().split("\n")
    for line in lines:
        points = []
        point_strings = line.split(" -> ")
        for ps in point_strings:
            x_string, y_string = ps.split(",")
            points.append(Point(x=int(x_string), y=int(y_string)))

        for one, two in zip(points[:-1], points[1:]):
            grid.update({p: "#" for p in list(points_on_line_segment(one, two))})

    return grid


def move_sand(sand_point, grid) -> Point:
    down = Point(sand_point.x, sand_point.y+1)
    if grid.get(down) is None:
        return down

    down_left = Point(sand_point.x-1, sand_point.y+1)
    if grid.get(down_left) is None:
        return down_left

    down_right = Point(sand_point.x+1, sand_point.y+1)
    if grid.get(down_right) is None:
        return down_right

    return sand_point


def simulate_sand_flow_p1(grid): # destructive!
    SAND_ORIGIN = Point(x=500, y=0)
    LOWEST_ROCK_POINT = max([p.y for p in grid.keys()]) # Y-axis grows down so larger Y values are "lower" w/r/t gravity

    while True: # each sand unit
        falling_sand = SAND_ORIGIN

        while True: # each movement of a sand unit
            new_sand_point = move_sand(falling_sand, grid)

            if new_sand_point == falling_sand:
                # sand came to rest
                grid[new_sand_point] = "o"
                break

            if new_sand_point.y > LOWEST_ROCK_POINT:
                # sand has reached the abyss
                return

            falling_sand = new_sand_point


def simulate_sand_flow_p2(grid): # destructive!
    SAND_ORIGIN = Point(x=500, y=0)
    FLOOR_LEVEL = 2 + max([p.y for p in grid.keys()]) # Y-axis grows down so larger Y values are "lower" w/r/t gravity

    # add the floor, it doesn't actually need to be infinitely wide, adding the height of the grid on either side will do
    leftmost = min([p.x for p in grid.keys()])
    rightmost = max([p.x for p in grid.keys()])
    height = max([p.y for p in grid.keys()])
    for floor_x in range(leftmost-height, rightmost+height+1):
        grid[Point(x=floor_x, y=FLOOR_LEVEL)] = "#"

    while True: # each sand unit
        falling_sand = SAND_ORIGIN

        while True: # each movement of a sand unit
            new_sand_point = move_sand(falling_sand, grid)

            if new_sand_point == falling_sand:
                # sand came to rest
                grid[new_sand_point] = "o"
                if new_sand_point == SAND_ORIGIN:
                    return
                else:
                    break

            if new_sand_point.y >= FLOOR_LEVEL:
                # woops
                raise Exception(f"sand fell below the floor at {new_sand_point}, you have a bug")

            falling_sand = new_sand_point        


def print_grid(grid):
    leftmost = min([p.x for p in grid.keys()])
    rightmost = max([p.x for p in grid.keys()])
    height = max([p.y for p in grid.keys()])

    for y in range(0, height+1):
        line = "".join([grid.get(Point(x,y), ".") for x in range(leftmost, rightmost+1)])
        print(line)


if __name__ == "__main__":
    input14 = open("../input/input14").read()

    grid = sparse_grid_from_input(input14)
    simulate_sand_flow_p1(grid)
    sand_units = len([1 for k,v in grid.items() if v == "o"])
    print(f"(p1 answer) How many units of sand come to rest before sand starts flowing into the abyss below? {sand_units}") # 1298

    grid = sparse_grid_from_input(input14)
    simulate_sand_flow_p2(grid)
    sand_units = len([1 for k,v in grid.items() if v == "o"])
    print(f"(p2 answer) How many units of sand come to rest before sand starts flowing into the abyss below? {sand_units}") # 25585



##########################

SAMPLE_INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def test_points_on_line_segment_horizontal():
    expected = set([Point(498,4), Point(498,5), Point(498,6)])
    actual = points_on_line_segment(Point(498,4), Point(498,6))
    print(actual)
    assert expected == actual


def test_points_on_line_segment_vertical():
    expected = set([Point(498,6), Point(497,6), Point(496,6)])
    actual = points_on_line_segment(Point(498,6), Point(496,6))
    print(actual)
    assert expected == actual


def test_sparse_grid_from_input():
    expected = {
        Point(498,4): "#",
        Point(498,5): "#",
        Point(498,6): "#",
        Point(497,6): "#",
        Point(496,6): "#",
        Point(503,4): "#",
        Point(502,4): "#",
        Point(502,5): "#",
        Point(502,6): "#",
        Point(502,7): "#",
        Point(502,8): "#",
        Point(502,9): "#",
        Point(501,9): "#",
        Point(500,9): "#",
        Point(499,9): "#",
        Point(498,9): "#",
        Point(497,9): "#",
        Point(496,9): "#",
        Point(495,9): "#",
        Point(494,9): "#",
    }
    actual = sparse_grid_from_input(SAMPLE_INPUT)
    print(actual)
    assert expected == actual


def test_simulate_sand_flow_p1():
    expected = {
        Point(498,4): "#",
        Point(498,5): "#",
        Point(498,6): "#",
        Point(497,6): "#",
        Point(496,6): "#",
        Point(503,4): "#",
        Point(502,4): "#",
        Point(502,5): "#",
        Point(502,6): "#",
        Point(502,7): "#",
        Point(502,8): "#",
        Point(502,9): "#",
        Point(501,9): "#",
        Point(500,9): "#",
        Point(499,9): "#",
        Point(498,9): "#",
        Point(497,9): "#",
        Point(496,9): "#",
        Point(495,9): "#",
        Point(494,9): "#",
        #
        Point(497,5): "o",
        Point(495,8): "o",
        Point(497,8): "o",
        Point(498,8): "o",
        Point(499,8): "o",
        Point(500,8): "o",
        Point(501,8): "o",
        Point(498,7): "o",
        Point(499,7): "o",
        Point(500,7): "o",
        Point(501,7): "o",
        Point(499,6): "o",
        Point(500,6): "o",
        Point(501,6): "o",
        Point(499,5): "o",
        Point(500,5): "o",
        Point(501,5): "o",
        Point(499,4): "o",
        Point(500,4): "o",
        Point(501,4): "o",
        Point(499,3): "o",
        Point(500,3): "o",
        Point(501,3): "o",
        Point(500,2): "o",
    }
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    simulate_sand_flow_p1(grid)
    assert expected == grid
    assert 24 == len([1 for k,v in grid.items() if v == "o"])


def test_simulate_sand_flow_p2():
    expected = {
        Point(498,4): "#",
        Point(498,5): "#",
        Point(498,6): "#",
        Point(497,6): "#",
        Point(496,6): "#",
        Point(503,4): "#",
        Point(502,4): "#",
        Point(502,5): "#",
        Point(502,6): "#",
        Point(502,7): "#",
        Point(502,8): "#",
        Point(502,9): "#",
        Point(501,9): "#",
        Point(500,9): "#",
        Point(499,9): "#",
        Point(498,9): "#",
        Point(497,9): "#",
        Point(496,9): "#",
        Point(495,9): "#",
        Point(494,9): "#",
        #floor
        Point(485,11): "#",
        Point(486,11): "#",
        Point(487,11): "#",
        Point(488,11): "#",
        Point(489,11): "#",
        Point(490,11): "#",
        Point(491,11): "#",
        Point(492,11): "#",
        Point(493,11): "#",
        Point(494,11): "#",
        Point(495,11): "#",
        Point(496,11): "#",
        Point(497,11): "#",
        Point(498,11): "#",
        Point(499,11): "#",
        Point(500,11): "#",
        Point(501,11): "#",
        Point(502,11): "#",
        Point(503,11): "#",
        Point(504,11): "#",
        Point(505,11): "#",
        Point(506,11): "#",
        Point(507,11): "#",
        Point(508,11): "#",
        Point(509,11): "#",
        Point(510,11): "#",
        Point(511,11): "#",
        Point(512,11): "#",
    }
    expected.update({Point(x, 10): "o" for x in [490,491,492,493,494,502,503,504,505,506,507,508,509,510]})
    expected.update({Point(x, 9): "o" for x in [491,492,493,503,504,505,506,507,508,509]})
    expected.update({Point(x, 8): "o" for x in [492,493,494,495,496,497,498,499,500,501,503,504,505,506,507,508]})
    expected.update({Point(x, 7): "o" for x in [493,494,495,496,498,499,500,501,503,504,505,506,507]})
    expected.update({Point(x, 6): "o" for x in [494,495,499,500,501,503,504,505,506]})
    expected.update({Point(x, 5): "o" for x in [495,496,497,499,500,501,503,504,505]})
    expected.update({Point(x, 4): "o" for x in [496,497,499,500,501,504]})
    expected.update({Point(x, 3): "o" for x in [497,498,499,500,501,502,503]})
    expected.update({Point(x, 2): "o" for x in [498,499,500,501,502]})
    expected.update({Point(x, 1): "o" for x in [499,500,501]})
    expected.update({Point(x, 0): "o" for x in [500]})
    
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    simulate_sand_flow_p2(grid)
    print_grid(grid)
    assert expected == grid
    assert 93 == len([1 for k,v in grid.items() if v == "o"])
