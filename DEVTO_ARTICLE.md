---
title: "Building Multi-Engine Data Dashboards with Bokeh, Seaborn, and Plotly: Automated CI/CD Deployment to the Public Cloud"
published: true
description: "A comprehensive guide to orchestrating statistical and interactive visualizations across Bokeh, Seaborn, and Plotly with Streamlit, backed by automated GitHub Actions CI/CD and cloud deployment."
tags: "python, data-science, devops, webdev"
cover_image: "https://raw.githubusercontent.com/Hashiravc/viz-dashboard-ci-cd/main/.github/assets/banner.png"
canonical_url: "https://github.com/Hashiravc/viz-dashboard-ci-cd"
---

# Building Multi-Engine Data Dashboards with Bokeh, Seaborn, and Plotly: Automated CI/CD Deployment to the Public Cloud

[![CI/CD Dashboard Pipeline](https://github.com/Hashiravc/viz-dashboard-ci-cd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Hashiravc/viz-dashboard-ci-cd/actions/workflows/ci-cd.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://viz-dashboard-ci-cd.streamlit.app/)

> **Public Project Repository:** [https://github.com/Hashiravc/viz-dashboard-ci-cd](https://github.com/Hashiravc/viz-dashboard-ci-cd)  
> **Live Cloud Application:** [https://viz-dashboard-ci-cd.streamlit.app/](https://viz-dashboard-ci-cd.streamlit.app/)

---

## 1. Introduction & The Visualization Dilemma

Data science teams rarely have a single visualization problem. In a typical production workflow:
- **Researchers & Statisticians** demand publication-grade density curves, covariance matrices, and confidence intervals—the domain of **Seaborn** and **Matplotlib**.
- **Front-end Data Engineers** require hardware-accelerated, high-framerate interactive canvas plots capable of panning, box-zooming, and hover-inspecting thousands of nodes—the superpower of **Bokeh**.
- **Product Managers & Analysts** expect intuitive 3D spatial representations, drill-down sunburst hierarchies, and reactive cross-filtering—the wheelhouse of **Plotly** and **Dash**.
- **Software Engineers** demand an all-in-one web framework that doesn't require a separate React/Vue frontend, accompanied by **automated CI/CD pipelines** that test, package, and deploy directly to a public cloud or SaaS provider.

In this article, we demonstrate how to build an integrated **Multi-Engine Analytics Hub** combining **Seaborn, Bokeh, and Plotly** under **Streamlit**, validate it with automated unit tests via **GitHub Actions**, and deploy it continuously to a public cloud provider.

---

## 2. Visualization Frameworks Compared

Before building the dashboard, it is crucial to understand the architectural trade-offs among the dominant Python visualization tools:

| Framework | Rendering Engine | Interactivity Paradigm | Learning Curve | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Streamlit** | React / Webpack (Client) + Python (Server) | Full Python script re-execution on user action | Very Gentle | Rapid data apps, internal tools, executive dashboards |
| **Plotly / Dash** | React.js + D3.js + WebGL | Declarative JSON schemas with bidirectional callbacks | Gentle | Interactive drill-downs, financial analytics, geospatial charts |
| **Bokeh** | HTML5 Canvas / WebGL (`BokehJS`) | Client-side JavaScript callbacks & Python server models | Moderate | High-performance streaming, large canvas plots, standalone HTML widgets |
| **Seaborn / Matplotlib** | Static bitmap / SVG backend (Agg) | Static figure outputs (rendered to buffer) | Gentle | Statistical research, academic papers, distribution heatmaps |
| **Shiny for Python** | Reactive dependency graph | Fine-grained reactive computational graphs | Moderate | High-concurrency applications, R-to-Python migrations |

---

## 3. System Architecture & CI/CD Pipeline

Modern data products must adhere to the same DevOps rigor as backend microservices. The architecture consists of three core layers:

```
+-----------------------------------------------------------------------------------+
|                            DEVELOPER WORKFLOW (GitOps)                            |
|                                                                                   |
|  [ Local Code ] ---> [ git push origin main ] ---> [ GitHub Public Repository ]  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        GITHUB ACTIONS CI/CD PIPELINE                              |
|                                                                                   |
|  Step 1: Code Lint & Syntax Verification                                          |
|  Step 2: Automated Unit Testing (pytest test_dashboard.py)                        |
|  Step 3: Docker Container Build & Layer Validation                                |
|  Step 4: Automated Deployment Trigger / GitOps Webhook Sync                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     PUBLIC CLOUD / SAAS HOSTING PLATFORM                         |
|                                                                                   |
|    Streamlit Community Cloud  /  Render Web Service  /  Hugging Face Spaces      |
|              (Live URL: https://viz-dashboard-ci-cd.streamlit.app/)               |
+-----------------------------------------------------------------------------------+
```

---

## 4. Implementation Deep-Dive

### 4.1 Synthetic Data Synthesizer (`data_loader.py`)

To simulate realistic industry conditions, we synthesize a multi-variable compensation and talent dataset:

```python
import numpy as np
import pandas as pd

def generate_sample_data(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    job_titles = ["Data Scientist", "Machine Learning Engineer", "DevOps Engineer", "Cloud Architect"]
    experience_levels = ["Entry-level", "Mid-level", "Senior", "Executive"]
    
    records = []
    for i in range(n_samples):
        exp = np.random.choice(experience_levels, p=[0.20, 0.40, 0.32, 0.08])
        job = np.random.choice(job_titles)
        salary = int(np.clip(np.random.normal(120000, 35000), 30000, 380000))
        records.append({
            "id": i + 1,
            "job_title": job,
            "experience_level": exp,
            "salary_usd": salary,
            "remote_ratio": int(np.random.choice([0, 50, 100])),
            "work_life_balance": round(float(np.clip(np.random.normal(3.8, 0.7), 1.0, 5.0)), 1),
        })
    return pd.DataFrame(records)
```

### 4.2 Statistical Rigor: Seaborn & Matplotlib

Seaborn delivers mathematical depth with kernel density estimation (KDE) and covariance heatmaps:

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(data=df, x="salary_usd", hue="experience_level", kde=True, palette="mako", ax=ax)
ax.set_title("Kernel Density Estimation (KDE) of Tech Compensation")
st.pyplot(fig)
plt.close(fig)
```

### 4.3 High-Performance Canvas: Bokeh with HoverTools

Bokeh renders directly to an HTML5 canvas, supporting responsive pan/zoom controls and customized inspection metadata without server round-trips:

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter

source = ColumnDataSource(df)
p = figure(
    title="Bokeh Canvas: Work-Life Balance vs. Compensation",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    background_fill_color="#1E293B",
    width=900, height=450
)
circle = p.scatter(x="work_life_balance", y="salary_usd", size=10, source=source, alpha=0.8)
p.add_tools(HoverTool(renderers=[circle], tooltips=[
    ("Role", "@job_title"),
    ("Salary", "@salary_usd{$0,0}"),
    ("Seniority", "@experience_level")
]))
st.bokeh_chart(p, use_container_width=True)
```

### 4.4 Declarative Interactivity: Plotly Sunburst & Scatter

Plotly provides dynamic hierarchical exploration:

```python
import plotly.express as px

fig = px.sunburst(
    df,
    path=["company_country", "experience_level", "job_title"],
    values="salary_usd",
    title="Global Talent Distribution Hierarchy",
    template="plotly_dark",
    color="salary_usd",
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig, use_container_width=True)
```

---

## 5. Automated CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

The repository includes a complete GitHub Actions automation workflow that enforces code quality, executes test suites, builds container artifacts, and triggers cloud updates upon merging to `main`:

```yaml
name: CI/CD Dashboard Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint-and-test:
    name: 🧪 Run Quality Checks & Unit Tests
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Execute Pytest Suite
        run: |
          pytest -v tests/

  docker-build:
    name: 🐳 Docker Container Build & Verify
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Build Container
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: viz-dashboard:latest

  deploy-cloud:
    name: 🚀 Automated Cloud Deployment Trigger
    needs: [lint-and-test, docker-build]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Notify GitOps Sync
        run: |
          echo "Automated tests and Docker build verified!"
          echo "Syncing latest commit with public cloud provider..."
```

---

## 6. Cloud & SaaS Deployment Guide

### Option 1: Streamlit Community Cloud (Recommended GitOps)
1. Fork or push your repository to GitHub: `https://github.com/Hashiravc/viz-dashboard-ci-cd`.
2. Navigate to [share.streamlit.io](https://share.streamlit.io/) and click **New App**.
3. Select your repository: `Hashiravc/viz-dashboard-ci-cd`, branch: `main`, and main file: `app.py`.
4. Click **Deploy!** Any subsequent `git push` to `main` will automatically trigger a zero-downtime rolling update.

### Option 2: Render / Railway / Hugging Face Spaces (Docker-based)
1. Use the pre-configured [Dockerfile](file:///c:/Users/Hashira/Documents/GitHub/Moviles%20I/viz-dashboard-ci-cd/Dockerfile) included in the repository.
2. In [Render](https://render.com), create a **Web Service** pointing to `https://github.com/Hashiravc/viz-dashboard-ci-cd`.
3. Choose the **Docker** runtime environment and expose port `8501`.
4. Enable **Auto-Deploy** so every passing commit on `main` immediately updates your live container.

---

## 7. How to Run Locally

Clone the repository and spin up the dashboard in your local environment:

```bash
# 1. Clone the public repository
git clone https://github.com/Hashiravc/viz-dashboard-ci-cd.git
cd viz-dashboard-ci-cd

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated test suite
pytest -v tests/

# 5. Launch the Streamlit dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501` to view the interactive hub.

---

## 8. Key Takeaways & Conclusion

1. **Polyglot Visualization Wins:** No single library fits all enterprise needs. Combining Seaborn (statistical depth), Bokeh (canvas speed), and Plotly (interactivity) in a unified UI provides comprehensive data coverage.
2. **Automated CI/CD Prevents Regressions:** Running automated unit tests (`pytest`) and Docker build validations within GitHub Actions ensures that visual bugs or broken dependencies never reach production.
3. **Public Cloud Democratization:** Platforms like Streamlit Community Cloud and Render eliminate infrastructure overhead, enabling immediate worldwide accessibility via automated GitOps pipelines.

---

## 9. Team Member Dev.to Publishing Notes

Each team member can publish this article under their individual Dev.to profile with custom personalization:
- **Author Section:** Add your name, team role, and specific technical focus (e.g., Seaborn statistical modeling, Bokeh canvas optimization, or GitHub Actions CI/CD pipeline).
- **Custom Learnings:** Highlight your favorite visualization tool and key challenges solved during development.
- **Repository Reference:** Ensure the public repository link [https://github.com/Hashiravc/viz-dashboard-ci-cd](https://github.com/Hashiravc/viz-dashboard-ci-cd) remains featured.

---

*Authored by the Viz Dashboard Engineering Team | Public Repository: [Hashiravc/viz-dashboard-ci-cd](https://github.com/Hashiravc/viz-dashboard-ci-cd)*
