# Neural-Domination-Group-Project

ARI711S group project repository for the three AI tasks:

1. Flight connections between cities
2. Hospital shift scheduling
3. Traffic sign recognition with CNNs

## Current Status

The project is now in the implementation and integration stage.

What is already in place:
- Part 1 search implementation and demo results
- Part 2 CSP scheduler implementation and demo results
- Part 3 CNN training pipeline, saved model, and evaluation figures
- Supporting notebooks, reports, and presentation draft files

## Team

- Tayo (Group Leader)
- Jaden
- Femi
- Pascal
- Josiah

## Main Folders

```text
.
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- demo_flights/
|   |-- demo_staff/
|   `-- demo_gtsrb/
|-- docs/
|   |-- Group Task List.md
|   `-- Workflow.md
|-- meeting-notes/
|-- notebooks/
|-- presentation/
|-- references/
|-- reports/
`-- src/
```

## Key Deliverables

- [docs/Group Task List.md](docs/Group%20Task%20List.md): member responsibilities and milestone plan
- [docs/Workflow.md](docs/Workflow.md): branching, review flow, and definition of done
- [reports/results.md](reports/results.md): runnable results summary
- [reports/evaluation_notes.md](reports/evaluation_notes.md): evaluation notes and metrics
- [presentation/slide_draft.md](presentation/slide_draft.md): slide storyline and visual checklist

## How To Run The Project

Part 1 - Flight connections:

```bash
python src/part1_search/flights.py data/demo_flights
```

Part 2 - Hospital shift scheduler:

```bash
python src/part2_optimization/run_scheduler.py data/demo_staff/staff_small.txt
```

Part 3 - Traffic sign recognition:

```bash
python src/train.py gtsrb/Train reports/artifacts/gtsrb_model.keras
```

## Notes

- The official assignment datasets are not tracked in the repository.
- Demo data is included for Parts 1 and 2.
- The extracted GTSRB training data is expected locally under `gtsrb/Train` for Part 3.
- The final submission still needs to be assembled into one polished notebook/PDF.

## Workflow

1. Pull the latest `main` branch.
2. Work on a feature branch using `feature/<name>-<task>`.
3. Keep commits small and focused.
4. Update the relevant notebook, report, or results file.
5. Open a pull request for review before merge.
