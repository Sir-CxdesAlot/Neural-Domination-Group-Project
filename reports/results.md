# Results Summary

This file captures the latest runnable results produced in this workspace after switching execution to the machine's Conda `base` environment.

## Important context

- The official assignment datasets for flights, hospital staff files, and GTSRB are still not tracked in this repository.
- Parts 1 and 2 were validated on generated demo datasets.
- Part 3 was executed on a generated synthetic traffic-sign dataset to validate the CNN pipeline end to end.

## Part 1 - Flight Connections

- Entry point: `src/part1_search/flights.py`
- Dataset used: `data/demo_flights/`
- Evaluation status: 4 / 4 cases passed
- Example CLI result:
  - `Windhoek -> Johannesburg -> Nairobi -> Cairo`
  - hop count: `3`
- Figure: `reports/figures/part1_route_lengths.png`

## Part 2 - Hospital Shift Scheduler

- Entry point: `src/part2_optimization/run_scheduler.py`
- Dataset used: `data/demo_staff/staff_small.txt`
- Result: all 21 shifts assigned
- Leave violations: `0`
- Rest-rule violations: `0`
- Maximum shifts assigned to any nurse: `5`
- Fairness standard deviation: `1.6`
- Figures:
  - `reports/figures/part2_schedule_overview.png`
  - `reports/figures/part2_shift_distribution.png`

## Part 3 - Traffic Sign Recognition

- Entry point: `src/train.py`
- Dataset used: `data/demo_gtsrb/`
- Training run executed with:
  - `EPOCHS=6`
  - `BATCH=32`
- Final direct training-script test accuracy: `0.6923`
- Saved model: `reports/artifacts/demo_model_from_entry.keras`
- Evaluation figures:
  - `reports/figures/confusion.png`
  - `reports/figures/sample_predictions.png`
  - `reports/figures/training_curve.png`

## Supporting evaluation outputs

- Evaluation notes: `reports/evaluation_notes.md`
- Metrics JSON: `reports/evaluation_metrics.json`
- Slide storyline: `presentation/slide_draft.md`
