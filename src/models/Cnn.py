"""
models/cnn.py
=============
CNN model factory for the GTSRB traffic sign classifier (Part 3).

The module exposes a single factory function ``build_baseline_cnn`` so that
the model architecture lives in one place and can be imported by both the
training entry-point and any notebook.

Architecture (baseline)
-----------------------
    Input  (30×30×3, float32 ∈ [0, 1])
      Conv2D(32, 3×3, ReLU, same)
      MaxPool(2×2)
      Conv2D(64, 3×3, ReLU, same)
      MaxPool(2×2)
      Dropout(0.25)
      Flatten
      Dense(128, ReLU)
      Dropout(0.50)
      Dense(43, Softmax)          ← one output per GTSRB category

Loss      : categorical_crossentropy
Optimiser : Adam (default lr = 0.001)
Metric    : accuracy

Usage
-----
    from models.Cnn import build_baseline_cnn

    model = build_baseline_cnn()
    model.summary()
"""

# TensorFlow is an optional heavy dependency; guard the import so that
# Parts 1 & 2 can be used without it installed.
try:
    import tensorflow as tf
    _TF_AVAILABLE = True
except ImportError:
    _TF_AVAILABLE = False

IMG_SIZE    = 30    # pixels – must match the value used in utils/data_loader.py
NUM_CLASSES = 43    # GTSRB categories 0–42


def build_baseline_cnn(
    img_size:    int = IMG_SIZE,
    num_classes: int = NUM_CLASSES,
    dropout_conv: float = 0.25,
    dropout_fc:   float = 0.50,
    learning_rate: float = 1e-3,
) -> "tf.keras.Model":
    """
    Build and compile the baseline CNN.

    Parameters
    ----------
    img_size      : Side length (pixels) of the square input images.
    num_classes   : Number of output categories.
    dropout_conv  : Dropout rate after the second conv+pool block.
    dropout_fc    : Dropout rate after the fully-connected layer.
    learning_rate : Adam learning rate.

    Returns
    -------
    tf.keras.Sequential  (compiled, ready to call .fit())

    Raises
    ------
    ImportError  if TensorFlow is not installed.
    """
    if not _TF_AVAILABLE:
        raise ImportError(
            "TensorFlow is required for Part 3.\n"
            "Install it with:  pip install tensorflow"
        )

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(img_size, img_size, 3), name="input"),
            # ── Convolutional block 1 ─────────────────────────────────────
            tf.keras.layers.Conv2D(
                32, (3, 3),
                activation="relu",
                padding="same",
                name="conv1",
            ),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2), name="pool1"),

            # ── Convolutional block 2 ─────────────────────────────────────
            tf.keras.layers.Conv2D(
                64, (3, 3),
                activation="relu",
                padding="same",
                name="conv2",
            ),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2), name="pool2"),

            tf.keras.layers.Dropout(dropout_conv, name="drop_conv"),

            # ── Classifier head ───────────────────────────────────────────
            tf.keras.layers.Flatten(name="flatten"),
            tf.keras.layers.Dense(128, activation="relu", name="fc1"),
            tf.keras.layers.Dropout(dropout_fc, name="drop_fc"),
            tf.keras.layers.Dense(num_classes, activation="softmax", name="output"),
        ],
        name="baseline_cnn",
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model
