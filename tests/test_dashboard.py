"""Unit tests for the Multi-Tool Visualization Dashboard."""

import sys
from pathlib import Path

# Ensure root directory is in python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from data_loader import generate_sample_data, filter_data


def test_generate_sample_data_columns_and_size():
    df = generate_sample_data(n_samples=100, seed=42)
    assert len(df) == 100
    expected_cols = [
        "id",
        "work_year",
        "job_title",
        "experience_level",
        "employment_type",
        "salary_usd",
        "company_country",
        "company_size",
        "remote_ratio",
        "work_life_balance",
        "tech_satisfaction",
    ]
    for col in expected_cols:
        assert col in df.columns


def test_generate_sample_data_ranges():
    df = generate_sample_data(n_samples=200, seed=99)
    assert df["salary_usd"].min() >= 25000
    assert df["salary_usd"].max() <= 450000
    assert set(df["work_year"].unique()).issubset({2021, 2022, 2023, 2024, 2025})
    assert set(df["remote_ratio"].unique()).issubset({0, 50, 100})


def test_filter_data_by_year_and_experience():
    df = generate_sample_data(n_samples=300, seed=42)
    filtered = filter_data(df, years=[2023, 2024], experience_levels=["Senior"])
    assert len(filtered) > 0
    assert set(filtered["work_year"].unique()).issubset({2023, 2024})
    assert set(filtered["experience_level"].unique()) == {"Senior"}


def test_filter_data_empty():
    df = generate_sample_data(n_samples=50, seed=7)
    filtered = filter_data(df)
    assert len(filtered) == len(df)
