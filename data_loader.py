"""Data loader and synthesizer for the Multi-Tool Visualization Dashboard."""

import numpy as np
import pandas as pd


def generate_sample_data(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic but realistic global tech compensation and role data.

    Returns a pandas DataFrame with fields suitable for statistical and interactive
    visualizations across Seaborn, Bokeh, Plotly, and Streamlit.
    """
    np.random.seed(seed)

    job_titles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "Data Engineer",
        "DevOps Engineer",
        "Fullstack Developer",
        "Frontend Developer",
        "Backend Developer",
        "Cloud Architect",
    ]

    experience_levels = ["Entry-level", "Mid-level", "Senior", "Executive"]
    company_sizes = ["Small (<50)", "Medium (50-250)", "Large (>250)"]
    employment_types = ["Full-Time", "Contract", "Part-Time", "Freelance"]
    countries = ["United States", "Germany", "United Kingdom", "Canada", "Spain", "France", "Brazil", "India"]

    base_salaries = {
        "Entry-level": (55000, 15000),
        "Mid-level": (90000, 20000),
        "Senior": (140000, 30000),
        "Executive": (210000, 45000),
    }

    job_multipliers = {
        "Data Scientist": 1.10,
        "Machine Learning Engineer": 1.25,
        "Data Engineer": 1.12,
        "DevOps Engineer": 1.15,
        "Fullstack Developer": 1.00,
        "Frontend Developer": 0.95,
        "Backend Developer": 1.05,
        "Cloud Architect": 1.28,
    }

    records = []
    years = [2021, 2022, 2023, 2024, 2025]

    for i in range(n_samples):
        exp = np.random.choice(experience_levels, p=[0.20, 0.40, 0.32, 0.08])
        job = np.random.choice(job_titles)
        size = np.random.choice(company_sizes, p=[0.25, 0.45, 0.30])
        country = np.random.choice(countries)
        year = int(np.random.choice(years, p=[0.10, 0.15, 0.25, 0.30, 0.20]))
        remote_ratio = int(np.random.choice([0, 50, 100], p=[0.20, 0.30, 0.50]))

        base_mean, base_std = base_salaries[exp]
        multiplier = job_multipliers[job]
        country_factor = 1.0 if country == "United States" else (0.85 if country in ["Germany", "United Kingdom", "Canada"] else 0.65)
        year_inflation = 1.0 + (year - 2021) * 0.04

        salary = int(np.clip(
            np.random.normal(base_mean, base_std) * multiplier * country_factor * year_inflation,
            25000,
            420000,
        ))

        work_life_balance = round(float(np.clip(np.random.normal(3.8, 0.7), 1.0, 5.0)), 1)
        tech_stack_satisfaction = round(float(np.clip(np.random.normal(4.1, 0.6), 1.0, 5.0)), 1)

        records.append({
            "id": i + 1,
            "work_year": year,
            "job_title": job,
            "experience_level": exp,
            "employment_type": np.random.choice(employment_types, p=[0.88, 0.06, 0.03, 0.03]),
            "salary_usd": salary,
            "company_country": country,
            "company_size": size,
            "remote_ratio": remote_ratio,
            "work_life_balance": work_life_balance,
            "tech_satisfaction": tech_stack_satisfaction,
        })

    return pd.DataFrame(records)


def filter_data(
    df: pd.DataFrame,
    years: list[int] | None = None,
    experience_levels: list[str] | None = None,
    job_titles: list[str] | None = None,
    remote_options: list[int] | None = None,
) -> pd.DataFrame:
    """Filter DataFrame based on user selections."""
    filtered = df.copy()

    if years:
        filtered = filtered[filtered["work_year"].isin(years)]
    if experience_levels:
        filtered = filtered[filtered["experience_level"].isin(experience_levels)]
    if job_titles:
        filtered = filtered[filtered["job_title"].isin(job_titles)]
    if remote_options is not None and len(remote_options) > 0:
        filtered = filtered[filtered["remote_ratio"].isin(remote_options)]

    return filtered
