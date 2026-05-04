"""
models/csp.py
=============
Constraint Satisfaction Problem solver for the hospital shift scheduler.

The weekly schedule has 21 variables (7 days × 3 shifts). Each variable's
domain is the set of available nurses. Three constraint types are enforced:

    Unary   – a nurse on approved leave cannot work that day.
    Binary  – a nurse on Night shift X cannot work Morning shift X+1.
    Higher  – no nurse can work more than MAX_SHIFTS_PER_NURSE shifts.

Pipeline
--------
    enforce_node_consistency()   (prune leave days)
        → ac3()                  (propagate rest-period arcs)
            → backtrack({})      (MRV + forward checking)

Usage
-----
    from models.csp import Shift_AI_Solver

    nurses, leave = load_staff("staff_small.txt")
    solver   = Shift_AI_Solver(nurses, leave)
    schedule = solver.solve()      # dict {shift_name: nurse_name} | None
"""

from collections import deque

# ── Schedule constants ────────────────────────────────────────────────────────
DAYS   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Night"]
ALL_SHIFTS = [f"{d}_{s}" for d in DAYS for s in SHIFTS]   # 21 variables

MAX_SHIFTS_PER_NURSE = 5


class Shift_AI_Solver:
    """
    CSP-based nurse scheduler.

    Parameters
    ----------
    nurses : list[str]        All available nurse names.
    leave  : dict[str, set]   nurse → set of day strings when on leave.
    """

    def __init__(self, nurses: list, leave: dict):
        self.nurses = nurses
        self.leave  = leave

        # domains[shift] = set of nurses that *could* fill this shift
        self.domains: dict[str, set] = {s: set(nurses) for s in ALL_SHIFTS}

        # Precompute binary arc pairs: (Night_X, Morning_{X+1})
        self._rest_pairs: list[tuple] = self._build_rest_pairs()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_shift(shift_name: str) -> tuple[str, str]:
        """Return (day, shift_type) from e.g. 'Monday_Morning'."""
        day, shift_type = shift_name.split("_", 1)
        return day, shift_type

    def _build_rest_pairs(self) -> list[tuple]:
        """Night_X → Morning_{X+1} arc pairs (excludes Sunday night)."""
        pairs = []
        for i in range(len(DAYS) - 1):
            pairs.append((f"{DAYS[i]}_Night", f"{DAYS[i + 1]}_Morning"))
        return pairs

    # ── 1. Node consistency ───────────────────────────────────────────────────

    def enforce_node_consistency(self) -> None:
        """
        Remove nurses from a shift's domain when they have approved leave
        on that shift's day (unary constraint).
        """
        for shift in ALL_SHIFTS:
            day, _ = self._parse_shift(shift)
            on_leave = {n for n in self.domains[shift]
                        if day in self.leave.get(n, set())}
            self.domains[shift] -= on_leave

    # ── 2. Arc revision ───────────────────────────────────────────────────────

    def revise(self, x: str, y: str) -> bool:
        """
        Make shift *x* arc-consistent with shift *y*.

        Only Night→Morning rest-period arcs are enforced here: if assigning
        nurse *n* to night shift *x* would leave no valid nurse for morning
        shift *y*, prune *n* from domain(x).

        Returns True if domain(x) was modified.
        """
        if (x, y) not in self._rest_pairs:
            return False

        to_prune = set()
        for nurse in self.domains[x]:
            # Assigning nurse to x means they cannot work y
            if self.domains[y] - {nurse} == set():
                to_prune.add(nurse)

        if to_prune:
            self.domains[x] -= to_prune
            return True
        return False

    # ── 3. AC-3 ──────────────────────────────────────────────────────────────

    def ac3(self) -> bool:
        """
        Enforce arc consistency across all Night→Morning constraint pairs.

        Returns False if any domain is wiped out (problem unsolvable),
        True otherwise.
        """
        queue = deque(self._rest_pairs)

        while queue:
            x, y = queue.popleft()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False                    # domain empty → no solution
                # Re-enqueue arcs that lead into x
                for (a, b) in self._rest_pairs:
                    if b == x and a != y:
                        queue.append((a, x))

        return True

    # ── 4. MRV variable selection ─────────────────────────────────────────────

    def select_unassigned_variable(self, assignment: dict) -> str:
        """
        Choose the next shift to assign using the Minimum Remaining Values
        (MRV) heuristic: pick the shift with the fewest eligible nurses.
        """
        unassigned = [s for s in ALL_SHIFTS if s not in assignment]
        return min(unassigned, key=lambda s: len(self.domains[s]))

    # ── Consistency check used during backtracking ────────────────────────────

    def _is_consistent(self, shift: str, nurse: str, assignment: dict) -> bool:
        """
        Return True iff assigning *nurse* to *shift* satisfies all constraints
        given the current partial *assignment*.
        """
        day, shift_type = self._parse_shift(shift)

        # Unary: leave
        if day in self.leave.get(nurse, set()):
            return False

        # Binary: rest period
        day_idx = DAYS.index(day)
        if shift_type == "Night" and day_idx < len(DAYS) - 1:
            next_morning = f"{DAYS[day_idx + 1]}_Morning"
            if assignment.get(next_morning) == nurse:
                return False
        if shift_type == "Morning" and day_idx > 0:
            prev_night = f"{DAYS[day_idx - 1]}_Night"
            if assignment.get(prev_night) == nurse:
                return False

        # Higher-order: shift cap
        if sum(1 for v in assignment.values() if v == nurse) >= MAX_SHIFTS_PER_NURSE:
            return False

        return True

    # ── 5. Backtracking search ────────────────────────────────────────────────

    def backtrack(self, assignment: dict) -> dict | None:
        """
        Recursive backtracking search with forward checking.

        Returns a complete {shift: nurse} dict on success, or None on failure.
        """
        if len(assignment) == len(ALL_SHIFTS):
            return assignment                           # all 21 shifts filled ✓

        var = self.select_unassigned_variable(assignment)

        for nurse in list(self.domains[var]):
            if not self._is_consistent(var, nurse, assignment):
                continue

            assignment[var] = nurse

            # Forward checking: prune domains of future variables
            pruned: dict[str, set] = {}
            dead_end = False

            for future in ALL_SHIFTS:
                if future in assignment:
                    continue
                removed = {n for n in self.domains[future]
                           if not self._is_consistent(future, n, assignment)}
                if removed:
                    pruned[future] = removed
                    self.domains[future] -= removed
                if not self.domains[future]:
                    dead_end = True
                    break

            if not dead_end:
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            # Restore domains and undo assignment
            for shift, removed in pruned.items():
                self.domains[shift] |= removed
            del assignment[var]

        return None                                    # trigger backtrack

    # ── Public entry-point ────────────────────────────────────────────────────

    def solve(self) -> dict | None:
        """
        Run the full CSP pipeline and return the completed schedule or None.

        Steps: node consistency → AC-3 → backtracking.
        """
        print(f"Data loaded: {len(self.nurses)} staff members available.")
        print("Enforcing node consistency...")
        self.enforce_node_consistency()

        print("Running AC-3 algorithm...")
        if not self.ac3():
            print("AC-3 detected an unsolvable constraint. Aborting.")
            return None

        print("Starting backtracking search...")
        return self.backtrack({})