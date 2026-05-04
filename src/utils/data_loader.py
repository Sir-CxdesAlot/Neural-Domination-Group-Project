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
_VALID_DAYS = {
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",
}


def _require_file(path: str) -> None:
    """Raise a clear error when an expected input file is missing."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Required data file not found: {path}")


def _require_columns(reader: csv.DictReader, required: set[str], path: str) -> None:
    """Validate that a CSV file has the columns required by its loader."""
    fieldnames = set(reader.fieldnames or [])
    missing = sorted(required - fieldnames)
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"{path} is missing required column(s): {joined}")


def _required_value(row: dict, column: str, path: str, line_num: int) -> str:
    """Read and trim a required CSV value, rejecting blank values."""
    value = (row.get(column) or "").strip()
    if not value:
        raise ValueError(f"{path}:{line_num} has a blank value for {column!r}")
    return value


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
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Flight data directory not found: {directory}")

    names    : dict[str, set]  = {}
    cities   : dict[str, dict] = {}
    airlines : dict[str, str]  = {}

    # ── cities.csv ────────────────────────────────────────────────────────────
    _cities_path = os.path.join(directory, "cities.csv")
    _require_file(_cities_path)
    with open(_cities_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _require_columns(reader, {"city_id", "city_name", "country"}, _cities_path)
        for row in reader:
            cid   = _required_value(row, "city_id", _cities_path, reader.line_num)
            cname = _required_value(row, "city_name", _cities_path, reader.line_num)
            cntry = _required_value(row, "country", _cities_path, reader.line_num)

            if cid in cities:
                raise ValueError(f"{_cities_path}:{reader.line_num} duplicates city_id {cid!r}")

            cities[cid] = {"name": cname, "country": cntry, "flights": set()}
            names.setdefault(cname.lower(), set()).add(cid)

    # ── airlines.csv ──────────────────────────────────────────────────────────
    _airlines_path = os.path.join(directory, "airlines.csv")
    _require_file(_airlines_path)
    with open(_airlines_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _require_columns(reader, {"airline_id", "airline_name"}, _airlines_path)
        for row in reader:
            airline_id = _required_value(row, "airline_id", _airlines_path, reader.line_num)
            airline_name = _required_value(row, "airline_name", _airlines_path, reader.line_num)

            if airline_id in airlines:
                raise ValueError(
                    f"{_airlines_path}:{reader.line_num} duplicates airline_id {airline_id!r}"
                )
            airlines[airline_id] = airline_name

    # ── flights.csv ───────────────────────────────────────────────────────────
    _flights_path = os.path.join(directory, "flights.csv")
    _require_file(_flights_path)
    with open(_flights_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _require_columns(
            reader,
            {"flight_id", "source_city_id", "destination_city_id", "airline_id"},
            _flights_path,
        )
        seen_flights: set[str] = set()
        for row in reader:
            fid = _required_value(row, "flight_id", _flights_path, reader.line_num)
            src = _required_value(row, "source_city_id", _flights_path, reader.line_num)
            dst = _required_value(row, "destination_city_id", _flights_path, reader.line_num)
            airline_id = _required_value(row, "airline_id", _flights_path, reader.line_num)

            if fid in seen_flights:
                raise ValueError(f"{_flights_path}:{reader.line_num} duplicates flight_id {fid!r}")
            if src not in cities:
                raise ValueError(
                    f"{_flights_path}:{reader.line_num} references unknown source_city_id {src!r}"
                )
            if dst not in cities:
                raise ValueError(
                    f"{_flights_path}:{reader.line_num} references unknown destination_city_id {dst!r}"
                )
            if airline_id not in airlines:
                raise ValueError(
                    f"{_flights_path}:{reader.line_num} references unknown airline_id {airline_id!r}"
                )

            seen_flights.add(fid)
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

    _require_file(filepath)
    with open(filepath, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts    = [p.strip() for p in line.replace("\t", ",").split(",")]
            name     = parts[0]

            if not name:
                raise ValueError(f"{filepath}:{line_num} has a blank nurse name")
            if name in leave:
                raise ValueError(f"{filepath}:{line_num} duplicates nurse name {name!r}")

            days_off = set()
            for raw_day in parts[1:]:
                if not raw_day or raw_day == "0":
                    continue
                day = _VALID_DAYS.get(raw_day.lower())
                if day is None:
                    valid = ", ".join(_VALID_DAYS.values())
                    raise ValueError(
                        f"{filepath}:{line_num} has invalid leave day {raw_day!r}; "
                        f"expected one of: {valid}, or 0 for no leave"
                    )
                days_off.add(day)

            nurses.append(name)
            leave[name] = days_off

    if not nurses:
        raise ValueError(f"No staff records found in {filepath}")

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
    if img_size <= 0:
        raise ValueError("img_size must be greater than 0")
    if num_classes <= 0:
        raise ValueError("num_classes must be greater than 0")

    if not _CV2_AVAILABLE:
        raise ImportError(
            "OpenCV and NumPy are required for Part 3.\n"
            "Install them with:  pip install opencv-python numpy"
        )
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"GTSRB data directory not found: {data_dir}")

    images = []
    labels = []

    for label in range(num_classes):
        category_path = os.path.join(data_dir, str(label))
        if not os.path.isdir(category_path):
            print(f"  [warn] Folder not found: {category_path} - skipping.")
            continue

        loaded = 0
        for fname in sorted(os.listdir(category_path)):
            fpath = os.path.join(category_path, fname)
            if not os.path.isfile(fpath):
                continue
            img   = cv2.imread(fpath)
            if img is None:
                continue
            img = cv2.resize(img, (img_size, img_size))
            images.append(img)
            labels.append(label)
            loaded += 1

        print(f"  Loaded {loaded:>5} images  <- category {label:>2}")

    if not images:
        raise ValueError(f"No readable images found in {data_dir}")

    images_arr = np.asarray(images, dtype="float32") / 255.0
    labels_arr = np.asarray(labels, dtype="int32")

    return images_arr, labels_arr
