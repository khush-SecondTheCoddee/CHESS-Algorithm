# CHESS Algorithm v1

CHESS is a path selection algorithm that compares a fastest route with a cheapest route, then uses a percentage threshold to decide whether the cost savings justify taking the slower alternative. The implementation uses Python 3.10+ and the standard library only.

## Architecture

- `chess.graph.Graph` stores directed or undirected edges with `travel_time` and `cost` and optional coordinates.
- `chess.baselines` provides reference Dijkstra cost search and A* search for either weight.
- `chess.algorithm.chess_v1` runs a fastest-route search and a cheapest-route search, records both sets of measures, and applies PST.
- `benchmarks/compare.py` compares Dijkstra, A*, and CHESS on a weighted graph and a generated grid maze.

## Terminology

- **TTD (Time to Destination):** Travel/execution time of the primary (faster) path.
- **ART (Alternative Reaching Time):** Travel/execution time of the alternative (slower) path.
- **CTD (Cost to Destination):** Cost associated with the primary (faster) path.
- **ACTD-S (Alternative Cost to Destination - Slower):** Cost associated with the alternative (slower) path.
- **PST (Path Switch Threshold):** Active v1 control parameter (`0.0` to `99.0`, representing percentage `0%` to `99%`).
- **AMSFSCF (Algorithm Manipulation Scale for Speed Cost Favoritism):** Future conceptual speed/cost scale, from 0 (Cheapest) to 1 (Fastest); documentation placeholder only.

PST is active in v1 and will be scrapped and replaced by AMSFSCF in a later update. AMSFSCF has no code implementation in v1. See [the formal specification](docs/SPEC.md) for the threshold table and mathematical rules.

## Usage

```python
from chess import Graph, chess_v1

graph = Graph(directed=False)
graph.add_edge("home", "fast junction", travel_time=2, cost=8)
graph.add_edge("home", "cheap junction", travel_time=3, cost=2)
graph.add_edge("fast junction", "work", travel_time=2, cost=8)
graph.add_edge("cheap junction", "work", travel_time=3, cost=2)

result = chess_v1(graph, "home", "work", pst=20.0)
print(result.path, result.switched)
print(result.ttd, result.ctd, result.art, result.actd_s)
```

Set coordinates with `graph.add_node(node, (x, y))` to provide Euclidean distance guidance. `dijkstra_cost(graph, start, goal)` and `a_star_search(graph, start, goal, weight="travel_time")` are available as baseline helpers. Both return `(path, total_weight)`; unreachable targets return `(None, float("inf"))`.

## Run locally

```sh
python -m unittest discover -s tests -v
python benchmarks/compare.py
```

## v1 limits and v2 roadmap

CHESS v1 makes two searches and then applies PST. Graph edge weights must be non-negative. The v2 direction is to replace PST with AMSFSCF, a continuous 0–1 preference control, and investigate search strategies that reduce repeated work while preserving explicit route measures. AMSFSCF is conceptual only in this release.
