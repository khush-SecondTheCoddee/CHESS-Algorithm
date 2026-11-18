"""Reference shortest-path implementations used by CHESS benchmarks."""
from __future__ import annotations

import heapq
import itertools
from typing import Any

from .graph import Graph, Node


def _search(graph: Graph, start: Node, goal: Node, weight: str, use_heuristic: bool):
    if weight not in ("travel_time", "cost"):
        raise ValueError("weight must be 'travel_time' or 'cost'")
    if not graph.has_node(start) or not graph.has_node(goal):
        return None, float("inf")
    counter = itertools.count()
    scale = graph.heuristic_scale(weight) if use_heuristic else 0.0
    queue = [(scale * graph.euclidean_distance(start, goal), next(counter), 0.0, start)]
    distances = {start: 0.0}
    previous: dict[Node, Node] = {}
    while queue:
        _, _, distance, node = heapq.heappop(queue)
        if distance != distances.get(node):
            continue
        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            return list(reversed(path)), distance
        for neighbor, weights in graph.neighbors(node):
            candidate = distance + weights[weight]
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                previous[neighbor] = node
                estimate = scale * graph.euclidean_distance(neighbor, goal)
                heapq.heappush(queue, (candidate + estimate, next(counter), candidate, neighbor))
    return None, float("inf")


def dijkstra_cost(graph: Graph, start: Node, goal: Node):
    """Return ``(path, cost)`` for the lowest-cost route, or ``(None, inf)``."""
    return _search(graph, start, goal, "cost", False)


def a_star_search(graph: Graph, start: Node, goal: Node, weight: str = "travel_time"):
    """Return ``(path, total_weight)`` optimizing travel_time or cost."""
    return _search(graph, start, goal, weight, True)
