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


def simulate_sand_flow(grid): # destructive!
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


if __name__ == "__main__":
    input14 = open("../input/input14").read()

    grid = sparse_grid_from_input(input14)
    simulate_sand_flow(grid)
    sand_units = len([1 for k,v in grid.items() if v == "o"])
    print(f"(p1 answer) How many units of sand come to rest before sand starts flowing into the abyss below? {sand_units}") # 1298


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


def test_simulate_sand_flow():
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
    simulate_sand_flow(grid)
