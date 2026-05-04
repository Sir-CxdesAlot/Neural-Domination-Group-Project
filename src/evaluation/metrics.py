from __future__ import annotations

from collections import Counter
from math import sqrt


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Night"]


def validate_flight_path(path, source_id: str, target_id: str, cities: dict) -> dict:
    """Validate that a returned path is legal inside the directed graph."""
    if path is None:
        return {
            "is_valid": False,
            "hop_count": None,
            "ended_at_target": False,
        }

    current = source_id
    for flight_id, city_id in path:
        if (flight_id, city_id) not in cities.get(current, {}).get("flights", set()):
            return {
                "is_valid": False,
                "hop_count": len(path),
                "ended_at_target": False,
            }
        current = city_id

    return {
        "is_valid": True,
        "hop_count": len(path),
        "ended_at_target": current == target_id,
    }


def evaluate_flight_case(case_name: str, expected_hops, path, source_id: str, target_id: str, cities: dict) -> dict:
    validation = validate_flight_path(path, source_id, target_id, cities)
    actual_hops = None if path is None else len(path)
    passed = False

    if expected_hops is None:
        passed = path is None
    else:
        passed = (
            validation["is_valid"]
            and validation["ended_at_target"]
            and actual_hops == expected_hops
        )

    return {
        "case": case_name,
        "expected_hops": expected_hops,
        "actual_hops": actual_hops,
        "path_found": path is not None,
        "passed": passed,
        **validation,
    }


def count_leave_violations(schedule: dict | None, leave: dict) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    if schedule is None:
        return violations

    for shift_name, nurse in schedule.items():
        day, _ = shift_name.split("_", 1)
        if day in leave.get(nurse, set()):
            violations.append((shift_name, nurse))
    return violations


def count_rest_violations(schedule: dict | None) -> list[tuple[str, str, str]]:
    violations: list[tuple[str, str, str]] = []
    if schedule is None:
        return violations

    for index, day in enumerate(DAYS[:-1]):
        night_key = f"{day}_Night"
        next_morning_key = f"{DAYS[index + 1]}_Morning"
        night_nurse = schedule.get(night_key)
        morning_nurse = schedule.get(next_morning_key)
        if night_nurse and morning_nurse and night_nurse == morning_nurse:
            violations.append((night_key, next_morning_key, night_nurse))
    return violations


def shift_counts(schedule: dict | None) -> dict[str, int]:
    if schedule is None:
        return {}
    return dict(sorted(Counter(schedule.values()).items()))


def fairness_stddev(counts: dict[str, int]) -> float:
    if not counts:
        return 0.0
    values = list(counts.values())
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return sqrt(variance)


def evaluate_schedule(schedule: dict | None, leave: dict) -> dict:
    counts = shift_counts(schedule)
    leave_violations = count_leave_violations(schedule, leave)
    rest_violations = count_rest_violations(schedule)
    max_assigned = max(counts.values()) if counts else 0

    complete = bool(schedule) and len(schedule) == len(DAYS) * len(SHIFTS)
    fully_assigned = complete and all(value != "UNASSIGNED" for value in schedule.values())

    return {
        "complete": complete,
        "fully_assigned": fully_assigned,
        "leave_violations": leave_violations,
        "rest_violations": rest_violations,
        "max_shifts_per_nurse": max_assigned,
        "shift_counts": counts,
        "fairness_stddev": round(fairness_stddev(counts), 3),
        "passes_constraints": fully_assigned
        and not leave_violations
        and not rest_violations
        and max_assigned <= 5,
    }


def validate_confusion_matrix(confusion, y_true) -> dict:
    return {
        "shape": list(confusion.shape),
        "sum_matches_test_size": int(confusion.sum()) == int(len(y_true)),
    }
