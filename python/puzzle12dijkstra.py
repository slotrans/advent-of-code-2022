from queue import PriorityQueue


class SparseGrid(dict):
    __slots__ = ["START", "END"]


def grid_from_input(input_string):
    grid = SparseGrid()

    for y, line in enumerate(input_string.strip().split("\n")):
        for x, height_letter in enumerate(list(line)):
            if height_letter == "S":
                grid[(x,y)] = 1
                grid.START = (x,y)
            elif height_letter == "E":
                grid[(x,y)] = 26
                grid.END = (x,y)
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


# https://www.geeksforgeeks.org/shortest-path-in-a-directed-graph-by-dijkstras-algorithm/
def min_steps_to_end(grid, starting_point) -> int:
    #Mark all vertices unvisited. Create a set of all unvisited vertices.
    unvisited = set(grid.keys())

    #Assign zero distance value to source vertex and infinity distance value to all other vertices.
    distances = {k: 9999 for k in grid.keys()}
    distances[starting_point] = 0

    #Set the source vertex as current vertex
    current = starting_point

    while True:
        #For current vertex, consider all of its unvisited children and calculate their tentative distances 
        #through the current. (distance of current + weight of the corresponding edge) Compare the newly calculated 
        #distance to the current assigned value (can be infinity for some vertices) and assign the smaller one.
        last_checked_child = None
        for child in adjacent_points(current):
            if child in unvisited and grid[child] <= grid[current]+1:
                tentative = distances[current] + 1
                distances[child] = min(tentative, distances[child])
                last_checked_child = child

        #After considering all the unvisited children of the current vertex, mark the current as visited and 
        #remove it from the unvisited set.
        unvisited.remove(current)

        #Similarly, continue for all the vertex until all the nodes are visited.
        if len(unvisited) == 0:
            break
        else:
            # NY: the description is wrong in that it doesn't specify an order for checking vertices, but the next
            # value for "current" *must* be the least-distance unvisited node
            least_distance = min([distances[u] for u in list(unvisited)])
            for vertex, distance in distances.items():
                if distance == least_distance and vertex in unvisited:
                    current = vertex
                    break

    return distances[grid.END]


if __name__ == "__main__":
    input12 = open("../input/input12").read()

    grid = grid_from_input(input12)
    shortest_path_length = min_steps_to_end(grid, grid.START)
    print(f"(p1 answer) shortest path from S: {shortest_path_length}") # 339

    for point, height in grid.items():
        if height == 1:
            path_length = min_steps_to_end(grid, point)
            print(f"  shortest path from {point} to E: {path_length}")
            shortest_path_length = min(path_length, shortest_path_length)
    print(f"(p2 answer)shortest path from any height=1 square: {shortest_path_length}") # 332


####################################

SAMPLE_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

def test_grid_from_input():
    expected = SparseGrid({
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
    })
    expected.START = (0,0)
    expected.END = (5,2)
    actual = grid_from_input(SAMPLE_INPUT)
    assert expected == actual


def test_min_steps_to_end_from_start():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 31
    actual = min_steps_to_end(grid, grid.START)
    assert expected == actual


def test_min_steps_to_end_from_left():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 1
    actual = min_steps_to_end(grid, (4,2))
    assert expected == actual


def test_min_steps_to_end_from_above():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 3
    actual = min_steps_to_end(grid, (5,1))
    assert expected == actual


def test_min_steps_to_end_from_right():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 5
    actual = min_steps_to_end(grid, (6,2))
    assert expected == actual


def test_min_steps_to_end_from_below():
    grid = grid_from_input(SAMPLE_INPUT)
    expected = 7
    actual = min_steps_to_end(grid, (5,3))
    assert expected == actual
