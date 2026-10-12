"""Interactive Multi-Tool Data Visualization & Analytics Dashboard.

Demonstrating Bokeh, Seaborn, Matplotlib, Plotly, and Streamlit
with Automated CI/CD and Public Cloud Deployment.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from data_loader import filter_data, generate_sample_data

# Page Configuration
st.set_page_config(
    page_title="Multi-Tool Viz Hub | CI/CD Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.8rem;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #312E81;
        color: #C7D2FE;
        margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_cached_data() -> pd.DataFrame:
    """Load and cache the baseline dataset."""
    return generate_sample_data(n_samples=1500, seed=42)


# Data Acquisition
raw_df = load_cached_data()

# Sidebar Controls
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.markdown("Filter real-time data across all visualization engines.")

selected_years = st.sidebar.multiselect(
    "Work Years",
    options=sorted(raw_df["work_year"].unique()),
    default=sorted(raw_df["work_year"].unique()),
)

selected_exp = st.sidebar.multiselect(
    "Experience Levels",
    options=list(raw_df["experience_level"].unique()),
    default=list(raw_df["experience_level"].unique()),
)

selected_jobs = st.sidebar.multiselect(
    "Job Titles",
    options=sorted(raw_df["job_title"].unique()),
    default=sorted(raw_df["job_title"].unique())[:5],
)

remote_filter = st.sidebar.multiselect(
    "Workplace Arrangement",
    options=[0, 50, 100],
    default=[0, 50, 100],
    format_func=lambda x: "On-site (0%)" if x == 0 else ("Hybrid (50%)" if x == 50 else "Fully Remote (100%)"),
)

st.sidebar.markdown("---")
st.sidebar.info(
    "🚀 **Deployment Info**\n\n"
    "- **Repository**: [GitHub](https://github.com/Hashiravc/viz-dashboard-ci-cd)\n"
    "- **CI/CD**: GitHub Actions\n"
    "- **Cloud Target**: Streamlit Community Cloud / Render"
)

# Apply Filters
df = filter_data(
    raw_df,
    years=selected_years,
    experience_levels=selected_exp,
    job_titles=selected_jobs,
    remote_options=remote_filter,
)

if df.empty:
    st.warning("⚠️ No data available for the current filter selection. Please adjust your filters.")
    st.stop()

# Header Section
st.markdown('<div class="main-header">Multi-Tool Data Visualization & Analytics Hub</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">A comparative architectural showcase of Bokeh, Seaborn, Matplotlib, and Plotly '
    'orchestrated with Streamlit & Automated CI/CD.</div>',
    unsafe_allow_html=True,
)

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", f"{len(df):,}", delta=f"{len(df) - len(raw_df)} from base")
with col2:
    avg_salary = df["salary_usd"].mean()
    st.metric("Mean Salary", f"${avg_salary:,.0f}", delta=f"{((avg_salary/raw_df['salary_usd'].mean()) - 1)*100:.1f}%")
with col3:
    remote_pct = (df["remote_ratio"] == 100).mean() * 100
    st.metric("Fully Remote Adoption", f"{remote_pct:.1f}%")
with col4:
    top_role = df.groupby("job_title")["salary_usd"].mean().idxmax()
    st.metric("Top Earning Role", top_role)

st.markdown("---")

# Main Visualization Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Plotly (Interactive)",
    "🎨 Seaborn & Matplotlib (Statistical)",
    "⚡ Bokeh (Web Canvas)",
    "⚖️ Framework Comparison",
    "🚀 CI/CD & Cloud Architecture",
])

# TAB 1: PLOTLY
with tab1:
    st.subheader("Interactive Exploratory Data Analysis with Plotly")
    st.markdown(
        "Plotly delivers reactive, declarative D3.js-powered visual components with built-in zoom, hover cards, and WebGL rendering."
    )

    pcol1, pcol2 = st.columns(2)

    with pcol1:
        # Salary distribution by role boxplot
        fig_box = px.box(
            df,
            x="job_title",
            y="salary_usd",
            color="experience_level",
            title="Compensation Range by Role & Seniority",
            labels={"salary_usd": "Salary (USD)", "job_title": "Role"},
            template="plotly_dark",
            category_orders={"experience_level": ["Entry-level", "Mid-level", "Senior", "Executive"]},
        )
        fig_box.update_layout(xaxis_tickangle=-45, legend_title_text="Seniority")
        st.plotly_chart(fig_box, use_container_width=True)

    with pcol2:
        # Sunburst hierarchy: Country -> Job Title -> Experience Level
        fig_sunburst = px.sunburst(
            df,
            path=["company_country", "experience_level", "job_title"],
            values="salary_usd",
            title="Global Talent Distribution Hierarchy",
            template="plotly_dark",
            color="salary_usd",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)

    # Remote vs Salary Scatter / Bubble
    fig_scatter = px.scatter(
        df,
        x="work_life_balance",
        y="salary_usd",
        size="tech_satisfaction",
        color="company_size",
        hover_name="job_title",
        facet_col="experience_level",
        title="Work-Life Balance vs. Salary across Seniority Tiers (Bubble Size = Tech Satisfaction)",
        labels={"work_life_balance": "Work-Life Rating (1-5)", "salary_usd": "Annual Compensation ($)"},
        template="plotly_dark",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 2: SEABORN & MATPLOTLIB
with tab2:
    st.subheader("Deep Statistical Analysis with Seaborn & Matplotlib")
    st.markdown(
        "Seaborn specializes in publication-ready, mathematically rigorous distributions, regression models, and covariance matrices."
    )

    scol1, scol2 = st.columns(2)

    with scol1:
        # Density distribution with KDE
        plt.style.use("dark_background")
        fig_sns1, ax1 = plt.subplots(figsize=(8, 5))
        sns.histplot(
            data=df,
            x="salary_usd",
            hue="experience_level",
            kde=True,
            palette="mako",
            alpha=0.4,
            ax=ax1,
        )
        ax1.set_title("Kernel Density Estimation (KDE) of Tech Compensation", fontsize=13, pad=12)
        ax1.set_xlabel("Salary (USD)", fontsize=11)
        ax1.set_ylabel("Frequency", fontsize=11)
        ax1.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
        fig_sns1.patch.set_facecolor("#0F172A")
        ax1.set_facecolor("#1E293B")
        st.pyplot(fig_sns1)
        plt.close(fig_sns1)

    with scol2:
        # Correlation Heatmap
        fig_sns2, ax2 = plt.subplots(figsize=(8, 5))
        numeric_cols = df[["salary_usd", "remote_ratio", "work_life_balance", "tech_satisfaction", "work_year"]]
        corr = numeric_cols.corr()
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="crest",
            vmin=-1,
            vmax=1,
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax2,
        )
        ax2.set_title("Feature Covariance Heatmap", fontsize=13, pad=12)
        fig_sns2.patch.set_facecolor("#0F172A")
        ax2.set_facecolor("#1E293B")
        st.pyplot(fig_sns2)
        plt.close(fig_sns2)

    # Violin Plot for Remote Ratios
    fig_sns3, ax3 = plt.subplots(figsize=(10, 4.5))
    sns.violinplot(
        data=df,
        x="remote_ratio",
        y="salary_usd",
        hue="company_size",
        split=False,
        palette="rocket",
        inner="quartile",
        ax=ax3,
    )
    ax3.set_title("Salary Dispersion Across Remote Modalities & Company Scales", fontsize=13, pad=12)
    ax3.set_xlabel("Remote Percentage (%)", fontsize=11)
    ax3.set_ylabel("Salary (USD)", fontsize=11)
    ax3.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    fig_sns3.patch.set_facecolor("#0F172A")
    ax3.set_facecolor("#1E293B")
    st.pyplot(fig_sns3)
    plt.close(fig_sns3)

# TAB 3: BOKEH
with tab3:
    st.subheader("High-Performance HTML5 Canvas Plotting with Bokeh")
    st.markdown(
        "Bokeh offers browser-optimized interactive data visualization with custom JavaScript callbacks, HoverTools, and canvas hardware acceleration."
    )

    # Prepare ColumnDataSource
    b_df = df.sample(min(len(df), 500), random_state=42).copy()
    b_df["salary_formatted"] = b_df["salary_usd"].apply(lambda x: f"${x:,.0f}")
    source = ColumnDataSource(b_df)

    exp_levels = ["Entry-level", "Mid-level", "Senior", "Executive"]
    colors = ["#38BDF8", "#818CF8", "#F472B6", "#FBBF24"]
    color_map = factor_cmap("experience_level", palette=colors, factors=exp_levels)

    # Bokeh Scatter Figure
    p = figure(
        title="Bokeh Interactive Canvas: Work-Life Balance vs. Annual Compensation",
        x_axis_label="Work-Life Balance Score (1.0 to 5.0)",
        y_axis_label="Salary (USD)",
        width=900,
        height=480,
        tools="pan,wheel_zoom,box_zoom,reset,save",
        background_fill_color="#1E293B",
        border_fill_color="#0F172A",
    )

    p.title.text_color = "#F8FAFC"
    p.title.text_font_size = "13pt"
    p.xaxis.axis_label_text_color = "#94A3B8"
    p.yaxis.axis_label_text_color = "#94A3B8"
    p.xaxis.major_label_text_color = "#E2E8F0"
    p.yaxis.major_label_text_color = "#E2E8F0"
    p.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    p.grid.grid_line_color = "#334155"
    p.grid.grid_line_dash = [6, 4]

    circle_renderer = p.scatter(
        x="work_life_balance",
        y="salary_usd",
        size=10,
        source=source,
        color=color_map,
        alpha=0.8,
        legend_field="experience_level",
    )

    hover = HoverTool(
        renderers=[circle_renderer],
        tooltips=[
            ("Role", "@job_title"),
            ("Seniority", "@experience_level"),
            ("Country", "@company_country"),
            ("Salary", "@salary_formatted"),
            ("Remote %", "@remote_ratio%"),
            ("WLB Rating", "@work_life_balance"),
        ],
    )
    p.add_tools(hover)
    p.legend.location = "top_left"
    p.legend.background_fill_color = "#0F172A"
    p.legend.background_fill_alpha = 0.8
    p.legend.label_text_color = "#F8FAFC"

    st.bokeh_chart(p, use_container_width=True)

    # Aggregated Bokeh Bar Chart
    agg_df = df.groupby("job_title", as_index=False)["salary_usd"].mean().sort_values("salary_usd", ascending=False)
    agg_source = ColumnDataSource(agg_df)

    p_bar = figure(
        x_range=list(agg_df["job_title"]),
        title="Bokeh Canvas: Average Salary by Role",
        width=900,
        height=380,
        tools="pan,reset,save",
        background_fill_color="#1E293B",
        border_fill_color="#0F172A",
    )
    p_bar.vbar(x="job_title", top="salary_usd", width=0.6, source=agg_source, color="#6366F1", alpha=0.9)
    p_bar.xaxis.major_label_orientation = 0.6
    p_bar.title.text_color = "#F8FAFC"
    p_bar.xaxis.major_label_text_color = "#E2E8F0"
    p_bar.yaxis.major_label_text_color = "#E2E8F0"
    p_bar.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    p_bar.grid.grid_line_color = "#334155"

    st.bokeh_chart(p_bar, use_container_width=True)

# TAB 4: FRAMEWORK COMPARISON MATRIX
with tab4:
    st.subheader("Engineering Matrix: Visualization Frameworks Benchmarked")
    st.markdown(
        "Selecting the right tool depends on your team's constraints: publication quality, reactive interactivity, or rapid full-stack delivery."
    )

    comparison_data = {
        "Framework": ["Streamlit", "Bokeh", "Seaborn / Matplotlib", "Plotly / Dash", "Shiny for Python"],
        "Paradigm": [
            "Pure Python Reactive Scripts",
            "HTML5 Canvas & JS Callbacks",
            "Imperative / Declarative Figures",
            "Declarative JSON & React / D3",
            "Reactive Computation Graph",
        ],
        "Interactivity Level": ["High (Widgets + State)", "Ultra-High (Canvas + JS)", "Static / Low", "High (D3.js / WebGL)", "High (Bi-directional)"],
        "Learning Curve": ["Very Gentle (10/10)", "Moderate (6/10)", "Gentle to Moderate (7/10)", "Gentle (8/10)", "Moderate (6/10)"],
        "Performance at Scale": ["Medium (reruns scripts)", "High (Canvas streaming)", "Low (static file generation)", "High (WebGL available)", "High (fine-grained react)"],
        "Best Use Case": [
            "Rapid data apps, prototypes, internal tools",
            "Real-time streaming, big canvas, standalone HTML",
            "Research papers, statistical modeling, books",
            "Enterprise analytics, interactive charts, Dash apps",
            "Complex statistical models, R-to-Python migrations",
        ],
    }

    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

# TAB 5: CI/CD & CLOUD
with tab5:
    st.subheader("Automated CI/CD Pipeline & Cloud Architecture")
    st.markdown(
        "This project adheres to enterprise GitOps best practices. Every commit automatically triggers validation, testing, and deployment."
    )

    st.markdown(
        """
        ```mermaid
        graph LR
            A[Local Commit / Git Push] --> B[GitHub Repository]
            B --> C[GitHub Actions CI/CD]
            C --> D[1. Lint & Format Check]
            C --> E[2. Pytest Test Suite]
            C --> F[3. Docker Container Build]
            F --> G{Branch: main?}
            G -- Yes --> H[Auto Deploy to Streamlit Cloud / Render SaaS]
            G -- No --> I[PR Status Check Passed]
        ```
        """
    )

    col_ci1, col_ci2 = st.columns(2)

    with col_ci1:
        st.markdown("### 🛠️ GitHub Actions Workflow (`ci-cd.yml`)")
        st.code(
            """name: CI/CD Dashboard Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test-and-verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Pytest
        run: pytest -v tests/
      - name: Build Docker Image
        run: docker build -t viz-dashboard .
""",
            language="yaml",
        )

    with col_ci2:
        st.markdown("### 🌐 Production Deployment Steps")
        st.markdown(
            """
            1. **Streamlit Community Cloud**:
               - Connect repo: `https://github.com/Hashiravc/viz-dashboard-ci-cd`
               - Main file path: `app.py`
               - Zero config auto-deploy on every push to `main` branch.
            2. **Docker / Render / Hugging Face Spaces**:
               - Self-contained container running on port 8501.
               - Automated webhook trigger on commit.
            """
        )

# Footer
st.markdown("---")
st.markdown(
    "<center><small>Built with ❤️ using Streamlit, Bokeh, Seaborn, Matplotlib, and Plotly | "
    "GitHub: <a href='https://github.com/Hashiravc/viz-dashboard-ci-cd' target='_blank'>Hashiravc/viz-dashboard-ci-cd</a></small></center>",
    unsafe_allow_html=True,
)
