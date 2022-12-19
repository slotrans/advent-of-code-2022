from collections import namedtuple

Cube = namedtuple("Cube", ["x","y","z"])


def sparse_grid_from_input(input_string):
    grid = {}
    for line in input_string.strip().split("\n"):
        x, y, z = [int(c) for c in line.split(",")]
        grid[Cube(x, y, z)] = "L" # L for lava
    return grid


def count_exposed_sides(coords, grid):
    exposed_sides = 0
    for dx, dy, dz in [
        (-1,  0,  0),
        (+1,  0,  0),
        ( 0, -1,  0),
        ( 0, +1,  0),
        ( 0,  0,  -1),
        ( 0,  0,  +1),
    ]:
        if grid.get(Cube(coords.x+dx, coords.y+dy, coords.z+dz)) is None:
            exposed_sides += 1
    
    return exposed_sides


def lava_droplet_surface_area(grid):
    surface_area = 0
    for cube, content in grid.items():
        if content == "L":
            surface_area += count_exposed_sides(cube, grid)
    return surface_area


def is_interior_point(coords, grid, bounds):
    # If, moving away from the point along each axis, we hit an occupied space,
    # then this point is inside the lava droplet.
    # I'm not certain but I suspect this only works if certain assumptions about the shape of the droplet are true!
    negative_x = False
    for x in range(coords.x-1, bounds["min_x"]-1, -1):
        if grid.get(Cube(x, coords.y, coords.z)) == "L":
            negative_x = True
            break
    positive_x = False
    for x in range(coords.x+1, bounds["max_x"]+1):
        if grid.get(Cube(x, coords.y, coords.z)) == "L":
            positive_x = True
            break
    negative_y = False
    for y in range(coords.y-1, bounds["min_y"]-1, -1):
        if grid.get(Cube(coords.x, y, coords.z)) == "L":
            negative_y = True
            break
    positive_y = False
    for y in range(coords.y+1, bounds["max_y"]+1):
        if grid.get(Cube(coords.x, y, coords.z)) == "L":
            positive_y = True
            break
    negative_z = False
    for z in range(coords.z-1, bounds["min_z"]-1, -1):
        if grid.get(Cube(coords.x, coords.y, z)) == "L":
            negative_z = True
            break
    positive_z = False
    for z in range(coords.z+1, bounds["max_z"]+1):
        if grid.get(Cube(coords.x, coords.y, z)) == "L":
            positive_z = True
            break

    return all([negative_x, positive_x, negative_y, positive_y, negative_z, positive_z])


def is_pocket(coords, grid):
    return grid.get(coords) is None and 0 == count_exposed_sides(coords, grid)


def mark_air_pockets(grid): # mutates the grid!
    bounds = {
        "min_x": 9999,
        "min_y": 9999,
        "min_z": 9999,
        "max_x": -9999,
        "max_y": -9999,
        "max_z": -9999,
    }
    for c in grid.keys():
        bounds["min_x"] = min(bounds["min_x"], c.x)
        bounds["min_y"] = min(bounds["min_y"], c.y)
        bounds["min_z"] = min(bounds["min_z"], c.z)

        bounds["max_x"] = max(bounds["max_x"], c.x)
        bounds["max_y"] = max(bounds["max_y"], c.y)
        bounds["max_z"] = max(bounds["max_z"], c.z)

    for x in range(bounds["min_x"], bounds["max_x"]+1):
        for y in range(bounds["min_y"], bounds["max_y"]+1):
            for z in range(bounds["min_z"], bounds["max_z"]+1):
                coords = Cube(x,y,z)
                if grid.get(coords) is None and is_interior_point(coords, grid, bounds):
                    grid[coords] = "A" # A for air


def print_grid_slice(grid, fixed_z):
    bounds = {
        "min_x": 9999,
        "min_y": 9999,
        "max_x": -9999,
        "max_y": -9999,
    }
    for c in grid.keys():
        bounds["min_x"] = min(bounds["min_x"], c.x)
        bounds["min_y"] = min(bounds["min_y"], c.y)

        bounds["max_x"] = max(bounds["max_x"], c.x)
        bounds["max_y"] = max(bounds["max_y"], c.y)

    grid_slice = []
    for y in range(bounds["min_y"], bounds["max_y"]+1):
        line = []
        for x in range(bounds["min_x"], bounds["max_x"]+1):
            line.append(grid.get(Cube(x,y,fixed_z), "*"))
        grid_slice.append("".join(line))
    for line in grid_slice:
        print(line)


if __name__ == "__main__":
    input18 = open("../input/input18").read()

    grid = sparse_grid_from_input(input18)
    p1_answer = lava_droplet_surface_area(grid)
    #print(f"(p1 answer) What is the surface area of your scanned lava droplet? {p1_answer}") # 4450

    #mark_air_pockets(grid)
    p2_answer = lava_droplet_surface_area(grid)
    #print(f"(p2 answer) What is the exterior surface area of your scanned lava droplet? {p2_answer}") # 
    
    # first wrong attempt: 4216 (too high)
    #   went on the assumption that there were only single-cube air pockets, and each one counted for a 6-face deduction

    # second wrong attempt: 2536 (too low)
    #   not sure what's wrong here

    for z in range(21+1):
        print(f"### z={z} ####################################")
        print_grid_slice(grid, z)
    # printing it, the lava droplet appears to have a hollow center

    # I think the idea is roughly this:
    #   1. establish a bounding box around the droplet, at least 1 unit larger on each side
    #   2. pick a point inside the box but outside the droplet
    #   3. mark that point as "steam" or whatever then recursively spread to all neighboring empty points
    #   4. after this process stops (runs out of empty points), count lava faces that are touching "steam"
    

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
        Cube(2,2,2): "L",
        Cube(1,2,2): "L",
        Cube(3,2,2): "L",
        Cube(2,1,2): "L",
        Cube(2,3,2): "L",
        Cube(2,2,1): "L",
        Cube(2,2,3): "L",
        Cube(2,2,4): "L",
        Cube(2,2,6): "L",
        Cube(1,2,5): "L",
        Cube(3,2,5): "L",
        Cube(2,1,5): "L",
        Cube(2,3,5): "L",
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


def test_is_interior_point():
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    bounds = {
        "min_x": 1,
        "min_y": 1,
        "min_z": 2,
        "max_x": 3,
        "max_y": 3,
        "max_z": 6,
    }
    for coords, expected in [
        (Cube(2,2,2), False),
        (Cube(1,2,2), False),
        (Cube(3,2,2), False),
        (Cube(2,1,2), False),
        (Cube(2,3,2), False),
        (Cube(2,2,1), False),
        (Cube(2,2,3), False),
        (Cube(2,2,4), False),
        (Cube(2,2,6), False),
        (Cube(1,2,5), False),
        (Cube(3,2,5), False),
        (Cube(2,1,5), False),
        (Cube(2,3,5), False),
        #
        (Cube(2,2,5), True),
    ]:
        actual = is_interior_point(coords, grid, bounds)
        assert expected == actual


def test_is_pocket():
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    for coords, expected in [
        (Cube(2,2,2), False),
        (Cube(1,2,2), False),
        (Cube(3,2,2), False),
        (Cube(2,1,2), False),
        (Cube(2,3,2), False),
        (Cube(2,2,1), False),
        (Cube(2,2,3), False),
        (Cube(2,2,4), False),
        (Cube(2,2,6), False),
        (Cube(1,2,5), False),
        (Cube(3,2,5), False),
        (Cube(2,1,5), False),
        (Cube(2,3,5), False),
        #
        (Cube(2,2,5), True),
    ]:
        actual = is_pocket(coords, grid)
        print(coords)
        assert expected == actual


def test_mark_air_pockets():
    grid = sparse_grid_from_input(SAMPLE_INPUT)
    assert len(grid) == 13

    mark_air_pockets(grid)
    assert len(grid) == 14
    assert grid[Cube(2,2,5)] == "A"
