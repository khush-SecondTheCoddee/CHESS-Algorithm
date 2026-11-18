"""Weighted graph primitives for CHESS and its reference algorithms."""
from __future__ import annotations

import math
from typing import Hashable, Iterable, Mapping

Node = Hashable


class Graph:
    """A weighted directed or undirected graph.

    Edges carry non-negative ``travel_time`` and ``cost`` values. Optional
    node coordinates enable Euclidean distance heuristics in spatial graphs.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Node, dict[Node, dict[str, float]]] = {}
        self._coordinates: dict[Node, tuple[float, float]] = {}

    def add_node(self, node: Node, coordinates: tuple[float, float] | None = None) -> None:
        self._adj.setdefault(node, {})
        if coordinates is not None:
            if len(coordinates) != 2:
                raise ValueError("coordinates must contain exactly two values")
            self._coordinates[node] = (float(coordinates[0]), float(coordinates[1]))

    def add_edge(self, source: Node, target: Node, travel_time: float = 1.0,
                 cost: float = 1.0) -> None:
        for name, value in (("travel_time", travel_time), ("cost", cost)):
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        self.add_node(source)
        self.add_node(target)
        self._adj[source][target] = {"travel_time": float(travel_time), "cost": float(cost)}
        if not self.directed:
            self._adj[target][source] = dict(self._adj[source][target])

    def neighbors(self, node: Node) -> Iterable[tuple[Node, Mapping[str, float]]]:
        return self._adj.get(node, {}).items()

    def has_node(self, node: Node) -> bool:
        return node in self._adj

    def edge_weight(self, source: Node, target: Node, weight: str) -> float:
        if weight not in ("travel_time", "cost"):
            raise ValueError("weight must be 'travel_time' or 'cost'")
        return self._adj[source][target][weight]

    def euclidean_distance(self, source: Node, target: Node) -> float:
        """Return coordinate distance, or zero when either node lacks coordinates."""
        if source not in self._coordinates or target not in self._coordinates:
            return 0.0
        x1, y1 = self._coordinates[source]
        x2, y2 = self._coordinates[target]
        return math.hypot(x2 - x1, y2 - y1)

    def heuristic_scale(self, weight: str) -> float:
        """Largest globally safe Euclidean heuristic multiplier for a weight."""
        ratios = []
        for u, adjacent in self._adj.items():
            for v, weights in adjacent.items():
                distance = self.euclidean_distance(u, v)
                if distance > 0:
                    ratios.append(weights[weight] / distance)
        return min(ratios, default=0.0)

    @property
    def nodes(self) -> tuple[Node, ...]:
        return tuple(self._adj)
