from __future__ import annotations

import csv
import shutil
from pathlib import Path

import cv2
import numpy as np


NUM_CLASSES = 43


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_demo_flight_data(root: Path) -> Path:
    """Create a small directed flight graph for repeatable BFS evaluation."""
    data_dir = root / "data" / "demo_flights"
    data_dir.mkdir(parents=True, exist_ok=True)

    cities = [
        {"city_id": "1", "city_name": "Windhoek", "country": "Namibia"},
        {"city_id": "2", "city_name": "Johannesburg", "country": "South Africa"},
        {"city_id": "3", "city_name": "Nairobi", "country": "Kenya"},
        {"city_id": "4", "city_name": "Cairo", "country": "Egypt"},
        {"city_id": "5", "city_name": "Lagos", "country": "Nigeria"},
        {"city_id": "6", "city_name": "Kigali", "country": "Rwanda"},
    ]
    airlines = [
        {"airline_id": "A1", "airline_name": "Air Demo One"},
        {"airline_id": "A2", "airline_name": "Air Demo Two"},
        {"airline_id": "A3", "airline_name": "Air Demo Three"},
    ]
    flights = [
        {"flight_id": "101", "source_city_id": "1", "destination_city_id": "2", "airline_id": "A1"},
        {"flight_id": "102", "source_city_id": "2", "destination_city_id": "3", "airline_id": "A1"},
        {"flight_id": "103", "source_city_id": "3", "destination_city_id": "4", "airline_id": "A1"},
        {"flight_id": "104", "source_city_id": "1", "destination_city_id": "6", "airline_id": "A2"},
        {"flight_id": "105", "source_city_id": "6", "destination_city_id": "3", "airline_id": "A2"},
        {"flight_id": "106", "source_city_id": "2", "destination_city_id": "5", "airline_id": "A3"},
        {"flight_id": "107", "source_city_id": "5", "destination_city_id": "4", "airline_id": "A3"},
        {"flight_id": "108", "source_city_id": "3", "destination_city_id": "5", "airline_id": "A3"},
        {"flight_id": "109", "source_city_id": "5", "destination_city_id": "6", "airline_id": "A2"},
    ]

    _write_csv(data_dir / "cities.csv", ["city_id", "city_name", "country"], cities)
    _write_csv(data_dir / "airlines.csv", ["airline_id", "airline_name"], airlines)
    _write_csv(
        data_dir / "flights.csv",
        ["flight_id", "source_city_id", "destination_city_id", "airline_id"],
        flights,
    )
    return data_dir


def generate_demo_staff_data(root: Path) -> Path:
    """Create a small nurse roster with light leave constraints."""
    data_dir = root / "data" / "demo_staff"
    data_dir.mkdir(parents=True, exist_ok=True)
    staff_file = data_dir / "staff_small.txt"
    staff_file.write_text(
        "\n".join(
            [
                "Alice,0",
                "Bob,Tuesday",
                "Carol,Wednesday",
                "David,Friday",
                "Eve,Saturday",
                "Frank,Monday",
                "Grace,Thursday",
                "Hannah,Sunday",
                "Ian,0",
                "Jade,0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return staff_file


def _class_color(label: int) -> tuple[int, int, int]:
    return (
        int((label * 37) % 200 + 30),
        int((label * 67) % 200 + 30),
        int((label * 97) % 200 + 30),
    )


def _draw_shape(image: np.ndarray, label: int, variant: int) -> np.ndarray:
    canvas = image.copy()
    accent = tuple(255 - x for x in _class_color(label))
    jitter = variant % 4

    if label % 4 == 0:
        cv2.circle(canvas, (15, 15), 7 + jitter, accent, 2)
    elif label % 4 == 1:
        cv2.rectangle(canvas, (6 + jitter, 6), (24, 24 - jitter), accent, 2)
    elif label % 4 == 2:
        points = np.array([[15, 4 + jitter], [4, 24], [26, 24]], dtype=np.int32)
        cv2.polylines(canvas, [points], isClosed=True, color=accent, thickness=2)
    else:
        cv2.line(canvas, (4, 4 + jitter), (26, 26), accent, 2)
        cv2.line(canvas, (26, 4 + jitter), (4, 26), accent, 2)

    label_text = str(label)
    cv2.putText(
        canvas,
        label_text,
        (1, 28 - jitter),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        accent,
        1,
        cv2.LINE_AA,
    )
    return canvas


def generate_demo_gtsrb(root: Path, images_per_class: int = 12, seed: int = 42) -> Path:
    """Generate a tiny synthetic traffic-sign dataset for pipeline validation."""
    data_dir = root / "data" / "demo_gtsrb"
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)

    for label in range(NUM_CLASSES):
        class_dir = data_dir / str(label)
        class_dir.mkdir(parents=True, exist_ok=True)
        base_color = np.full((30, 30, 3), _class_color(label), dtype=np.uint8)

        for index in range(images_per_class):
            image = _draw_shape(base_color, label, index)
            noise = rng.integers(-18, 19, size=image.shape, dtype=np.int16)
            noisy = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            blur = cv2.GaussianBlur(noisy, (3, 3), 0)
            cv2.imwrite(str(class_dir / f"{index:03d}.png"), blur)

    return data_dir
