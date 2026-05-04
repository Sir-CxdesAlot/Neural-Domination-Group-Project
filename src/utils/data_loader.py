"""
utils/data_loader.py
====================
Data-loading helpers for all three project parts.

Functions
---------
load_flight_data(directory)  → (names, cities, airlines)   Part 1
load_staff(filepath)         → (nurses, leave)              Part 2
load_gtsrb(data_dir, ...)    → (images, labels)             Part 3
"""

import csv
import os

# ── Part 3 optional deps ──────────────────────────────────────────────────────
try:
    import cv2
    import numpy as np
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

# ── Part 3 constants (mirror models/cnn.py to avoid circular imports) ─────────
_IMG_SIZE    = 30
_NUM_CLASSES = 43


# =============================================================================
# Part 1 – Flight-network loader
# =============================================================================

def load_flight_data(directory: str) -> tuple[dict, dict, dict]:
    """
    Parse the three CSV files that describe a flight-route network.

    Parameters
    ----------
    directory : Path to the folder containing cities.csv, flights.csv,
                and airlines.csv.

    Returns
    -------
    names    : dict  city_name (lowercase) → set of city_ids
    cities   : dict  city_id → {"name": str, "country": str,
                                 "flights": set of (flight_id, dest_city_id)}
    airlines : dict  airline_id → airline_name
    """
    names    : dict[str, set]  = {}
    cities   : dict[str, dict] = {}
    airlines : dict[str, str]  = {}

    # ── cities.csv ────────────────────────────────────────────────────────────
    _cities_path = os.path.join(directory, "cities.csv")
    with open(_cities_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid   = row["city_id"].strip()
            cname = row["city_name"].strip()
            cntry = row["country"].strip()

            cities[cid] = {"name": cname, "country": cntry, "flights": set()}
            names.setdefault(cname.lower(), set()).add(cid)

    # ── airlines.csv ──────────────────────────────────────────────────────────
    _airlines_path = os.path.join(directory, "airlines.csv")
    with open(_airlines_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            airlines[row["airline_id"].strip()] = row["airline_name"].strip()

    # ── flights.csv ───────────────────────────────────────────────────────────
    _flights_path = os.path.join(directory, "flights.csv")
    with open(_flights_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fid = row["flight_id"].strip()
            src = row["source_city_id"].strip()
            dst = row["destination_city_id"].strip()
            if src in cities:
                cities[src]["flights"].add((fid, dst))

    return names, cities, airlines


# =============================================================================
# Part 2 – Staff / leave-day loader
# =============================================================================

def load_staff(filepath: str) -> tuple[list, dict]:
    """
    Parse a staff file listing nurse names and their approved leave days.

    Expected format (comma *or* tab separated, '#' lines are comments):
        Nurse Name, LeaveDay1, LeaveDay2, ...
        (use '0' or leave blank to indicate no leave)

    Parameters
    ----------
    filepath : Path to the staff text file.

    Returns
    -------
    nurses : list[str]        Ordered list of all nurse names.
    leave  : dict[str, set]   nurse → set of day strings when on leave.
    """
    nurses : list[str]       = []
    leave  : dict[str, set]  = {}

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts    = [p.strip() for p in line.replace("\t", ",").split(",")]
            name     = parts[0]
            days_off = {p for p in parts[1:] if p and p != "0"}

            nurses.append(name)
            leave[name] = days_off

    return nurses, leave


# =============================================================================
# Part 3 – GTSRB image loader
# =============================================================================

def load_gtsrb(
    data_dir:    str,
    img_size:    int = _IMG_SIZE,
    num_classes: int = _NUM_CLASSES,
) -> tuple:
    """
    Walk *data_dir* (sub-folders 0 – num_classes-1) and load all images.

    Each image is:
      • read with OpenCV (BGR → kept as-is, consistent with cv2 convention)
      • resized to *img_size* × *img_size*
      • normalised to [0, 1] float32

    Parameters
    ----------
    data_dir    : Root path of the unzipped GTSRB dataset.
    img_size    : Target side length (pixels). Default: 30.
    num_classes : Number of categories to load. Default: 43.

    Returns
    -------
    images : np.ndarray  shape (N, img_size, img_size, 3), float32
    labels : np.ndarray  shape (N,), int32

    Raises
    ------
    ImportError  if OpenCV / NumPy are not installed.
    """
    if not _CV2_AVAILABLE:
        raise ImportError(
            "OpenCV and NumPy are required for Part 3.\n"
            "Install them with:  pip install opencv-python numpy"
        )

    images = []
    labels = []

    for label in range(num_classes):
        category_path = os.path.join(data_dir, str(label))
        if not os.path.isdir(category_path):
            print(f"  [warn] Folder not found: {category_path} — skipping.")
            continue

        loaded = 0
        for fname in os.listdir(category_path):
            fpath = os.path.join(category_path, fname)
            img   = cv2.imread(fpath)
            if img is None:
                continue
            img = cv2.resize(img, (img_size, img_size))
            images.append(img)
            labels.append(label)
            loaded += 1

        print(f"  Loaded {loaded:>5} images  ← category {label:>2}")

    images_arr = np.array(images, dtype="float32") / 255.0
    labels_arr = np.array(labels, dtype="int32")

    return images_arr, labels_arr