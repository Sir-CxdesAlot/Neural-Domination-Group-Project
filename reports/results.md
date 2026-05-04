# Results Summary

This file captures the latest runnable results produced in this workspace. The canonical values match `reports/evaluation_metrics.json` and `reports/evaluation_notes.md`.

## Important context

- The official assignment datasets for flights and hospital staff files are still not tracked in this repository.
- Parts 1 and 2 were validated on generated demo datasets.
- Part 3 was executed on the extracted GTSRB training dataset in `gtsrb/Train`.

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
- Dataset used: `gtsrb/Train`
- Dataset kind: real GTSRB training data
- Total images loaded: `39,209`
- Held-out test images: `7,842`
- Training run executed with:
  - `EVAL_EPOCHS=6`
  - `EVAL_BATCH=32`
- Final evaluation-script test accuracy: `0.9872`
- Correct predictions: `7,742 / 7,842`
- Saved model: `reports/artifacts/gtsrb_model.keras`
- Evaluation figures:
  - `reports/figures/confusion.png`
  - `reports/figures/sample_predictions.png`
  - `reports/figures/training_curve.png`

## Supporting evaluation outputs

- Evaluation notes: `reports/evaluation_notes.md`
- Metrics JSON: `reports/evaluation_metrics.json`
- Slide storyline: `presentation/slide_draft.md`
