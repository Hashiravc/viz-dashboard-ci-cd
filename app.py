"""Interactive Multi-Engine Data Visualization & Analytics Hub.

Demonstrating Bokeh, Seaborn, Matplotlib, and Plotly orchestrated with Streamlit,
backed by automated GitHub Actions CI/CD and Cloud Deployment.
Authored by Hashira Belén Vargas Candia.
"""

import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as components
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.transform import factor_cmap

from data_loader import filter_data, generate_sample_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Multi-Tool Viz Hub | CI/CD Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM MODERN CSS STYLING
# ==========================================
st.markdown(
    """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }

    /* Header Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(8px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .hero-subtitle {
        font-size: 1.02rem;
        color: #94A3B8;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    /* Badges */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    
    .badge-primary {
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.35);
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    
    .badge-neutral {
        background: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px 20px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #6366F1;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
    }

    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }

    .kpi-subtext {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 6px;
    }

    /* Sidebar Enhancement */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid #1E293B;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        color: #94A3B8;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #6366F1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# DATA LOADING & CACHING
# ==========================================
@st.cache_data
def load_data() -> pd.DataFrame:
    """Generate and cache the baseline dataset."""
    return generate_sample_data(n_samples=1600, seed=42)


raw_df = load_data()

# ==========================================
# SIDEBAR CONTROLS & FILTERING
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    st.caption("Filter real-time data across all visualization engines.")

    # Filter Presets
    st.markdown("**⚡ Quick Presets**")
    preset_col1, preset_col2 = st.columns(2)
    
    # Store filter preset state in session_state if needed
    all_jobs = sorted(raw_df["job_title"].unique())
    ai_jobs = ["Data Scientist", "Machine Learning Engineer", "Data Engineer"]
    dev_jobs = ["Fullstack Developer", "Frontend Developer", "Backend Developer", "DevOps Engineer", "Cloud Architect"]

    if "selected_jobs" not in st.session_state:
        st.session_state.selected_jobs = all_jobs[:5]

    with preset_col1:
        if st.button("🤖 Data & AI", use_container_width=True):
            st.session_state.selected_jobs = ai_jobs
    with preset_col2:
        if st.button("💻 Software/Cloud", use_container_width=True):
            st.session_state.selected_jobs = dev_jobs

    selected_years = st.multiselect(
        "Work Years",
        options=sorted(raw_df["work_year"].unique()),
        default=sorted(raw_df["work_year"].unique()),
    )

    selected_exp = st.multiselect(
        "Experience Levels",
        options=["Entry-level", "Mid-level", "Senior", "Executive"],
        default=["Mid-level", "Senior"],
    )

    selected_jobs = st.multiselect(
        "Job Titles",
        options=all_jobs,
        default=st.session_state.selected_jobs,
    )

    remote_filter = st.multiselect(
        "Workplace Modality",
        options=[0, 50, 100],
        default=[0, 50, 100],
        format_func=lambda x: "🏢 On-site (0%)" if x == 0 else ("⚖️ Hybrid (50%)" if x == 50 else "🌐 Fully Remote (100%)"),
    )

    st.markdown("---")
    st.markdown("### 🚀 Project Information")
    st.markdown(
        """
        - **Author**: Hashira Belén Vargas Candia
        - **Repository**: [Hashiravc/viz-dashboard-ci-cd](https://github.com/Hashiravc/viz-dashboard-ci-cd)
        - **CI/CD**: GitHub Actions
        - **Hosting**: Streamlit Community Cloud
        """
    )
    st.markdown(
        '<a href="https://github.com/Hashiravc/viz-dashboard-ci-cd" target="_blank" style="text-decoration:none;">'
        '<div style="text-align:center; padding:8px; background:#1E293B; border:1px solid #334155; border-radius:8px; color:#F8FAFC; font-weight:600; font-size:0.85rem;">'
        '⭐ Star on GitHub'
        '</div></a>',
        unsafe_allow_html=True,
    )

# Filter Data
df = filter_data(
    raw_df,
    years=selected_years,
    experience_levels=selected_exp,
    job_titles=selected_jobs,
    remote_options=remote_filter,
)

# ==========================================
# HERO HEADER SECTION
# ==========================================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Multi-Engine Data Visualization Hub</div>
        <div class="hero-subtitle">
            An enterprise-grade comparative analytics platform orchestrating <strong>Plotly</strong>, <strong>Seaborn</strong>, 
            <strong>Matplotlib</strong>, and <strong>Bokeh</strong> inside <strong>Streamlit</strong>, backed by automated GitHub Actions CI/CD.
        </div>
        <div class="badge-container">
            <span class="badge badge-success">🟢 Production Live on Cloud</span>
            <span class="badge badge-primary">⚡ Automated CI/CD (GitHub Actions)</span>
            <span class="badge badge-neutral">👤 Author: Hashira Belén Vargas Candia</span>
            <span class="badge badge-neutral">🐍 Python 3.11+</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your criteria in the sidebar.")
    st.stop()

# ==========================================
# TOP KPI METRIC CARDS
# ==========================================
avg_salary = df["salary_usd"].mean()
base_avg = raw_df["salary_usd"].mean()
salary_diff_pct = ((avg_salary - base_avg) / base_avg) * 100
remote_pct = (df["remote_ratio"] == 100).mean() * 100
top_paying_role = df.groupby("job_title")["salary_usd"].mean().idxmax()
top_role_salary = df.groupby("job_title")["salary_usd"].mean().max()

kpi_html = f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">📊 Filtered Records</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-subtext">{len(df)/len(raw_df)*100:.1f}% of total catalog ({len(raw_df):,})</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">💰 Average Compensation</div>
        <div class="kpi-value">${avg_salary:,.0f}</div>
        <div class="kpi-subtext">{'▲' if salary_diff_pct >= 0 else '▼'} {abs(salary_diff_pct):.1f}% vs. general market baseline</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🌐 Fully Remote Adoption</div>
        <div class="kpi-value">{remote_pct:.1f}%</div>
        <div class="kpi-subtext">{(df['remote_ratio'] == 100).sum():,} engineers working 100% remote</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🏆 Top Earning Specialization</div>
        <div class="kpi-value" style="font-size: 1.25rem; font-weight:700; color:#A5B4FC; margin-top:4px;">{top_paying_role}</div>
        <div class="kpi-subtext">Avg: ${top_role_salary:,.0f} / year</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ==========================================
# BOKEH RENDER HELPER (STANDALONE HTML COMPONENT)
# ==========================================
def render_bokeh(fig, height=520):
    """Safely render any Bokeh figure in Streamlit without depending on deprecated st.bokeh_chart."""
    html_content = file_html(fig, CDN, "Bokeh Visual")
    components.html(html_content, height=height, scrolling=False)


# ==========================================
# MAIN VISUALIZATION TABS
# ==========================================
tab_plotly, tab_seaborn, tab_bokeh, tab_data, tab_compare, tab_cicd = st.tabs([
    "📈 Plotly (Interactive)",
    "🎨 Seaborn & Matplotlib (Statistical)",
    "⚡ Bokeh (HTML5 Canvas)",
    "📋 Data Explorer & Export",
    "⚖️ Framework Benchmark",
    "🚀 CI/CD & Architecture",
])

# ------------------------------------------
# TAB 1: PLOTLY (INTERACTIVE)
# ------------------------------------------
with tab_plotly:
    st.subheader("Interactive Exploratory Data Analysis with Plotly")
    st.caption("Plotly delivers hardware-accelerated D3.js interactive charts with instant tooltips, zooming, and dynamic re-scaling.")

    pcol1, pcol2 = st.columns(2)

    with pcol1:
        fig_box = px.box(
            df,
            x="job_title",
            y="salary_usd",
            color="experience_level",
            title="<b>Compensation Range by Role & Seniority</b>",
            labels={"salary_usd": "Annual Salary (USD)", "job_title": "Role", "experience_level": "Seniority"},
            template="plotly_dark",
            category_orders={"experience_level": ["Entry-level", "Mid-level", "Senior", "Executive"]},
            color_discrete_sequence=["#38BDF8", "#818CF8", "#F472B6", "#FBBF24"],
        )
        fig_box.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#1E293B",
            font=dict(family="Inter, sans-serif", color="#F8FAFC"),
            xaxis=dict(tickangle=-40, gridcolor="#334155"),
            yaxis=dict(gridcolor="#334155"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=50, l=40, r=20),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with pcol2:
        country_agg = (
            df.groupby("company_country")
            .agg(
                avg_salary=("salary_usd", "mean"),
                headcount=("id", "count"),
                top_role=("job_title", lambda x: x.mode()[0] if not x.empty else "N/A"),
            )
            .reset_index()
            .sort_values("avg_salary", ascending=True)
        )

        fig_country = px.bar(
            country_agg,
            x="avg_salary",
            y="company_country",
            orientation="h",
            color="avg_salary",
            color_continuous_scale="Viridis",
            title="<b>Global Market: Mean Compensation by Country</b>",
            labels={"avg_salary": "Average Salary (USD)", "company_country": "Country"},
            text="avg_salary",
            hover_data={"headcount": True, "top_role": True},
        )
        fig_country.update_traces(
            texttemplate="$%{x:,.0f}",
            textposition="outside",
            textfont=dict(size=11, color="#E2E8F0"),
            marker=dict(line=dict(width=1, color="#1E293B")),
        )
        fig_country.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#1E293B",
            font=dict(family="Inter, sans-serif", color="#F8FAFC"),
            xaxis=dict(tickprefix="$", gridcolor="#334155"),
            yaxis=dict(gridcolor="#334155"),
            margin=dict(t=60, b=50, l=40, r=60),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_country, use_container_width=True)

    # -------------------------------------------------------------
    # INTUITIVE WORK-LIFE BALANCE & COMPENSATION ANALYSIS
    # -------------------------------------------------------------
    st.markdown("#### ⚖️ Work-Life Balance vs. Compensation Analysis")
    
    view_mode = st.radio(
        "Display Mode:",
        options=["🎯 Executive Quadrant Matrix (Aggregated by Role & Seniority)", "🔬 Micro Scatter Distribution (Individual Data Points + Trendline)"],
        horizontal=True,
    )

    median_salary = df["salary_usd"].median()
    median_wlb = df["work_life_balance"].median()

    if "Executive" in view_mode:
        # Aggregate by Job Title & Experience for clean, zero-clutter insights
        agg_wlb = (
            df.groupby(["job_title", "experience_level"])
            .agg(
                avg_salary=("salary_usd", "mean"),
                avg_wlb=("work_life_balance", "mean"),
                tech_sat=("tech_satisfaction", "mean"),
                headcount=("id", "count"),
            )
            .reset_index()
        )

        fig_quadrant = px.scatter(
            agg_wlb,
            x="avg_wlb",
            y="avg_salary",
            size="headcount",
            color="job_title",
            symbol="experience_level",
            text="job_title",
            title="<b>Executive Quadrant Matrix: Compensation vs. Work-Life Balance</b>",
            labels={
                "avg_wlb": "Average Work-Life Balance (1 to 5)",
                "avg_salary": "Average Compensation (USD)",
                "job_title": "Specialization",
                "experience_level": "Seniority",
                "headcount": "Engineers Count",
            },
            template="plotly_dark",
            size_max=32,
        )

        fig_quadrant.update_traces(
            textposition="top center",
            textfont=dict(size=10, color="#E2E8F0"),
            marker=dict(line=dict(width=1.5, color="#FFFFFF")),
        )

        # Add Quadrant Reference Lines
        fig_quadrant.add_hline(
            y=median_salary,
            line_dash="dash",
            line_color="#64748B",
            annotation_text=f"Market Median Salary: ${median_salary:,.0f}",
            annotation_position="bottom right",
            annotation_font=dict(size=10, color="#94A3B8"),
        )
        fig_quadrant.add_vline(
            x=median_wlb,
            line_dash="dash",
            line_color="#64748B",
            annotation_text=f"Median WLB: {median_wlb:.1f}",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#94A3B8"),
        )

        # Quadrant Explanatory Annotations
        max_y = agg_wlb["avg_salary"].max() * 1.05
        min_y = agg_wlb["avg_salary"].min() * 0.95
        max_x = agg_wlb["avg_wlb"].max() + 0.1
        min_x = agg_wlb["avg_wlb"].min() - 0.1

        fig_quadrant.add_annotation(
            x=max_x, y=max_y, text="🚀 High Pay & High Balance", showarrow=False,
            font=dict(color="#10B981", size=11, family="Inter")
        )
        fig_quadrant.add_annotation(
            x=min_x, y=max_y, text="⚠️ High Pay & High Demands", showarrow=False,
            font=dict(color="#F59E0B", size=11, family="Inter")
        )

        fig_quadrant.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#1E293B",
            font=dict(family="Inter, sans-serif", color="#F8FAFC"),
            yaxis=dict(tickprefix="$", gridcolor="#334155"),
            xaxis=dict(gridcolor="#334155"),
            margin=dict(t=60, b=40, l=40, r=30),
            height=540,
        )
        st.plotly_chart(fig_quadrant, use_container_width=True)

    else:
        # Micro scatter with subtle point size, high opacity, and trendline
        fig_scatter = px.scatter(
            df,
            x="work_life_balance",
            y="salary_usd",
            color="experience_level",
            hover_name="job_title",
            hover_data={"company_country": True, "remote_ratio": True, "tech_satisfaction": True},
            title="<b>Individual Distribution: Work-Life Balance vs. Compensation with Market Trendline</b>",
            labels={"work_life_balance": "Work-Life Balance (1-5)", "salary_usd": "Compensation (USD)", "experience_level": "Seniority"},
            template="plotly_dark",
            opacity=0.6,
            color_discrete_sequence=["#38BDF8", "#818CF8", "#F472B6", "#FBBF24"],
        )
        fig_scatter.update_traces(marker=dict(size=7, line=dict(width=0.5, color="#1E293B")))

        # Add clean linear trendline via numpy
        if len(df) > 1:
            x_vals = df["work_life_balance"].to_numpy()
            y_vals = df["salary_usd"].to_numpy()
            m, b = np.polyfit(x_vals, y_vals, 1)
            x_trend = np.linspace(x_vals.min(), x_vals.max(), 50)
            y_trend = m * x_trend + b
            fig_scatter.add_trace(
                go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode="lines",
                    name="Linear Trendline",
                    line=dict(color="#F43F5E", width=2.5, dash="dash"),
                )
            )

        fig_scatter.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#1E293B",
            font=dict(family="Inter, sans-serif", color="#F8FAFC"),
            yaxis=dict(tickprefix="$", gridcolor="#334155"),
            xaxis=dict(gridcolor="#334155"),
            margin=dict(t=60, b=40, l=40, r=20),
            height=500,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)


# ------------------------------------------
# TAB 2: SEABORN & MATPLOTLIB (STATISTICAL)
# ------------------------------------------
with tab_seaborn:
    st.subheader("Statistical Modeling & Rigor with Seaborn & Matplotlib")
    st.caption("Seaborn produces mathematically rigorous distribution models, covariance matrices, and publication-ready static figures.")

    scol1, scol2 = st.columns(2)

    with scol1:
        fig_sns1, ax1 = plt.subplots(figsize=(8, 5), dpi=120)
        sns.histplot(
            data=df,
            x="salary_usd",
            hue="experience_level",
            kde=True,
            palette="mako",
            alpha=0.45,
            ax=ax1,
        )
        ax1.set_title("Kernel Density Estimation (KDE) of Tech Compensation", fontsize=12, fontweight="bold", pad=12, color="#F8FAFC")
        ax1.set_xlabel("Salary (USD)", fontsize=10, color="#94A3B8")
        ax1.set_ylabel("Density / Count", fontsize=10, color="#94A3B8")
        ax1.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
        ax1.tick_params(colors="#CBD5E1")
        fig_sns1.patch.set_facecolor("#0F172A")
        ax1.set_facecolor("#1E293B")
        st.pyplot(fig_sns1)
        plt.close(fig_sns1)

    with scol2:
        fig_sns2, ax2 = plt.subplots(figsize=(8, 5), dpi=120)
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
            annot_kws={"size": 9, "color": "#FFFFFF"},
        )
        ax2.set_title("Covariance & Correlation Matrix", fontsize=12, fontweight="bold", pad=12, color="#F8FAFC")
        ax2.tick_params(colors="#CBD5E1")
        fig_sns2.patch.set_facecolor("#0F172A")
        ax2.set_facecolor("#1E293B")
        st.pyplot(fig_sns2)
        plt.close(fig_sns2)

    # Violin Plot
    fig_sns3, ax3 = plt.subplots(figsize=(11, 4.5), dpi=120)
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
    ax3.set_title("Salary Dispersion Across Remote Modalities & Company Scales", fontsize=12, fontweight="bold", pad=12, color="#F8FAFC")
    ax3.set_xlabel("Remote Percentage (%)", fontsize=10, color="#94A3B8")
    ax3.set_ylabel("Compensation (USD)", fontsize=10, color="#94A3B8")
    ax3.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)
    ax3.tick_params(colors="#CBD5E1")
    fig_sns3.patch.set_facecolor("#0F172A")
    ax3.set_facecolor("#1E293B")
    st.pyplot(fig_sns3)
    plt.close(fig_sns3)


# ------------------------------------------
# TAB 3: BOKEH (HTML5 CANVAS ENGINE)
# ------------------------------------------
with tab_bokeh:
    st.subheader("High-Performance HTML5 Canvas Plotting with Bokeh")
    st.markdown(
        """
        <div style="background:#1E293B; border-left:4px solid #6366F1; padding:12px 16px; border-radius:6px; margin-bottom:16px;">
            <strong style="color:#C7D2FE;">⚡ Rendered via BokehJS Standalone Canvas</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8;">
                Bokeh plots render hardware-accelerated vectors directly onto an HTML5 Canvas, enabling zero-latency panning, 
                zooming, and hover tooltips without requiring server re-execution.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Bokeh Scatter Figure
    b_df = df.sample(min(len(df), 600), random_state=42).copy()
    b_df["salary_formatted"] = b_df["salary_usd"].apply(lambda x: f"${x:,.0f}")
    source = ColumnDataSource(b_df)

    exp_levels = ["Entry-level", "Mid-level", "Senior", "Executive"]
    colors = ["#38BDF8", "#818CF8", "#F472B6", "#FBBF24"]
    color_map = factor_cmap("experience_level", palette=colors, factors=exp_levels)

    p_scatter = figure(
        title="Bokeh Interactive Canvas: Work-Life Balance vs. Annual Compensation",
        x_axis_label="Work-Life Balance Score (1.0 to 5.0)",
        y_axis_label="Salary (USD)",
        height=460,
        sizing_mode="stretch_width",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        background_fill_color="#1E293B",
        border_fill_color="#0F172A",
    )
    p_scatter.title.text_color = "#F8FAFC"
    p_scatter.title.text_font_size = "12pt"
    p_scatter.xaxis.axis_label_text_color = "#94A3B8"
    p_scatter.yaxis.axis_label_text_color = "#94A3B8"
    p_scatter.xaxis.major_label_text_color = "#CBD5E1"
    p_scatter.yaxis.major_label_text_color = "#CBD5E1"
    p_scatter.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    p_scatter.grid.grid_line_color = "#334155"
    p_scatter.grid.grid_line_dash = [4, 4]

    circle_r = p_scatter.scatter(
        x="work_life_balance",
        y="salary_usd",
        size=9,
        source=source,
        color=color_map,
        alpha=0.85,
        legend_field="experience_level",
    )

    hover_tool = HoverTool(
        renderers=[circle_r],
        tooltips=[
            ("Role", "@job_title"),
            ("Seniority", "@experience_level"),
            ("Country", "@company_country"),
            ("Compensation", "@salary_formatted"),
            ("Remote", "@remote_ratio%"),
            ("WLB Rating", "@work_life_balance"),
        ],
    )
    p_scatter.add_tools(hover_tool)
    p_scatter.legend.location = "top_left"
    p_scatter.legend.background_fill_color = "#0F172A"
    p_scatter.legend.background_fill_alpha = 0.8
    p_scatter.legend.label_text_color = "#F8FAFC"

    render_bokeh(p_scatter, height=480)

    # Bokeh Bar Chart
    agg_df = df.groupby("job_title", as_index=False)["salary_usd"].mean().sort_values("salary_usd", ascending=False)
    agg_source = ColumnDataSource(agg_df)

    p_bar = figure(
        x_range=list(agg_df["job_title"]),
        title="Bokeh Canvas: Mean Salary by Specialization",
        height=380,
        sizing_mode="stretch_width",
        tools="pan,reset,save",
        background_fill_color="#1E293B",
        border_fill_color="#0F172A",
    )
    p_bar.vbar(x="job_title", top="salary_usd", width=0.55, source=agg_source, color="#6366F1", alpha=0.9)
    p_bar.xaxis.major_label_orientation = 0.6
    p_bar.title.text_color = "#F8FAFC"
    p_bar.title.text_font_size = "12pt"
    p_bar.xaxis.major_label_text_color = "#CBD5E1"
    p_bar.yaxis.major_label_text_color = "#CBD5E1"
    p_bar.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    p_bar.grid.grid_line_color = "#334155"

    render_bokeh(p_bar, height=400)


# ------------------------------------------
# TAB 4: DATA EXPLORER & EXPORT
# ------------------------------------------
with tab_data:
    st.subheader("Interactive Dataset Explorer & Data Export")
    st.caption("Inspect filtered records, sort attributes, or download the dataset directly as CSV.")

    search_query = st.text_input("🔍 Search by Job Title or Country", placeholder="e.g. Data Scientist, Germany...")

    display_df = df.copy()
    if search_query:
        display_df = display_df[
            display_df["job_title"].str.contains(search_query, case=False, na=False)
            | display_df["company_country"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "salary_usd": st.column_config.NumberColumn("Salary (USD)", format="$%d"),
            "work_life_balance": st.column_config.ProgressColumn("Work-Life Balance", min_value=1.0, max_value=5.0),
            "tech_satisfaction": st.column_config.ProgressColumn("Tech Satisfaction", min_value=1.0, max_value=5.0),
            "remote_ratio": st.column_config.NumberColumn("Remote %", format="%d%%"),
        },
    )

    # Download button
    csv_buffer = io.StringIO()
    display_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_buffer.getvalue(),
        file_name="filtered_tech_compensation.csv",
        mime="text/csv",
    )


# ------------------------------------------
# TAB 5: FRAMEWORK BENCHMARK MATRIX
# ------------------------------------------
with tab_compare:
    st.subheader("Architectural Comparison: Python Visualization Ecosystem")
    st.markdown(
        "A breakdown of when each visualization tool is best suited in enterprise production architectures:"
    )

    benchmark_data = {
        "Library": ["Streamlit", "Plotly / Dash", "Bokeh", "Seaborn / Matplotlib", "Shiny for Python"],
        "Rendering Backend": ["React + Python Server", "React.js + D3.js + WebGL", "HTML5 Canvas (BokehJS)", "Static Agg / SVG", "Reactive Computation Graph"],
        "Interactivity Paradigm": ["Full Script Rerun on State Change", "Declarative JSON & Bidirectional", "Hardware Canvas & JS Callbacks", "Static Figure Render", "Fine-Grained Reactive Graph"],
        "Interactivity Level": ["High (Widgets + Reactive)", "High (D3.js / 3D)", "Ultra-High (Canvas + Zoom)", "Static / Low", "High (Full-Stack)"],
        "Learning Curve": ["Very Gentle (10/10)", "Gentle (8/10)", "Moderate (6/10)", "Gentle (7/10)", "Moderate (6/10)"],
        "Best Production Scenario": [
            "Rapid data apps, prototyping, executive KPI portals",
            "Complex interactive charts, financial dashboards, Dash web apps",
            "High-frequency data streaming, big canvas, standalone HTML",
            "Scientific publications, academic papers, statistical exploratory",
            "Complex enterprise statistical apps, R-to-Python migrations",
        ],
    }
    st.dataframe(pd.DataFrame(benchmark_data), use_container_width=True, hide_index=True)


# ------------------------------------------
# TAB 6: CI/CD & ARCHITECTURE
# ------------------------------------------
with tab_cicd:
    st.subheader("GitOps CI/CD Automation & Cloud Hosting Architecture")
    st.markdown(
        """
        This dashboard uses a modern GitOps continuous delivery lifecycle. Every push to the `main` branch
        triggers automated quality gates on GitHub Actions before updating the public cloud deployment.
        """
    )

    col_ci1, col_ci2 = st.columns(2)

    with col_ci1:
        st.markdown("#### 🔄 Pipeline Stages")
        st.markdown(
            """
            1. **Continuous Integration (CI)**:
               - Python 3.11 environment initialization with pip dependency caching.
               - Automated unit testing via `pytest tests/test_dashboard.py`.
               - Python bytecode compilation check (`py_compile`).
            2. **Container Packaging**:
               - Build Docker container layer and verify dependency resolution.
            3. **Continuous Deployment (CD)**:
               - Direct GitOps webhook synchronization with **Streamlit Community Cloud**.
               - Zero-downtime rolling update.
            """
        )

    with col_ci2:
        st.markdown("#### 🌐 Production Links")
        st.markdown(
            """
            - **Public Repository**: [https://github.com/Hashiravc/viz-dashboard-ci-cd](https://github.com/Hashiravc/viz-dashboard-ci-cd)
            - **Live Public SaaS**: [https://viz-dashboard-ci-cd.streamlit.app/](https://viz-dashboard-ci-cd.streamlit.app/)
            - **CI/CD Pipeline Status**: [![CI/CD](https://github.com/Hashiravc/viz-dashboard-ci-cd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Hashiravc/viz-dashboard-ci-cd/actions/workflows/ci-cd.yml)
            """
        )

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#64748B; font-size:0.85rem; padding-bottom:12px;">
        Designed & Built by <strong>Hashira Belén Vargas Candia</strong> | 
        <a href="https://github.com/Hashiravc/viz-dashboard-ci-cd" target="_blank" style="color:#818CF8; text-decoration:none;">
            GitHub: Hashiravc/viz-dashboard-ci-cd
        </a> | 
        Deployed on Streamlit Community Cloud
    </div>
    """,
    unsafe_allow_html=True,
)
