"""
part3_ml/train.py  (also serves as src/train.py entry point)
=============================================================
Entry point for Part 3: Traffic Sign Recognition (GTSRB).

Full pipeline:
    1. Load & preprocess images      (utils.data_loader.load_gtsrb)
    2. Train/test split              (sklearn)
    3. Build baseline CNN            (models.cnn.build_baseline_cnn)
    4. Train with validation split
    5. Evaluate accuracy + report
    6. Visual inspection on test set
    7. Optionally save model to disk

Usage
-----
    # Train only
    python part3_ml/train.py gtsrb/

    # Train and save model
    python part3_ml/train.py gtsrb/ model.h5

    # Custom hyperparameters via environment variables
    EPOCHS=20 BATCH=64 python part3_ml/train.py gtsrb/ model.h5
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

from models.cnn        import build_baseline_cnn, NUM_CLASSES
from utils.data_loader import load_gtsrb

try:
    import tensorflow as tf
except ImportError:
    sys.exit("TensorFlow not found. Run: pip install tensorflow")

# ── Hyperparameters (overridable via env vars) ────────────────────────────────
EPOCHS     = int(os.environ.get("EPOCHS", 10))
BATCH_SIZE = int(os.environ.get("BATCH",  32))
TEST_SIZE  = float(os.environ.get("TEST_SPLIT", 0.20))
RANDOM_SEED = 42


# =============================================================================
# Evaluation helpers
# =============================================================================

def evaluate(model, X_test: np.ndarray, y_test: np.ndarray) -> tuple:
    """
    Evaluate *model* on the test set.

    Returns (confusion_matrix, accuracy).
    Prints accuracy + per-class report for the first 10 categories.
    """
    print("\nEvaluating model...")
    y_test_cat = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)
    loss, acc  = model.evaluate(X_test, y_test_cat, verbose=2)
    print(f"\nModel accuracy: {acc:.4f}")

    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)

    target_names = [f"Sign_{i:02d}" for i in range(NUM_CLASSES)]
    print("\nClassification Report (categories 0–9):")
    print(
        classification_report(
            y_test, y_pred,
            labels=list(range(10)),
            target_names=target_names[:10],
            zero_division=0,
        )
    )

    cm = confusion_matrix(y_test, y_pred)
    return cm, acc


def visual_inspection(
    model,
    X_test: np.ndarray,
    y_test: np.ndarray,
    n: int = 10,
) -> None:
    """
    Print prediction results for *n* randomly sampled test images.
    """
    rng     = np.random.default_rng(RANDOM_SEED)
    indices = rng.choice(len(X_test), size=min(n, len(X_test)), replace=False)

    print(f"\nVisual Inspection ({n} random test samples):")
    print(f"{'Idx':>6}  {'True':>5}  {'Pred':>5}  {'Confidence':>11}  Match")
    print("─" * 46)

    for idx in indices:
        probs = model.predict(X_test[idx : idx + 1], verbose=0)[0]
        pred  = int(np.argmax(probs))
        true  = int(y_test[idx])
        conf  = float(probs[pred])
        mark  = "✓" if pred == true else "✗"
        print(f"{idx:>6}  {true:>5}  {pred:>5}  {conf:>10.2%}  {mark}")


# =============================================================================
# Training curve summary
# =============================================================================

def print_history(history) -> None:
    train_accs = history.history["accuracy"]
    val_accs   = history.history["val_accuracy"]
    print("\nTraining history (epoch | train_acc | val_acc):")
    print("─" * 38)
    for epoch, (ta, va) in enumerate(zip(train_accs, val_accs), start=1):
        bar = "█" * int(ta * 20)
        print(f"  Epoch {epoch:>2} | {ta:.4f}  | {va:.4f}  {bar}")


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python part3_ml/train.py <gtsrb_dir> [model.h5]")

    data_dir   = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) == 3 else None

    # ── 1. Load data ──────────────────────────────────────────────────────────
    print("Loading data...")
    X, y = load_gtsrb(data_dir)
    print(f"Data loaded.  Total images: {len(X):,}  |  Classes: {NUM_CLASSES}")

    # ── 2. Train / test split ─────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y,
    )
    y_train_cat = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)

    # ── 3. Build model ────────────────────────────────────────────────────────
    print("\nBuilding model...")
    model = build_baseline_cnn()
    model.summary()

    # ── 4. Train ──────────────────────────────────────────────────────────────
    print(f"\nTraining model  (epochs={EPOCHS}, batch={BATCH_SIZE}) ...")
    history = model.fit(
        X_train, y_train_cat,
        validation_split=0.10,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1,
    )

    # ── 5. Evaluate ───────────────────────────────────────────────────────────
    cm, acc = evaluate(model, X_test, y_test)

    # ── 6. Visual inspection ──────────────────────────────────────────────────
    visual_inspection(model, X_test, y_test, n=10)

    # ── 7. Training curve ─────────────────────────────────────────────────────
    print_history(history)

    # ── 8. Save model ─────────────────────────────────────────────────────────
    if model_path:
        model.save(model_path)
        print(f"\nModel saved to {model_path}")

    print(f"\nFinal test accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()