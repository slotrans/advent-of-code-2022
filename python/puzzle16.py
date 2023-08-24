import itertools
#import functools

import networkx


def graph_from_input(input_string):
    graph = networkx.MultiDiGraph()
    lines = input_string.strip().split("\n")
    for line in lines:
        first_part, second_part = line.split("; ")
        valve_name = first_part.split(" ")[1]
        rate = int(first_part.split(" ")[4].split("=")[1])
        valve_list_string = second_part.removeprefix("tunnels lead to valves ").removeprefix("tunnel leads to valve ")
        adjacent_valve_names = [x.strip() for x in valve_list_string.split(",")]

        graph.add_node(valve_name, rate=rate, open=False)
        graph.add_edges_from([(valve_name, x) for x in adjacent_valve_names])
    
    return graph


def get_openable_valves(graph):
    out = set()
    for n in graph.nodes(data=True):
        name, attributes = n
        if attributes['rate'] > 0 and attributes['open'] == False:
            out.add(name)
    return out


def build_distance_map(graph, valve_set):
    distance_map = {}
    valves_we_care_about = valve_set.union({"AA"})
    for origin, destination in itertools.combinations(valves_we_care_about, 2):
        distance = networkx.shortest_path_length(graph, origin, destination)
        distance_map[(origin, destination)] = distance
        distance_map[(destination, origin)] = distance
    return distance_map


def pressure_released_recursive(rates_map, distance_map, time_remaining, current_valve, remaining_valve_set) -> int:
    # recursive base case #1
    if time_remaining < 1:
        return 0

    pressure_released = rates_map[current_valve] * (time_remaining - 1)

    # recursive base case #2
    if len(remaining_valve_set) == 0:
        return pressure_released

    return max([
        pressure_released + pressure_released_recursive(
            rates_map,
            distance_map, 
            time_remaining - (1 if current_valve != "AA" else 0) - distance_map[(current_valve, next_current_valve)], # annoying special case for AA which we don't spend a minute opening
            next_current_valve,
            remaining_valve_set.difference({next_current_valve}),
        )
        for next_current_valve
        in remaining_valve_set
    ])


def most_pressure_released(graph, time_limit):
    rates_map = networkx.get_node_attributes(graph, "rate")

    valves_to_open = get_openable_valves(graph)
    distance_map = build_distance_map(graph, valves_to_open)

    return pressure_released_recursive(
        rates_map=rates_map,
        distance_map=distance_map, 
        time_remaining=30,
        current_valve="AA",
        remaining_valve_set=valves_to_open,
    )


if __name__ == "__main__":
    input16 = open("../input/input16").read()

    valve_graph = graph_from_input(input16)

    p1_answer = most_pressure_released(graph=valve_graph, time_limit=30)
    print(f"most pressure that can be released: {p1_answer}") # 2029



###############################

SAMPLE_INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def test_graph_from_input():
    expected = networkx.MultiDiGraph()
    expected.add_node("AA", rate=0, open=False)
    expected.add_node("BB", rate=13, open=False)
    expected.add_node("CC", rate=2, open=False)
    expected.add_node("DD", rate=20, open=False)
    expected.add_node("EE", rate=3, open=False)
    expected.add_node("FF", rate=0, open=False)
    expected.add_node("GG", rate=0, open=False)
    expected.add_node("HH", rate=22, open=False)
    expected.add_node("II", rate=0, open=False)
    expected.add_node("JJ", rate=21, open=False)
    expected.add_edges_from([("AA", x) for x in ["DD", "II", "BB"]])
    expected.add_edges_from([("BB", x) for x in ["CC", "AA"]])
    expected.add_edges_from([("CC", x) for x in ["DD", "BB"]])
    expected.add_edges_from([("DD", x) for x in ["CC", "AA", "EE"]])
    expected.add_edges_from([("EE", x) for x in ["FF", "DD"]])
    expected.add_edges_from([("FF", x) for x in ["EE", "GG"]])
    expected.add_edges_from([("GG", x) for x in ["FF", "HH"]])
    expected.add_edges_from([("HH", x) for x in ["GG"]])
    expected.add_edges_from([("II", x) for x in ["AA", "JJ"]])
    expected.add_edges_from([("JJ", x) for x in ["II"]])

    actual = graph_from_input(SAMPLE_INPUT)
    
    assert set(expected.nodes) == set(actual.nodes)
    assert set(expected.edges) == set(actual.edges)


def test_get_openable_valves():
    graph = graph_from_input(SAMPLE_INPUT)
    expected = set(["BB", "CC", "DD", "EE", "HH", "JJ"])
    actual = get_openable_valves(graph)
    assert expected == actual


def test_build_distance_map():
    graph = graph_from_input(SAMPLE_INPUT)
    openable = get_openable_valves(graph)
    actual = build_distance_map(graph, openable)
    expected = {
        ('AA', 'BB'): 1,
        ('AA', 'CC'): 2,
        ('AA', 'DD'): 1,
        ('AA', 'EE'): 2,
        ('AA', 'HH'): 5,
        ('AA', 'JJ'): 2,
        ('BB', 'AA'): 1,
        ('BB', 'CC'): 1,
        ('BB', 'DD'): 2,
        ('BB', 'EE'): 3,
        ('BB', 'HH'): 6,
        ('BB', 'JJ'): 3,
        ('CC', 'AA'): 2,
        ('CC', 'DD'): 1,
        ('CC', 'EE'): 2,
        ('CC', 'HH'): 5,
        ('CC', 'JJ'): 4,
        ('DD', 'AA'): 1,
        ('DD', 'EE'): 1,
        ('DD', 'HH'): 4,
        ('DD', 'JJ'): 3,
        ('EE', 'AA'): 2,
        ('EE', 'HH'): 3,
        ('EE', 'JJ'): 4,
        ('HH', 'AA'): 5,
        ('HH', 'JJ'): 7,
        ('JJ', 'AA'): 2,
        #
        ('BB', 'AA'): 1,
        ('CC', 'AA'): 2,
        ('DD', 'AA'): 1,
        ('EE', 'AA'): 2,
        ('HH', 'AA'): 5,
        ('JJ', 'AA'): 2,
        ('AA', 'BB'): 1,
        ('CC', 'BB'): 1,
        ('DD', 'BB'): 2,
        ('EE', 'BB'): 3,
        ('HH', 'BB'): 6,
        ('JJ', 'BB'): 3,
        ('AA', 'CC'): 2,
        ('DD', 'CC'): 1,
        ('EE', 'CC'): 2,
        ('HH', 'CC'): 5,
        ('JJ', 'CC'): 4,
        ('AA', 'DD'): 1,
        ('EE', 'DD'): 1,
        ('HH', 'DD'): 4,
        ('JJ', 'DD'): 3,
        ('AA', 'EE'): 2,
        ('HH', 'EE'): 3,
        ('JJ', 'EE'): 4,
        ('AA', 'HH'): 5,
        ('JJ', 'HH'): 7,
        ('AA', 'JJ'): 2,
    }
    assert expected == actual


def test_most_pressure_released():
    graph = graph_from_input(SAMPLE_INPUT)
    expected = 1651
    actual = most_pressure_released(graph, 30)
    assert expected == actual
