import itertools
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def rock0(x_shift, y_shift): # horizontal
    return {
        Point(0 + x_shift, 0 + y_shift): "#",
        Point(1 + x_shift, 0 + y_shift): "#",
        Point(2 + x_shift, 0 + y_shift): "#",
        Point(3 + x_shift, 0 + y_shift): "#",
    }

def rock1(x_shift, y_shift): # + shape
    return {
        Point(1 + x_shift, 0 + y_shift): "#",
        Point(0 + x_shift, 1 + y_shift): "#",
        Point(1 + x_shift, 1 + y_shift): "#",
        Point(2 + x_shift, 1 + y_shift): "#",
        Point(1 + x_shift, 2 + y_shift): "#",
    }

def rock2(x_shift, y_shift): # reverse L shape
    return {
        Point(0 + x_shift, 0 + y_shift): "#",
        Point(1 + x_shift, 0 + y_shift): "#",
        Point(2 + x_shift, 0 + y_shift): "#",
        Point(2 + x_shift, 1 + y_shift): "#",
        Point(2 + x_shift, 2 + y_shift): "#",
    }

def rock3(x_shift, y_shift): # vertical
    return {
        Point(0 + x_shift, 0 + y_shift): "#",
        Point(0 + x_shift, 1 + y_shift): "#",
        Point(0 + x_shift, 2 + y_shift): "#",
        Point(0 + x_shift, 3 + y_shift): "#",
    }

def rock4(x_shift, y_shift): # square
    return {
        Point(0 + x_shift, 0 + y_shift): "#",
        Point(1 + x_shift, 0 + y_shift): "#",
        Point(0 + x_shift, 1 + y_shift): "#",
        Point(1 + x_shift, 1 + y_shift): "#",
    }


def is_collision(grid1, grid2):
    return not grid1.keys().isdisjoint(grid2.keys())


def render(grid_obj, rock_obj=None):
    if rock_obj:
        effective_grid = {**grid_obj.grid, **rock_obj.grid}
        max_height = max(grid_obj.max_height, rock_obj.top)
    else:
        effective_grid = grid_obj.grid
        max_height = grid_obj.max_height

    out = ""
    for y in range(max_height, -1, -1):
        out += "|" + "".join([effective_grid.get(Point(x, y), ".") for x in range(7)]) + "|\n"
    out += "+-------+"
    return out


class Rock:
    def __init__(self, grid):
        self.grid = grid
        self.bottom = 999999999
        self.top = 0
        self.left_edge = 999999999
        self.right_edge = 0
        for p in self.grid.keys():
            self.bottom = min(self.bottom, p.y)
            self.top = max(self.top, p.y)
            self.left_edge = min(self.left_edge, p.x)
            self.right_edge = max(self.right_edge, p.x)

    def shifted_left(self):
        return Rock({Point(p.x-1, p.y): "#" for p in self.grid.keys()})

    def shifted_right(self):
        return Rock({Point(p.x+1, p.y): "#" for p in self.grid.keys()})

    def shifted_down(self):
        return Rock({Point(p.x, p.y-1): "#" for p in self.grid.keys()})



class Grid:
    def __init__(self, jet_pattern):
        self.jet_generator = itertools.cycle(jet_pattern.strip())
        self.rock_generator = itertools.cycle([rock0, rock1, rock2, rock3, rock4])
        self.stopped_rocks = 0
        self.grid = {}
        self.max_height = -1

    def drop_rock(self) -> None:
        rock = Rock(next(self.rock_generator)(x_shift=2, y_shift=self.max_height+4)) # don't ask me why it's +4 and not +3

        while True:
            # "being pushed by a jet of hot gas"
            jet = next(self.jet_generator)
            shifted_rock = rock.shifted_left() if jet == "<" else rock.shifted_right()
            if shifted_rock.left_edge >= 0 and shifted_rock.right_edge <= 6 and not is_collision(self.grid, shifted_rock.grid):
                rock = shifted_rock
                #print(f"rock #{self.stopped_rocks} moved {jet}")
                #print(render(self, rock))
            else:
                #print(f"rock #{self.stopped_rocks} could not move {jet} (top={rock.top}, bottom={rock.bottom}, left={rock.left_edge}, right={rock.right_edge})")
                #print(render(self, rock))
                pass # jet has no effect

            # "falling one unit down"
            shifted_rock = rock.shifted_down()
            if shifted_rock.bottom >= 0 and not is_collision(self.grid, shifted_rock.grid):
                rock = shifted_rock
                #print(f"rock #{self.stopped_rocks} moved down")
                #print(render(self, rock))
            else:
                #print(f"rock #{self.stopped_rocks} could not move down (top={rock.top}, bottom={rock.bottom}, left={rock.left_edge}, right={rock.right_edge})")
                #print(render(self, rock))
                break

        self.stopped_rocks += 1
        self.grid.update(rock.grid)
        self.max_height = max(self.max_height, rock.top)


def height_after_n_rocks(jet_pattern, num_rocks, do_output):
    grid = Grid(jet_pattern)
    while grid.stopped_rocks < num_rocks:
        grid.drop_rock()
        if do_output:
            print()
            print(render(grid))

    return grid.max_height + 1 # because the "floor" is -1


if __name__ == "__main__":
    input17 = open("../input/input17").read()

    p1_answer = height_after_n_rocks(jet_pattern=input17, num_rocks=2022, do_output=False)
    print(f"height after 2022 rocks fall: {p1_answer}") # 3202
    

###########################

SAMPLE_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_height_after_n_rocks():
    expected = 3068
    actual = height_after_n_rocks(jet_pattern=SAMPLE_INPUT, num_rocks=2022, do_output=False)
    assert expected == actual

def test_first_10():
    expected = 17
    actual = height_after_n_rocks(jet_pattern=SAMPLE_INPUT, num_rocks=10, do_output=True)
    assert expected == actual

def test_height_after_n_rocks_p2():
    expected = 1514285714288
    actual = height_after_n_rocks(jet_pattern=SAMPLE_INPUT, num_rocks=1000000000000, do_output=False)
    assert expected == actual
