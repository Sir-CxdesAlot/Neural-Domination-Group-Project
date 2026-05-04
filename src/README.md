# src

Implementation code for all three project parts.

## Directory structure
- `models/` — baseline model classes (CNN, CSP solver, search primitives)
- `utils/` — helper functions for data loading and visualization
- `part1_search/` — flight connection search implementation
- `part2_optimization/` — hospital shift scheduler
- `part3_ml/` — traffic sign recognition training
- `train.py` — main entry point

## Part 3: Traffic Sign Recognition (CNN)

### Running the training pipeline

Download and extract the GTSRB dataset, then run:

```bash
# Train only
python part3_ml/train.py gtsrb/Train

# Train and save model
python part3_ml/train.py gtsrb/Train reports/artifacts/gtsrb_model.keras

# With custom hyperparameters
EPOCHS=20 BATCH=64 python part3_ml/train.py gtsrb/Train reports/artifacts/gtsrb_model.keras
```

### Expected dataset structure

```
gtsrb/
├── Train/
│   ├── 0/
│   │   ├── image1.png
│   │   └── ...
│   ├── 1/
│   │   ├── image1.png
│   │   └── ...
│   └── ... (folders 0–42)
├── Test/
├── Train.csv
├── Test.csv
└── Meta.csv
```

Use `gtsrb/Train` as the data path for the current loader. The root `gtsrb/`
folder is ignored by Git because it is a local dataset.

### Hyperparameter options

- `EPOCHS` — training epochs (default: 10)
- `BATCH` — batch size (default: 32)
- `TEST_SPLIT` — test/train split ratio (default: 0.20)

### Output

The script will print:
- Data loading summary
- Model architecture summary
- Training history (epoch, train_acc, val_acc)
- Test accuracy
- Classification report
- Visual inspection of sample predictions

If `model.h5` is specified, the trained model is saved for later use.

### Dependencies

```bash
pip install tensorflow opencv-python scikit-learn numpy matplotlib
```

## Part 1 & 2: Search and Optimization

See respective folders for usage and requirements.
