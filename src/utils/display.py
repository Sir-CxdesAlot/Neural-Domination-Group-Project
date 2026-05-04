"""
utils/display.py
================
Human-readable output helpers shared across project parts.

Functions
---------
print_schedule(schedule, leave)   Pretty-print the nurse schedule (Part 2).
print_flight_path(path, cities, source_id)  Print hop-by-hop route (Part 1).
"""

from __future__ import annotations

DAYS   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Night"]


# =============================================================================
# Part 1 – Route display
# =============================================================================

def print_flight_path(
    path:      list[tuple] | None,
    cities:    dict,
    source_id: str,
) -> None:
    """
    Print a numbered hop-by-hop route returned by ``shortest_path``.

    Parameters
    ----------
    path      : List of (flight_id, city_id) tuples, or None (no route).
    cities    : The cities dict from ``load_flight_data``.
    source_id : city_id of the departure city.
    """
    if path is None:
        print("Not connected — no route exists between these two cities.")
        return

    if not path:
        print("Same city — no flights needed.")
        return

    print(f"\n{len(path)} flight connection(s).\n")
    current_id = source_id
    for step, (flight_id, city_id) in enumerate(path, start=1):
        from_name = cities[current_id]["name"]
        to_name   = cities[city_id]["name"]
        print(f"  {step}: {from_name}  →  {to_name}")
        current_id = city_id


# =============================================================================
# Part 2 – Schedule display
# =============================================================================

def print_schedule(schedule: dict | None, leave: dict) -> None:
    """
    Pretty-print the completed nurse schedule with leave annotations.

    Parameters
    ----------
    schedule : {shift_name: nurse_name} dict returned by the solver,
               or None if no valid schedule was found.
    leave    : {nurse_name: set of day strings} from ``load_staff``.
    """
    if schedule is None:
        print("\n❌  No valid schedule could be found.")
        return

    shift_counts: dict[str, int] = {}

    for day in DAYS:
        print(f"\n{day.upper()}:")
        for shift_type in SHIFTS:
            key   = f"{day}_{shift_type}"
            nurse = schedule.get(key, "UNASSIGNED")

            # Nurses on leave that day (excluding the assigned nurse)
            on_leave = [
                n for n, ld in leave.items()
                if day in ld and n != nurse
            ]

            note = ""
            if on_leave:
                names = ", ".join(on_leave[:2])
                verb  = "is" if len(on_leave) == 1 else "are"
                note  = f"  (Note: {names} {verb} Off)"

            print(f"  {shift_type:<11}: {nurse}{note}")
            if nurse != "UNASSIGNED":
                shift_counts[nurse] = shift_counts.get(nurse, 0) + 1

    # ── Totals ────────────────────────────────────────────────────────────────
    print("\nSchedule Totals:")
    for nurse, count in sorted(shift_counts.items(), key=lambda x: -x[1]):
        print(f"  - {nurse}: {count} shift(s)")

    all_ok = len(schedule) == len(DAYS) * len(SHIFTS) and \
             all(v != "UNASSIGNED" for v in schedule.values())

    status = "✅  All 21 shifts assigned. All constraints satisfied." \
             if all_ok else "⚠️   Partial – some shifts remain unassigned."
    print(f"\nStatus: {status}")