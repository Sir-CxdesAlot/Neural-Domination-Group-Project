from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evaluation.demo_data import generate_demo_flight_data, generate_demo_gtsrb, generate_demo_staff_data
from evaluation.metrics import evaluate_flight_case, evaluate_schedule, validate_confusion_matrix
from evaluation.visuals import (
    plot_confusion_matrix,
    plot_flight_route_lengths,
    plot_placeholder_message,
    plot_sample_predictions,
    plot_schedule_table,
    plot_shift_distribution,
    plot_training_curves,
)
from models.Cnn import NUM_CLASSES, build_baseline_cnn
from models.Csp import Shift_AI_Solver
from part1_search.flights import shortest_path
from utils.data_loader import load_flight_data, load_gtsrb, load_staff

try:
    import tensorflow as tf

    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


RANDOM_SEED = 42
TEST_SIZE = 0.20
EPOCHS = int(os.environ.get("EVAL_EPOCHS", "6"))
BATCH_SIZE = int(os.environ.get("EVAL_BATCH", "32"))
DEFAULT_GTSRB_DIR = ROOT / "gtsrb" / "Train"

FIG_DIR = ROOT / "reports" / "figures"
ARTIFACT_DIR = ROOT / "reports" / "artifacts"
REPORT_PATH = ROOT / "reports" / "evaluation_notes.md"
METRICS_PATH = ROOT / "reports" / "evaluation_metrics.json"


def _resolve_city_id(city_name: str, names: dict) -> str:
    matches = names.get(city_name.lower(), set())
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one match for {city_name!r}, got {sorted(matches)}")
    return next(iter(matches))


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _resolve_gtsrb_dir() -> tuple[Path, str]:
    configured = Path(os.environ.get("GTSRB_DIR", str(DEFAULT_GTSRB_DIR)))
    if not configured.is_absolute():
        configured = ROOT / configured

    if configured.is_dir():
        return configured, "real"

    print(f"  - GTSRB directory not found at {_display_path(configured)}; using generated demo data.")
    return generate_demo_gtsrb(ROOT), "demo"


def run_part1() -> dict:
    print("Running Part 1 evaluation...")
    data_dir = generate_demo_flight_data(ROOT)
    names, cities, _ = load_flight_data(str(data_dir))

    cases = [
        ("Windhoek to Cairo", "Windhoek", "Cairo", 3),
        ("Johannesburg to Lagos", "Johannesburg", "Lagos", 1),
        ("Nairobi to Nairobi", "Nairobi", "Nairobi", 0),
        ("Cairo to Windhoek", "Cairo", "Windhoek", None),
    ]

    results = []
    for case_name, source_name, target_name, expected_hops in cases:
        source_id = _resolve_city_id(source_name, names)
        target_id = _resolve_city_id(target_name, names)
        path = shortest_path(source_id, target_id, cities)
        result = evaluate_flight_case(case_name, expected_hops, path, source_id, target_id, cities)
        results.append(result)
        print(
            f"  - {case_name}: expected={expected_hops}, "
            f"actual={result['actual_hops']}, passed={result['passed']}"
        )

    figure_path = FIG_DIR / "part1_route_lengths.png"
    plot_flight_route_lengths(results, figure_path)

    summary = {
        "status": "completed",
        "dataset": str(data_dir.relative_to(ROOT)),
        "cases_run": len(results),
        "cases_passed": sum(item["passed"] for item in results),
        "results": results,
        "figure": str(figure_path.relative_to(ROOT)),
    }
    return summary


def run_part2() -> dict:
    print("Running Part 2 evaluation...")
    staff_file = generate_demo_staff_data(ROOT)
    nurses, leave = load_staff(str(staff_file))
    solver = Shift_AI_Solver(nurses, leave)
    schedule = solver.solve()
    metrics = evaluate_schedule(schedule, leave)

    counts_path = FIG_DIR / "part2_shift_distribution.png"
    schedule_path = FIG_DIR / "part2_schedule_overview.png"
    plot_shift_distribution(metrics["shift_counts"], counts_path)
    plot_schedule_table(schedule, schedule_path)

    print(
        "  - Complete schedule:",
        metrics["complete"],
        "| Constraints satisfied:",
        metrics["passes_constraints"],
        "| Max shifts:",
        metrics["max_shifts_per_nurse"],
    )

    return {
        "status": "completed",
        "dataset": str(staff_file.relative_to(ROOT)),
        "nurses": len(nurses),
        "metrics": metrics,
        "figures": [
            str(counts_path.relative_to(ROOT)),
            str(schedule_path.relative_to(ROOT)),
        ],
    }


def run_part3() -> dict:
    print("Running Part 3 evaluation...")
    confusion_path = FIG_DIR / "confusion.png"
    predictions_path = FIG_DIR / "sample_predictions.png"
    curves_path = FIG_DIR / "training_curve.png"

    if not TF_AVAILABLE:
        message = "Part 3 was not executed in this environment because TensorFlow is not installed."
        plot_placeholder_message("Part 3 Confusion Matrix", message, confusion_path)
        plot_placeholder_message("Part 3 Sample Predictions", message, predictions_path)
        plot_placeholder_message("Part 3 Training Curve", message, curves_path)
        print("  - TensorFlow not available, skipping Part 3.")
        return {
            "status": "skipped",
            "reason": "tensorflow is not installed in this environment",
            "figures": [
                str(confusion_path.relative_to(ROOT)),
                str(predictions_path.relative_to(ROOT)),
                str(curves_path.relative_to(ROOT)),
            ],
        }

    data_dir, dataset_kind = _resolve_gtsrb_dir()
    tf.random.set_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    X, y = load_gtsrb(str(data_dir))
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y,
    )
    y_train_cat = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)
    y_test_cat = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)

    model = build_baseline_cnn()
    history = model.fit(
        X_train,
        y_train_cat,
        validation_split=0.10,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=0,
    )

    loss, accuracy = model.evaluate(X_test, y_test_cat, verbose=0)
    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
    confusion = confusion_matrix(y_test, y_pred)

    model_path = ARTIFACT_DIR / (
        "gtsrb_model.keras" if dataset_kind == "real" else "demo_model.keras"
    )

    plot_confusion_matrix(confusion, confusion_path)
    plot_sample_predictions(X_test, y_test, y_pred, predictions_path)
    plot_training_curves(history, curves_path)
    model.save(model_path)

    validation = validate_confusion_matrix(confusion, y_test)
    correct = int((y_pred == y_test).sum())
    total = int(len(y_test))

    print(
        f"  - Accuracy={accuracy:.4f} | Correct={correct}/{total} "
        f"| Confusion valid={validation['sum_matches_test_size']}"
    )

    return {
        "status": "completed",
        "dataset": _display_path(data_dir),
        "dataset_kind": dataset_kind,
        "total_images": int(len(X)),
        "test_images": total,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "loss": float(loss),
        "accuracy": float(accuracy),
        "correct_predictions": correct,
        "confusion_matrix_validation": validation,
        "figures": [
            str(confusion_path.relative_to(ROOT)),
            str(predictions_path.relative_to(ROOT)),
            str(curves_path.relative_to(ROOT)),
        ],
        "model_artifact": str(model_path.relative_to(ROOT)),
    }


def write_report(results: dict) -> None:
    lines = [
        "# Evaluation Notes",
        "",
        "This report was generated by `src/evaluation/run_evaluation.py`.",
        "",
        "Important note:",
        "The repository does not track the official assignment flight and staff datasets, so this run used generated demo data for Parts 1 and 2.",
        "For Part 3, the script defaults to local `gtsrb/Train` data when present; otherwise it falls back to generated synthetic traffic-sign data.",
        "",
        "## Part 1 - Flight Connections",
        f"- Status: {results['part1']['status']}",
        f"- Dataset: `{results['part1']['dataset']}`",
        f"- Cases passed: {results['part1']['cases_passed']} / {results['part1']['cases_run']}",
        f"- Figure: `{results['part1']['figure']}`",
        "",
        "## Part 2 - Hospital Shift Scheduler",
        f"- Status: {results['part2']['status']}",
        f"- Dataset: `{results['part2']['dataset']}`",
        f"- Nurses in demo roster: {results['part2']['nurses']}",
        f"- All constraints satisfied: {results['part2']['metrics']['passes_constraints']}",
        f"- Max shifts given to one nurse: {results['part2']['metrics']['max_shifts_per_nurse']}",
        f"- Shift fairness standard deviation: {results['part2']['metrics']['fairness_stddev']}",
        "",
        "## Part 3 - Traffic Sign Recognition",
        f"- Status: {results['part3']['status']}",
    ]

    if results["part3"]["status"] == "completed":
        lines.extend(
            [
                f"- Dataset: `{results['part3']['dataset']}`",
                f"- Dataset kind: {results['part3'].get('dataset_kind', 'unknown')}",
                f"- Test accuracy: {results['part3']['accuracy']:.4f}",
                f"- Correct predictions: {results['part3']['correct_predictions']} / {results['part3']['test_images']}",
                f"- Training epochs: {results['part3']['epochs']}",
                "- Figures:",
                f"  - `{results['part3']['figures'][0]}`",
                f"  - `{results['part3']['figures'][1]}`",
                f"  - `{results['part3']['figures'][2]}`",
            ]
        )
    else:
        lines.extend(
            [
                f"- Reason: {results['part3']['reason']}",
                "- Placeholder figures were generated for slide planning:",
                f"  - `{results['part3']['figures'][0]}`",
                f"  - `{results['part3']['figures'][1]}`",
                f"  - `{results['part3']['figures'][2]}`",
            ]
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    METRICS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    results = {
        "part1": run_part1(),
        "part2": run_part2(),
        "part3": run_part3(),
    }
    write_report(results)

    print("\nSaved:")
    print(f"  - Report: {REPORT_PATH.relative_to(ROOT)}")
    print(f"  - Metrics: {METRICS_PATH.relative_to(ROOT)}")
    print(f"  - Figures: {FIG_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
