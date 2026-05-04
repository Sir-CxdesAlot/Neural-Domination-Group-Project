from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def plot_flight_route_lengths(results: list[dict], out_path) -> None:
    labels = [item["case"] for item in results]
    values = [item["actual_hops"] if item["actual_hops"] is not None else 0 for item in results]
    colors = ["#2e8b57" if item["passed"] else "#b22222" for item in results]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(labels, values, color=colors)
    ax.set_title("Part 1 Evaluation: Flight Route Lengths")
    ax.set_ylabel("Hops")
    ax.set_ylim(0, max(values + [1]) + 1)
    ax.tick_params(axis="x", rotation=15)

    for index, item in enumerate(results):
        label = "None" if item["actual_hops"] is None else str(item["actual_hops"])
        ax.text(index, values[index] + 0.05, label, ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_shift_distribution(counts: dict[str, int], out_path) -> None:
    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(labels, values, color="#4169e1")
    ax.axhline(5, color="#b22222", linestyle="--", linewidth=1, label="Max allowed")
    ax.set_title("Part 2 Evaluation: Nurse Shift Distribution")
    ax.set_ylabel("Assigned shifts")
    ax.tick_params(axis="x", rotation=30)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_schedule_table(schedule: dict, out_path) -> None:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    shifts = ["Morning", "Afternoon", "Night"]
    table_rows = [[schedule.get(f"{day}_{shift}", "") for shift in shifts] for day in days]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=table_rows,
        rowLabels=days,
        colLabels=shifts,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)
    ax.set_title("Part 2 Evaluation: Weekly Schedule Overview", pad=18)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_confusion_matrix(confusion: np.ndarray, out_path) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    image = ax.imshow(confusion, cmap="Blues")
    ax.set_title("Part 3 Evaluation: Confusion Matrix")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_sample_predictions(images, y_true, y_pred, out_path, max_items: int = 9) -> None:
    count = min(max_items, len(images))
    indices = np.linspace(0, len(images) - 1, count, dtype=int)

    fig, axes = plt.subplots(3, 3, figsize=(8, 8))
    axes = axes.flatten()

    for axis, index in zip(axes, indices):
        axis.imshow(images[index][:, :, ::-1])
        axis.axis("off")
        axis.set_title(f"T:{int(y_true[index])} P:{int(y_pred[index])}", fontsize=9)

    for axis in axes[count:]:
        axis.axis("off")

    fig.suptitle("Part 3 Evaluation: Sample Predictions", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_training_curves(history, out_path) -> None:
    epochs = range(1, len(history.history["accuracy"]) + 1)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(epochs, history.history["accuracy"], marker="o", label="Train accuracy")
    ax.plot(epochs, history.history["val_accuracy"], marker="o", label="Val accuracy")
    ax.set_title("Part 3 Evaluation: Training Curve")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.05)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_placeholder_message(title: str, message: str, out_path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis("off")
    ax.set_title(title)
    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        wrap=True,
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
