# Project Results & Findings

## Part 1 — Flight Connections Between Cities

**Implementation:** `src/part1_search/flights.py`

### Test Results
- Dataset used: (specify cities CSV files)
- Example paths tested:
  - Windhoek → Cairo: expected 3 connections
  - (add more test cases)

### Notes
- BFS correctly finds shortest path (fewest hops)
- Handles disconnected cities gracefully (returns None)

---

## Part 2 — Hospital Shift Scheduler (CSP Solver)

**Implementation:** `src/models/Csp.py`

### Test Results
- Dataset: `staff_small.txt` / `staff_medium.txt` / `staff_complex.txt`
- Nurses available: (number)
- Solver status: Success / Failed
- All 21 shifts assigned: Yes / No
- Constraints satisfied: Yes / No

### Example schedule output
```
MONDAY:
  Morning:   [Nurse Name]
  Afternoon: [Nurse Name]
  Night:     [Nurse Name]
...
Schedule Totals:
  - Nurse A: 3 shifts
  - Nurse B: 4 shifts
  - (etc.)
```

### Notes
- AC-3 propagation pruned X domain values
- Backtracking iterations: (optional metric)
- MRV heuristic effectiveness: (observations)

---

## Part 3 — Traffic Sign Recognition (CNN)

**Implementation:** `src/models/Cnn.py` and `src/part3_ml/train.py`

### Dataset
- GTSRB dataset path: (path)
- Total images: 
- Classes: 43 (traffic sign categories 0–42)
- Train/test split: 80/20

### Model Architecture
- Conv layers: 2 (32 filters, 64 filters)
- Pool layers: 2 (MaxPooling 2×2)
- Dense layers: 1 hidden (128 units) + output (43 units)
- Dropout: 0.25 (conv), 0.50 (dense)
- Activation: ReLU (hidden), Softmax (output)

### Training Hyperparameters
- Epochs: 10
- Batch size: 32
- Learning rate: 0.001 (Adam optimizer)
- Loss: categorical_crossentropy
- Validation split: 10%

### Results

**Test Set Performance**
- Accuracy: (e.g., 0.9535 or 95.35%)
- Precision: (optional, per-class if available)
- Recall: (optional, per-class if available)

**Confusion Matrix**
- Location: `reports/figures/confusion.png`
- Observations: (e.g., which classes are confused)

**Sample Predictions**
- Location: `reports/figures/sample_predictions.png`
- Observations: (e.g., confidence scores, misclassification patterns)

### Training History
| Epoch | Train Accuracy | Val Accuracy |
|-------|----------------|--------------|
| 1     |                |              |
| 5     |                |              |
| 10    |                |              |

### Notes & Observations
- What worked well:
- What didn't work:
- Future improvements:
- Any issues encountered:

---

## Environment & Dependencies

**Python Version:** 3.10+

**Key Packages:**
- tensorflow >= 2.12
- scikit-learn >= 1.0
- opencv-python >= 4.5
- numpy >= 1.20
- pandas >= 1.3
- matplotlib >= 3.4

**Installation:**
```bash
pip install tensorflow opencv-python scikit-learn numpy matplotlib pandas
```

---

## Summary

- Part 1: ✅ / ❌
- Part 2: ✅ / ❌
- Part 3: ✅ / ❌

**Final notes:** (overall project observations)



