"""
part2_optimization/run_scheduler.py
=====================================
Entry point for Part 2: Hospital Shift Scheduler.

Loads a staff file, runs the CSP pipeline (node consistency → AC-3 →
backtracking with MRV + forward checking), and prints the weekly schedule.

Usage
-----
    python part2_optimization/run_scheduler.py <staff_file>

    # Examples
    python part2_optimization/run_scheduler.py data/staff_small.txt
    python part2_optimization/run_scheduler.py data/staff_medium.txt
    python part2_optimization/run_scheduler.py data/staff_complex.txt
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.csp        import Shift_AI_Solver
from utils.data_loader import load_staff
from utils.display     import print_schedule


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python part2_optimization/run_scheduler.py <staff_file>")

    staff_file = sys.argv[1]
    print("Generating Weekly Schedule for 2026...")

    nurses, leave = load_staff(staff_file)

    solver   = Shift_AI_Solver(nurses, leave)
    schedule = solver.solve()

    print_schedule(schedule, leave)


if __name__ == "__main__":
    main()