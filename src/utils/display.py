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
MAX_SHIFTS_PER_NURSE = 5


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
        print("Not connected - no route exists between these two cities.")
        return

    if not path:
        print("Same city - no flights needed.")
        return

    print(f"\n{len(path)} flight connection(s).\n")
    current_id = source_id
    for step, (flight_id, city_id) in enumerate(path, start=1):
        from_name = cities[current_id]["name"]
        to_name   = cities[city_id]["name"]
        print(f"  {step}: {from_name}  ->  {to_name}")
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
        print("\nNo valid schedule could be found.")
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

    expected_shifts = [f"{day}_{shift}" for day in DAYS for shift in SHIFTS]
    fully_assigned = all(
        schedule.get(shift) not in (None, "UNASSIGNED")
        for shift in expected_shifts
    )

    leave_violations = []
    for shift, nurse in schedule.items():
        day, _ = shift.split("_", 1)
        if day in leave.get(nurse, set()):
            leave_violations.append((shift, nurse))

    rest_violations = []
    for index, day in enumerate(DAYS[:-1]):
        night_shift = f"{day}_Night"
        morning_shift = f"{DAYS[index + 1]}_Morning"
        night_nurse = schedule.get(night_shift)
        morning_nurse = schedule.get(morning_shift)
        if night_nurse and morning_nurse and night_nurse == morning_nurse:
            rest_violations.append((night_shift, morning_shift, night_nurse))

    overloads = {
        nurse: count
        for nurse, count in shift_counts.items()
        if count > MAX_SHIFTS_PER_NURSE
    }

    all_ok = (
        fully_assigned
        and len(schedule) == len(expected_shifts)
        and not leave_violations
        and not rest_violations
        and not overloads
    )

    status = "All 21 shifts assigned. All constraints satisfied." if all_ok else (
        "Partial - some shifts remain unassigned."
        if not fully_assigned
        else "Schedule assigned, but one or more constraints are violated."
    )
    print(f"\nStatus: {status}")

    if all_ok:
        return

    if not fully_assigned:
        print("  - One or more expected shifts are missing or unassigned.")
    for shift, nurse in leave_violations:
        print(f"  - Leave violation: {nurse} assigned to {shift}.")
    for night_shift, morning_shift, nurse in rest_violations:
        print(f"  - Rest violation: {nurse} assigned to {night_shift} and {morning_shift}.")
    for nurse, count in overloads.items():
        print(f"  - Shift limit violation: {nurse} assigned {count} shifts.")
