import networkx as nx


def adjacent_points(point):
    return {
        (point[0]-1, point[1]),
        (point[0]+1, point[1]),
        (point[0], point[1]-1),
        (point[0], point[1]+1),
    }


def graph_from_input(input_string): # -> (graph, start, end)
    G = nx.DiGraph()

    # nodes
    for y, line in enumerate(input_string.strip().split("\n")):
        for x, height_letter in enumerate(list(line)):
            if height_letter == "S":
                height = 1
                start = (x,y)
            elif height_letter == "E":
                height = 26
                end = (x,y)
            else:
                height = ord(height_letter) - 96 # ascii tricks: turns a=1, b=2, ...z=26

            G.add_node((x,y), height=height)

    # edges
    graph_as_grid = nx.get_node_attributes(G, "height") # dict of node -> height
    for node, height in graph_as_grid.items():
        for p in adjacent_points(node):
            if (p in graph_as_grid) and graph_as_grid[p] <= height+1:
                G.add_edge(node, p)

    return (G, start, end)


def min_steps(graph, start, end) -> int:
    try:
        return nx.shortest_path_length(graph, start, end)
    except nx.NetworkXNoPath:
        return 9999


if __name__ == "__main__":
    input12 = open("../input/input12").read()

    graph, start, end = graph_from_input(input12)
    shortest_path_length = min_steps(graph, start, end)
    print(f"(p1 answer) shortest path from S: {shortest_path_length}") # 339

    for alternate_start, height in nx.get_node_attributes(graph, "height").items():
        if height == 1:
            path_length = min_steps(graph, alternate_start, end)
            print(f"  shortest path from {alternate_start} to E: {path_length}")
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


def test_graph_from_input():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    assert (0,0) == start
    assert (5,2) == end
    assert 40 == graph.number_of_nodes()


def test_min_steps_from_start():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    expected = 31
    actual = min_steps(graph, start, end)
    assert expected == actual


def test_min_steps_from_left():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    expected = 1
    actual = min_steps(graph, (4,2), end)
    assert expected == actual


def test_min_steps_from_above():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    expected = 3
    actual = min_steps(graph, (5,1), end)
    assert expected == actual


def test_min_steps_from_right():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    expected = 5
    actual = min_steps(graph, (6,2), end)
    assert expected == actual


def test_min_steps_from_below():
    graph, start, end = graph_from_input(SAMPLE_INPUT)
    expected = 7
    actual = min_steps(graph, (5,3), end)
    assert expected == actual
