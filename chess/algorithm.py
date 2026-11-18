"""CHESS Algorithm v1 path selection."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from .baselines import a_star_search
from .graph import Graph, Node


@dataclass(frozen=True)
class PathResult:
    """Selected route and explicitly tracked primary/alternative measures."""
    algorithm: str
    path: list[Node] | None
    ttd: float
    ctd: float
    art: float
    actd_s: float
    pst: float
    switched: bool
    savings_pct: float
    exec_time_ms: float


def _measure(graph: Graph, path: list[Node] | None, weight: str) -> float:
    if path is None:
        return float("inf")
    return sum(graph.edge_weight(a, b, weight) for a, b in zip(path, path[1:]))


def chess_v1(graph: Graph, start: Node, goal: Node, pst: float = 20.0) -> PathResult:
    """Choose between the fastest route and the cheapest route using PST."""
    if not isinstance(pst, (int, float)) or not 0.0 <= pst <= 99.0:
        raise ValueError("pst must be between 0.0 and 99.0 inclusive")
    began = time.perf_counter()
    fast_path, ttd = a_star_search(graph, start, goal, "travel_time")
    alt_path, _ = a_star_search(graph, start, goal, "cost")
    art = _measure(graph, alt_path, "travel_time")
    ctd = _measure(graph, fast_path, "cost")
    actd_s = _measure(graph, alt_path, "cost")
    savings_pct = ((ctd - actd_s) / ctd * 100.0
                   if actd_s < ctd and ctd > 0 and ctd != float("inf") else 0.0)
    switched = False
    path, selected_ttd, selected_ctd = fast_path, ttd, ctd
    if not (ttd == art and ctd == actd_s) and savings_pct >= pst and actd_s < ctd:
        path, selected_ttd, selected_ctd, switched = alt_path, art, actd_s, True
    elapsed = (time.perf_counter() - began) * 1000.0
    return PathResult("CHESS v1", path, selected_ttd, selected_ctd, art, actd_s,
                      float(pst), switched, savings_pct, elapsed)
