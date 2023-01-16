@Grab("org.jgrapht:jgrapht-core:1.5.1")

import org.jgrapht.Graph
import org.jgrapht.graph.DefaultDirectedGraph
import org.jgrapht.graph.DefaultEdge
import org.jgrapht.alg.shortestpath.DijkstraShortestPath


record Point(int x, int y) {}


class Puzzle12 {
    def adjacentPoints(Point p) {
        return [
            new Point(p.x-1, p.y),
            new Point(p.x+1, p.y),
            new Point(p.x, p.y-1),
            new Point(p.x, p.y+1),
        ]
    }


    def graphFromInput(String input) {
        Point start = null
        Point end = null
        Map<Point, Integer> heightMap = [:]

        input.trim().readLines().eachWithIndex { line, y ->
            line.toList().eachWithIndex { heightLetter, x ->
                def point = new Point(x,y)
                def height = null

                if(heightLetter == "S") {
                    height = 1
                    start = point
                }
                else if(heightLetter == "E") {
                    height = 26
                    end = point
                }
                else {
                    height = ((int) heightLetter.toCharacter()) - 96
                }

                heightMap[point] = height
            }
        }

        Graph<Point, DefaultEdge> graph = new DefaultDirectedGraph(DefaultEdge.class)

        // vertices
        for(p in heightMap.keySet()) {
            graph.addVertex(p)
        }

        // edges
        for(vertex in graph.vertexSet()) {
            for(p in adjacentPoints(vertex)) {
                if(p in heightMap && heightMap[p] <= heightMap[vertex]+1) {
                    graph.addEdge(vertex, p)
                }
            }
        }

        return [graph, heightMap, start, end]
    }

    double minSteps(Graph graph, Point start, Point end) {
        def shortestPathAlgo = new DijkstraShortestPath(graph)
        return shortestPathAlgo.getPathWeight(start, end)
    }

    def run() {
        def puzzle12 = new Puzzle12()

        def input12 = new File("../input/input12").text

        def (graph, heightMap, start, end) = puzzle12.graphFromInput(input12)
        def shortest_path_length = puzzle12.minSteps(graph, start, end)
        println("(p1 answer) shortest path from S: ${shortest_path_length}") // 339

        for(alternate_start in graph.vertexSet()) {
            if(heightMap[alternate_start] == 1) {
                def path_length = puzzle12.minSteps(graph, alternate_start, end)
                println("  shortest path from {alternate_start} to E: ${path_length}")
                shortest_path_length = Math.min(path_length, shortest_path_length)
            }
        }
        println("(p2 answer)shortest path from any height=1 square: ${shortest_path_length}") // 332
    }
}


///////////////////////////////////////////////////////////

// hacky!
class Puzzle12Test {
    def SAMPLE_INPUT = """Sabqponm
                         |abcryxxl
                         |accszExk
                         |acctuvwj
                         |abdefghi""".stripMargin()

    def test_graphFromInput() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        assert new Point(0,0) == start
        assert new Point(5,2) == end
        assert 40 == graph.vertexSet().size()

        println("test_graphFromInput: passed")
    }

    def test_minStepsFromStart() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        def actual = puzzle12.minSteps(graph, start, end)
        def expected = 31
        assert expected == actual

        println("test_minStepsFromStart: passed")
    }

    def test_minStepsFromLeft() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        def actual = puzzle12.minSteps(graph, new Point(4,2), end)
        def expected = 1
        assert expected == actual

        println("test_minStepsFromLeft: passed")
    }

    def test_minStepsFromAbove() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        def actual = puzzle12.minSteps(graph, new Point(5,1), end)
        def expected = 3
        assert expected == actual

        println("test_minStepsFromAbove: passed")
    }

    def test_minStepsFromRight() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        def actual = puzzle12.minSteps(graph, new Point(6,2), end)
        def expected = 5
        assert expected == actual

        println("test_minStepsFromRight: passed")
    }

    def test_minStepsFromBelow() {
        def puzzle12 = new Puzzle12()
        def (graph, heightMap, start, end) = puzzle12.graphFromInput(SAMPLE_INPUT)
        def actual = puzzle12.minSteps(graph, new Point(5,3), end)
        def expected = 7
        assert expected == actual

        println("test_minStepsFromBelow: passed")
    }

    def run() {
        test_graphFromInput()
        test_minStepsFromStart()
        test_minStepsFromLeft()
        test_minStepsFromAbove()
        test_minStepsFromRight()
        test_minStepsFromBelow()
    }
}

///////////////////////////////////////////////////////////

if(this.args.size() > 0 && this.args[0] == "test") {
    new Puzzle12Test().run()
}
else {
    new Puzzle12().run()
}
