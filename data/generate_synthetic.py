"""Deterministic synthetic student enrollment data generator.

Run directly:
    python data/generate_synthetic.py

Output: data/students.csv (5,000 rows, fixed seed = 42)
"""
from __future__ import annotations

import random
from pathlib import Path

import polars as pl

SEED = 42
NUM_STUDENTS = 5_000

COLLEGES: list[str] = [
    "Liberal Arts",
    "Engineering",
    "Business",
    "Education",
    "Natural Sciences",
    "Health Professions",
]

PROGRAMS: dict[str, list[str]] = {
    "Liberal Arts": ["English", "History", "Philosophy", "Political Science"],
    "Engineering": [
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
    ],
    "Business": ["Accounting", "Finance", "Management", "Marketing"],
    "Education": ["Early Childhood", "Secondary Education", "Special Education"],
    "Natural Sciences": ["Biology", "Chemistry", "Mathematics", "Physics"],
    "Health Professions": ["Nursing", "Pre-Medicine", "Public Health", "Kinesiology"],
}

CLASSIFICATIONS: list[str] = ["Freshman", "Sophomore", "Junior", "Senior"]
TERMS: list[str] = ["Fall2023", "Spring2024", "Fall2024", "Spring2025"]

_GPA_BASE: dict[str, float] = {
    "Freshman": 2.5,
    "Sophomore": 2.7,
    "Junior": 2.9,
    "Senior": 3.0,
}

_CREDIT_TARGET: dict[str, int] = {
    "Freshman": 15,
    "Sophomore": 15,
    "Junior": 16,
    "Senior": 14,
}


def _gpa(classification: str, rng: random.Random) -> float:
    raw = rng.gauss(_GPA_BASE[classification], 0.6)
    return round(max(0.0, min(4.0, raw)), 2)


def _credit_hours(classification: str, rng: random.Random) -> tuple[int, int]:
    attempted = max(9, min(19, round(rng.gauss(_CREDIT_TARGET[classification], 2))))
    if rng.random() > 0.1:
        earned = attempted
    else:
        earned = round(attempted * rng.uniform(0.5, 0.9))
    return attempted, earned


def generate(output_path: Path) -> None:
    rng = random.Random(SEED)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    student_ids: list[int] = []
    terms: list[str] = []
    colleges: list[str] = []
    programs: list[str] = []
    classifications: list[str] = []
    gpas: list[float] = []
    attempted_list: list[int] = []
    earned_list: list[int] = []
    enrolled_list: list[bool] = []
    retained_list: list[bool] = []

    for i in range(NUM_STUDENTS):
        college = rng.choice(COLLEGES)
        program = rng.choice(PROGRAMS[college])
        classification = rng.choice(CLASSIFICATIONS)
        term = rng.choice(TERMS)
        gpa = _gpa(classification, rng)
        attempted, earned = _credit_hours(classification, rng)

        # Retention probability increases with GPA; students below 2.0 never retained
        retention_prob = 0.55 + (gpa / 4.0) * 0.35
        retained = gpa >= 2.0 and rng.random() < retention_prob

        student_ids.append(10_000_001 + i)
        terms.append(term)
        colleges.append(college)
        programs.append(program)
        classifications.append(classification)
        gpas.append(gpa)
        attempted_list.append(attempted)
        earned_list.append(earned)
        enrolled_list.append(True)
        retained_list.append(retained)

    df = pl.DataFrame(
        {
            "student_id": student_ids,
            "term": terms,
            "college": colleges,
            "program": programs,
            "classification": classifications,
            "gpa": gpas,
            "credit_hours_attempted": attempted_list,
            "credit_hours_earned": earned_list,
            "enrolled": enrolled_list,
            "retained_next_term": retained_list,
        }
    )

    df.write_csv(output_path)
    print(f"Wrote {len(df):,} records → {output_path}")


if __name__ == "__main__":
    generate(Path(__file__).parent / "students.csv")
