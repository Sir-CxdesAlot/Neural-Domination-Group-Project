"""
part1_search/flights.py
=======================
Entry point for Part 1: Flight Connections Between Cities.

Finds the shortest sequence of direct flights between two cities using
Breadth-First Search (BFS), which guarantees the minimum number of hops.

Usage
-----
    python part1_search/flights.py <data_directory>

The data directory must contain:
    cities.csv    – city_id, city_name, country
    flights.csv   – flight_id, source_city_id, destination_city_id, airline_id
    airlines.csv  – airline_id, airline_name
"""

import sys
import os

# Allow running from project root or from inside src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.search    import Node, QueueFrontier
from utils.data_loader import load_flight_data
from utils.display    import print_flight_path


# =============================================================================
# Core search functions
# =============================================================================

def neighbors_for_city(city_id: str, cities: dict) -> set:
    """
    Return all (flight_id, dest_city_id) pairs reachable in one hop
    from *city_id*.

    Parameters
    ----------
    city_id : The ID of the departure city.
    cities  : The cities dict from ``load_flight_data``.

    Returns
    -------
    set of (flight_id, city_id) tuples.
    """
    return cities.get(city_id, {}).get("flights", set())


def shortest_path(source: str, target: str, cities: dict) -> list | None:
    """
    BFS shortest path from *source* city_id to *target* city_id.

    Goal is checked when a child node is *created* (not dequeued) so the
    search terminates as soon as the target is reached — no wasted expansion.

    Parameters
    ----------
    source  : city_id of the departure city.
    target  : city_id of the destination city.
    cities  : The cities dict from ``load_flight_data``.

    Returns
    -------
    list of (flight_id, city_id) tuples describing the path,
    or None if no path exists.
    An empty list means source == target (zero connections).
    """
    if source == target:
        return []

    frontier = QueueFrontier()
    frontier.add(Node(state=source, parent=None, action=None))
    explored: set[str] = set()

    while not frontier.empty():
        node = frontier.remove()

        if node.state in explored:
            continue
        explored.add(node.state)

        for flight_id, city_id in sorted(neighbors_for_city(node.state, cities)):
            if city_id in explored:
                continue

            child = Node(state=city_id, parent=node, action=(flight_id, city_id))

            # ── Early goal check ─────────────────────────────────────────────
            if city_id == target:
                return _reconstruct_path(child)

            if not frontier.contains_state(city_id):
                frontier.add(child)

    return None   # no path found


def _reconstruct_path(node: Node) -> list:
    """Walk parent pointers from goal → root and reverse to get source→goal."""
    path = []
    while node.action is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


# =============================================================================
# Disambiguation helper
# =============================================================================

def _resolve_city(prompt_label: str, names: dict, cities: dict) -> str:
    """
    Prompt the user for a city name; return the resolved city_id.
    Handles duplicate names by asking for a city ID.
    """
    city_name = input(f"City: ").strip()
    matches   = names.get(city_name.lower(), set())

    if not matches:
        sys.exit(f"Error: city '{city_name}' not found in the dataset.")

    if len(matches) == 1:
        return next(iter(matches))

    # Multiple cities share this name — disambiguate
    print(f"Multiple cities named '{city_name}':")
    for cid in sorted(matches):
        c = cities[cid]
        print(f"  [{cid}] {c['name']}, {c['country']}")
    return input("Enter city ID: ").strip()


# =============================================================================
# CLI entry-point
# =============================================================================

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python part1_search/flights.py <data_directory>")

    data_dir = sys.argv[1]

    print("Loading data...")
    names, cities, airlines = load_flight_data(data_dir)
    print("Data loaded.\n")

    source_id = _resolve_city("Source", names, cities)
    target_id = _resolve_city("Target", names, cities)

    path = shortest_path(source_id, target_id, cities)
    print_flight_path(path, cities, source_id)


if __name__ == "__main__":
    main()
