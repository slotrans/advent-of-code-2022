
def tree_grid_from_input_string(input_string):
    grid = []
    for line in input_string.strip().split("\n"):
        grid.append([int(c) for c in line])
    return grid


def above(tree_grid, y, x):
    return [row[x] for row in tree_grid[:y]]


def below(tree_grid, y, x):
    return [row[x] for row in tree_grid[y+1:]]


def to_left(tree_grid, y, x):
    return tree_grid[y][:x]


def to_right(tree_grid, y, x):
    return tree_grid[y][x+1:]


def count_visible_from_outside(tree_grid):
    height = len(tree_grid)
    width = len(tree_grid[0])

    # the outer edge is all visible
    visible = 2*height + 2*width - 4

    # ignore the first and last rows
    for y in range(1, height-1):
        # ignore the left- and right-most columns
        for x in range(1, width-1):
            tree = tree_grid[y][x]

            if(    all([tree > other for other in above(tree_grid, y, x)])
                or all([tree > other for other in below(tree_grid, y, x)])
                or all([tree > other for other in to_left(tree_grid, y, x)])
                or all([tree > other for other in to_right(tree_grid, y, x)])
            ):
                visible += 1

    return visible


if __name__ == "__main__":
    input08 = open("../input/input08").read()

    tree_grid = tree_grid_from_input_string(input08)
    visible_outside = count_visible_from_outside(tree_grid)
    print(f"(p1 answer) how many trees are visible from outside the grid? {visible_outside}") # 1835


###################################

SAMPLE_INPUT = """\
30373
25512
65332
33549
35390
"""


def test_tree_grid_from_input_string():
    expected = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    actual = tree_grid_from_input_string(SAMPLE_INPUT)
    assert expected == actual


def test_count_visible_from_outside():
    expected = 21
    actual = count_visible_from_outside(tree_grid_from_input_string(SAMPLE_INPUT))
    assert expected == actual


def test_above():
    tree_grid = tree_grid_from_input_string(SAMPLE_INPUT)
    assert [] == above(tree_grid, 0, 0)
    assert [0] == above(tree_grid, 1, 1)
    assert [3, 5] == above(tree_grid, 2, 2)
    assert [7, 1, 3] == above(tree_grid, 3, 3)
    assert [3, 2, 2, 9] == above(tree_grid, 4, 4)


def test_below():
    tree_grid = tree_grid_from_input_string(SAMPLE_INPUT)
    assert [2, 6, 3, 3] == below(tree_grid, 0, 0)
    assert [5, 3, 5] == below(tree_grid, 1, 1)
    assert [5, 3] == below(tree_grid, 2, 2)
    assert [9] == below(tree_grid, 3, 3)
    assert [] == below(tree_grid, 4, 4)


def test_to_left():
    tree_grid = tree_grid_from_input_string(SAMPLE_INPUT)
    assert [] == to_left(tree_grid, 0, 0)
    assert [2] == to_left(tree_grid, 1, 1)
    assert [6, 5] == to_left(tree_grid, 2, 2)
    assert [3, 3, 5] == to_left(tree_grid, 3, 3)
    assert [3, 5, 3, 9] == to_left(tree_grid, 4, 4)


def test_to_right():
    tree_grid = tree_grid_from_input_string(SAMPLE_INPUT)
    assert [0, 3, 7, 3] == to_right(tree_grid, 0, 0)
    assert [5, 1, 2] == to_right(tree_grid, 1, 1)
    assert [3, 2] == to_right(tree_grid, 2, 2)
    assert [9] == to_right(tree_grid, 3, 3)
    assert [] == to_right(tree_grid, 4, 4)
