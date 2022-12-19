from collections import namedtuple

Cube = namedtuple("Cube", ["x","y","z"])


def sparse_grid_from_input(input_string):
    grid = {}
    for line in input_string.strip().split("\n"):
        x, y, z = [int(c) for c in line.split(",")]
        grid[Cube(x, y, z)] = 1
    return grid


def count_exposed_sides(coords, grid):
    covered_sides = 0
    for dx, dy, dz in [
        (-1,  0,  0),
        (+1,  0,  0),
        ( 0, -1,  0),
        ( 0, +1,  0),
        ( 0,  0,  -1),
        ( 0,  0,  +1),
    ]:
        if grid.get(Cube(coords.x+dx, coords.y+dy, coords.z+dz)):
            covered_sides += 1
    return 6 - covered_sides


def lava_droplet_surface_area(grid):
    surface_area = 0
    for cube in grid.keys():
        surface_area += count_exposed_sides(cube, grid)
    return surface_area


if __name__ == "__main__":
    input18 = open("../input/input18").read()

    grid = sparse_grid_from_input(input18)
    p1_answer = lava_droplet_surface_area(grid)
    print(f"(p1 answer) What is the surface area of your scanned lava droplet? {p1_answer}") # 4450
    

###########################

SAMPLE_INPUT = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def test_sparse_grid_from_input():
    expected = {
        Cube(2,2,2): 1,
        Cube(1,2,2): 1,
        Cube(3,2,2): 1,
        Cube(2,1,2): 1,
        Cube(2,3,2): 1,
        Cube(2,2,1): 1,
        Cube(2,2,3): 1,
        Cube(2,2,4): 1,
        Cube(2,2,6): 1,
        Cube(1,2,5): 1,
        Cube(3,2,5): 1,
        Cube(2,1,5): 1,
        Cube(2,3,5): 1,
    }
    actual = sparse_grid_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_count_exposed_sides():
    grid = sparse_grid_from_input("1,1,1\n2,1,1\n")
    assert 5 == count_exposed_sides(Cube(1,1,1), grid)
    assert 5 == count_exposed_sides(Cube(2,1,1), grid)


def test_lava_droplet_surface_area():
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    expected = 64
    actual = lava_droplet_surface_area(grid)
    assert expected == actual
