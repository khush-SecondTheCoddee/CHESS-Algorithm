"""Compare Dijkstra, A*, and CHESS v1 on a weighted graph and grid maze."""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chess import Graph, a_star_search, chess_v1, dijkstra_cost


def measure(label, function, graph, start, goal):
    began = time.perf_counter()
    output = function(graph, start, goal)
    elapsed = (time.perf_counter() - began) * 1000
    if isinstance(output, tuple):
        path = output[0]
    else:
        path = output.path
        elapsed = output.exec_time_ms
    ttime = cost = float("inf")
    if path is not None:
        ttime = sum(graph.edge_weight(a, b, "travel_time") for a, b in zip(path, path[1:]))
        cost = sum(graph.edge_weight(a, b, "cost") for a, b in zip(path, path[1:]))
    print(f"{label:12} {elapsed:9.3f} ms  path_time={ttime:8.2f}  path_cost={cost:8.2f}")


def graph_example():
    graph = Graph(directed=False)
    edges = [("S", "A", 2, 5), ("A", "G", 2, 5), ("S", "B", 3, 1),
             ("B", "G", 3, 1), ("A", "B", 1, 2)]
    for a, b, t, c in edges:
        graph.add_edge(a, b, t, c)
    return graph, "S", "G"


def grid_maze(width=30, height=20):
    graph = Graph(directed=False)
    for y in range(height):
        for x in range(width):
            graph.add_node((x, y), (x, y))
            # Deterministic alternating wall pattern with periodic openings.
            if x + 1 < width and not (x % 7 == 3 and y % 5 != 2):
                graph.add_edge((x, y), (x + 1, y), 1, 1 + ((x + y) % 4) * 0.2)
            if y + 1 < height:
                graph.add_edge((x, y), (x, y + 1), 1, 1 + ((x * 2 + y) % 4) * 0.2)
    return graph, (0, 0), (width - 1, height - 1)


def run_case(title, graph, start, goal):
    print(f"\n{title}")
    measure("Dijkstra cost", dijkstra_cost, graph, start, goal)
    measure("A* time", lambda g, s, t: a_star_search(g, s, t, "travel_time"), graph, start, goal)
    measure("CHESS v1", chess_v1, graph, start, goal)


if __name__ == "__main__":
    run_case("Weighted graph", *graph_example())
    run_case("Grid maze", *grid_maze())
