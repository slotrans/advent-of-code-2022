
def grid_from_input(input_string):
    grid = {}

    for y, line in enumerate(input_string.strip().split("\n")):
        for x, height_letter in enumerate(list(line)):
            if height_letter == "S":
                grid[(x,y)] = 1
                grid["start"] = (x,y)
            elif height_letter == "E":
                grid[(x,y)] = 26
                grid["end"] = (x,y)
            else:
                grid[(x,y)] = ord(height_letter) - 96 # ascii tricks: turns a=1, b=2, ...z=26

    return grid


def adjacent_points(point):
    return {
        (point[0]-1, point[1]),
        (point[0]+1, point[1]),
        (point[0], point[1]-1),
        (point[0], point[1]+1),
    }


def min_steps_to_end(grid, point, visited) -> int:
    print(f"{point} | {len(visited)}")
    if point == grid["end"]:
        return len(visited)

    this_height = grid[point]
    points_to_check = set()
    for p in adjacent_points(point):
        if (p in grid) and (p not in visited) and grid[p] <= this_height+1:
            points_to_check.add(p)

    if len(points_to_check) == 0:
        return 9999
    else:
        return min(
            [min_steps_to_end(grid, p, visited.union([point])) for p in points_to_check]
        )


if __name__ == "__main__":
    input12 = open("../input/input12").read()

    grid = grid_from_input(input12)
    shortest_path_length = min_steps_to_end(grid, grid["start"], set())
    print(f"shortest path: {shortest_path_length}")


####################################

SAMPLE_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

def test_grid_from_input():
    expected = {
        (0, 0): 1,
        (1, 0): 1,
        (2, 0): 2,
        (3, 0): 17,
        (4, 0): 16,
        (5, 0): 15,
        (6, 0): 14,
        (7, 0): 13,
        (0, 1): 1,
        (1, 1): 2,
        (2, 1): 3,
        (3, 1): 18,
        (4, 1): 25,
        (5, 1): 24,
        (6, 1): 24,
        (7, 1): 12,
        (0, 2): 1,
        (1, 2): 3,
        (2, 2): 3,
        (3, 2): 19,
        (4, 2): 26,
        (5, 2): 26,
        (6, 2): 24,
        (7, 2): 11,
        (0, 3): 1,
        (1, 3): 3,
        (2, 3): 3,
        (3, 3): 20,
        (4, 3): 21,
        (5, 3): 22,
        (6, 3): 23,
        (7, 3): 10,
        (0, 4): 1,
        (1, 4): 2,
        (2, 4): 4,
        (3, 4): 5,
        (4, 4): 6,
        (5, 4): 7,
        (6, 4): 8,
        (7, 4): 9,
        "start": (0,0),
        "end": (5,2),
    }
    actual = grid_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_min_steps_to_end_from_start():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 31
    actual = min_steps_to_end(grid, grid["start"], set())
    assert expected == actual


def test_min_steps_to_end_from_left():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 1
    actual = min_steps_to_end(grid, (4,2), set())
    assert expected == actual


def test_min_steps_to_end_from_above():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 3
    actual = min_steps_to_end(grid, (5,1), set())
    assert expected == actual


def test_min_steps_to_end_from_right():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 5
    actual = min_steps_to_end(grid, (6,2), set())
    assert expected == actual


def test_min_steps_to_end_from_below():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 7
    actual = min_steps_to_end(grid, (5,3), set())
    assert expected == actual
