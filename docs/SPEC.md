# CHESS Algorithm v1 Specification

## Status and terminology

- **TTD (Time to Destination):** Travel/execution time of the primary (faster) path.
- **ART (Alternative Reaching Time):** Travel/execution time of the alternative (slower) path.
- **CTD (Cost to Destination):** Cost associated with the primary (faster) path.
- **ACTD-S (Alternative Cost to Destination - Slower):** Cost associated with the alternative (slower) path.
- **PST (Path Switch Threshold):** Active v1 control parameter (`0.0` to `99.0`, representing percentage `0%` to `99%`). **[Status: Active in v1 — Scheduled for Deprecation in v2]**
- **AMSFSCF (Algorithm Manipulation Scale for Speed Cost Favoritism):** A conceptual scale from 0 (Cheapest) to 1 (Fastest), reserved for a future release. **[Status: Conceptual / Docs Only — Target Replacement in v2]**

AMSFSCF is a documentation-only placeholder in v1. PST is active in v1 and will be scrapped and replaced by AMSFSCF in a later update. There is no AMSFSCF control or implementation in the Python package.

## Graph model

A graph has finite, non-negative `travel_time` and `cost` on every directed edge. Undirected graphs store the same weight in each direction. A route's measure is the sum of its edge weights. Nodes may have 2D coordinates; Euclidean distance can guide A*. A safe global scale based on edge weight/distance preserves an admissible heuristic. Missing coordinates yield a zero heuristic.

## Selection rules

Let `fast_path` minimize total travel_time, and let `alt_path` minimize total cost. Define:

- `TTD = time(fast_path)` and `CTD = cost(fast_path)`.
- `ART = time(alt_path)` and `ACTD-S = cost(alt_path)`.
- If the routes have identical TTD/ART and CTD/ACTD-S, keep `fast_path` and set `switched = false`.
- If `ACTD-S < CTD` and `CTD > 0`, then `diff_pct = ((CTD - ACTD-S) / CTD) × 100`; otherwise `diff_pct = 0`.
- Switch to `alt_path` exactly when `diff_pct >= PST` and `ACTD-S < CTD`. A switch reports selected TTD as ART and selected CTD as ACTD-S.

PST must be numeric and within inclusive bounds 0.0–99.0; invalid values raise `ValueError`. With PST 0, any strictly positive cost saving triggers a switch. Ties remain on the primary route. Unreachable routes return no path and infinite measures.

## PST reference table

The final column is the minimum saving required to meet the threshold when CTD is 1.00 cost unit. At 0%, any positive saving switches, including a 0.01 unit difference; a zero difference does not switch because savings must be strict.

| PST | Minimum cost saving (CTD = 1.00) |
|---:|---:|
| 0% (`0.00`) | Any positive amount, including `0.01` |
| 10% (`10.00`) | `0.10` |
| 20% (`20.00`) | `0.20` |
| 30% (`30.00`) | `0.30` |
| 40% (`40.00`) | `0.40` |
| 50% (`50.00`) | `0.50` |
| 60% (`60.00`) | `0.60` |
| 70% (`70.00`) | `0.70` |
| 80% (`80.00`) | `0.80` |
| 90% (`90.00`) | `0.90` |
| 99% (`99.00`) | `0.99` (cap) |

## Implementation notes

CHESS v1 runs two A* searches: one for travel_time and one for cost. Each measure is tracked explicitly. The result includes selected path, selected TTD/CTD, alternative ART/ACTD-S, PST, savings percentage, switch flag, and execution time. The implementation prioritizes clarity and reproducible comparisons; it does not claim one search pass or universal speed advantage.

## AMSFSCF future concept

AMSFSCF is intended to express speed versus cost preference on a continuous 0–1 scale, where 0 means Cheapest and 1 means Fastest. It is conceptual only and reserved for v2+. The intended migration scraps PST and uses AMSFSCF as the replacement control.
