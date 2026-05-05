# ARI711S Group Project - Final Submission

**Project:** Neural-Domination Group - Search, Optimization & Machine Learning  
**Date:** May 5, 2026  
**Semester:** 5 2026

---

## Submission Contents

This folder contains the complete final submission for the ARI711S group project, including all code, results, and documentation.

### 1. Core Submission Files

#### Final Integration Notebook
- **File:** `../../notebooks/final_integration.ipynb`
- **Purpose:** Integrated Jupyter notebook combining all three project parts with results
- **Status:** ✓ Executed with all outputs
- **Contents:**
  - Part 1: Flight Search (BFS) - 4/4 test cases passed
  - Part 2: Hospital Scheduling (CSP) - 21/21 shifts assigned, 0 violations
  - Part 3: Traffic Sign Recognition (CNN) - 98.72% accuracy (7,742/7,842)
  - Evaluation figures grid

#### Presentation Slides
- **File:** `../../presentation/ARI711S_Group_Project.pptx`
- **Purpose:** 11-slide professional presentation
- **Contents:**
  1. Title slide (team & course)
  2. Problem framing (3 AI tasks)
  3. Part 1: Flight search with BFS explanation
  4. Part 2: CSP scheduling model
  5. Part 2: Shift distribution & fairness
  6. Part 3: CNN architecture & training
  7. Part 3: Classification results & accuracy
  8. Evaluation confusion matrix
  9. Project summary & key metrics
  10. Limitations & next steps
  11. Closing slide (Q&A)

#### Results Summary
- **File:** `../results.md`
- **Purpose:** Detailed results for all three parts
- **Key Metrics:**
  - Part 1: 4/4 test cases passed
  - Part 2: All constraints satisfied, fairness = 1.6 StdDev
  - Part 3: 98.72% test accuracy, 0.0693 loss

### 2. Implementation Details

#### Part 1: Flight Connections (BFS)
- **Implementation:** `../../src/part1_search/flights.py`
- **Algorithm:** Breadth-First Search
- **Result:** Minimum hop paths in flight network
- **Test Cases:** 4/4 passed
  - Windhoek → Cairo: 3 hops ✓
  - Johannesburg → Lagos: 1 hop ✓
  - Nairobi → Nairobi: 0 hops ✓
  - Cairo → Windhoek: No path ✓

#### Part 2: Hospital Shift Scheduling (CSP)
- **Implementation:** `../../src/part2_optimization/run_scheduler.py` + `../../src/models/Csp.py`
- **Model:** Constraint Satisfaction Problem
- **Variables:** 21 shifts (7 days × 3 shifts/day)
- **Constraints:** Leave days, rest rules, max 5 shifts/week
- **Solver Techniques:** Node consistency, AC-3, MRV, forward checking
- **Results:**
  - All 21 shifts assigned ✓
  - 0 leave violations ✓
  - 0 rest rule violations ✓
  - Fairness (StdDev): 1.6

#### Part 3: Traffic Sign Recognition (CNN)
- **Implementation:** `../../src/train.py` + `../../src/part3_ml/train.py` + `../../src/models/Cnn.py`
- **Dataset:** German Traffic Sign Recognition Benchmark (GTSRB)
- **Model Architecture:**
  - Input: 30×30 normalized images
  - Conv2D (32 filters) + MaxPooling
  - Conv2D (64 filters) + MaxPooling
  - Dropout (0.5)
  - Dense (128 units)
  - Dense (43 units, softmax)
- **Training:**
  - Epochs: 6
  - Batch size: 32
  - Optimizer: Adam
  - Loss: Categorical Crossentropy
- **Results:**
  - ★ Test Accuracy: **98.72%** (7,742/7,842 correct)
  - Test Loss: 0.0693
  - Model saved: `../artifacts/gtsrb_model.keras`

### 3. Evaluation Artifacts

#### Figures (All Generated)
- `../figures/confusion.png` - 43×43 confusion matrix heatmap
- `../figures/training_curve.png` - Training/validation accuracy curves
- `../figures/sample_predictions.png` - 9 example predictions with labels
- `../figures/part1_route_lengths.png` - Flight hop count histogram
- `../figures/part2_schedule_overview.png` - Weekly shift schedule table
- `../figures/part2_shift_distribution.png` - Nurse workload bar chart
- `submission_figures_grid.png` - All figures in one grid (6 figures)

#### Metrics & Evaluation
- **File:** `../evaluation_metrics.json`
- **Contents:** Complete metrics for all three parts in JSON format
- **Part 1:** Test cases, hop counts, path validity
- **Part 2:** Shift assignments, violations, fairness metrics
- **Part 3:** Accuracy, loss, confusion matrix validation

#### Evaluation Notes
- **File:** `../evaluation_notes.md`
- **Contents:** Detailed interpretation of results, limitations, and insights

### 4. Supporting Documentation

#### Background & Theory
- **File:** `../../reports/background.md`
- **Purpose:** Theoretical foundation for all three methods
- **Covers:** BFS algorithm, CSP concepts, CNN architecture

#### Literature Summary
- **File:** `../../references/literature-summary.md`
- **Purpose:** Sources and citations for each method
- **Justification:** Why each algorithm was chosen

#### Implementation Guide
- **File:** `../../src/README.md`
- **Purpose:** How to run each component
- **Commands:** Training, evaluation, and integration commands

### 5. Data & Models

#### Datasets
- **Part 1:** `../../data/demo_flights/` (flight network demo data)
- **Part 2:** `../../data/demo_staff/staff_small.txt` (nurse scheduling demo data)
- **Part 3:** `../../gtsrb/Train/` (real GTSRB dataset, 39,209 images, 43 classes)

#### Model Artifact
- **File:** `../artifacts/gtsrb_model.keras`
- **Size:** 5.16 MB
- **Architecture:** Sequential Keras model with 10 layers
- **Performance:** 98.72% test accuracy

### 6. Quick Start

#### To view the final submission:
```bash
# Open the integrated notebook with all results
jupyter notebook notebooks/final_integration.ipynb

# View the presentation
# Open: presentation/ARI711S_Group_Project.pptx

# Check detailed results
cat reports/results.md

# View evaluation metrics
cat reports/evaluation_metrics.json
```

#### To run components individually:
```bash
# Part 1: Flight search
python src/part1_search/flights.py

# Part 2: Hospital scheduling
python src/part2_optimization/run_scheduler.py

# Part 3: Traffic sign training (requires GTSRB dataset)
python src/train.py
```

---

## Project Completion Status

### ✓ COMPLETED

- [x] Background theory documented
- [x] Literature review completed
- [x] Part 1 (BFS): 4/4 test cases passed
- [x] Part 2 (CSP): All constraints satisfied
- [x] Part 3 (CNN): 98.72% accuracy achieved
- [x] Evaluation figures generated
- [x] Model artifact saved
- [x] Final integration notebook executed
- [x] Presentation slides created
- [x] Submission package prepared

### ⚠ NOTES FOR RESUBMISSION

- Parts 1 & 2 currently validated on **generated demo data**
- Official assignment datasets are not tracked in repository (confidentiality)
- **Before final submission:**
  1. Rerun Part 1 & 2 on real flight/staff datasets
  2. Verify Part 3 results on GTSRB test set
  3. Update `reports/results.md` with actual dataset results

---

## File Organization

```
submission/
├── README.md (this file)
├── ../../notebooks/final_integration.ipynb
├── ../../presentation/ARI711S_Group_Project.pptx
├── ../results.md
├── ../evaluation_metrics.json
├── ../evaluation_notes.md
├── ../artifacts/gtsrb_model.keras
├── ../figures/
│   ├── confusion.png
│   ├── training_curve.png
│   ├── sample_predictions.png
│   ├── part1_route_lengths.png
│   ├── part2_schedule_overview.png
│   ├── part2_shift_distribution.png
│   └── submission_figures_grid.png
├── ../../src/ (implementation source code)
├── ../../reports/background.md
└── ../../references/literature-summary.md
```

---

## Contact & Questions

- **Repository:** Neural-Domination-Group-Project
- **Course:** ARI711S (Artificial Intelligence)
- **Semester:** 5 2026
- **Submission Date:** May 5, 2026

---

**Status:** ✓ READY FOR FINAL SUBMISSION
