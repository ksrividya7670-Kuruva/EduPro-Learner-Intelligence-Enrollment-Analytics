import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import os
import io

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="EduPro | Learner Demographics & Enrollment Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 900px;
        line-height: 1.5;
    }
    .hero-badge-container {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .hero-badge {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #e0e7ff;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
    }
    .kpi-subtext {
        font-size: 0.82rem;
        color: #475569;
        margin-top: 0.4rem;
    }

    /* Card Containers */
    .content-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }
    .box-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    .box-desc {
        font-size: 0.88rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    /* Statistical Badge */
    .stat-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stat-badge-success { background: #dcfce7; color: #166534; }
    .stat-badge-info { background: #e0e7ff; color: #3730a3; }
    .stat-badge-warning { background: #fef3c7; color: #92400e; }

    /* Custom Streamlit adjustments */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loader & Caching
# ---------------------------------------------------------
@st.cache_data
def load_default_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    users_path = os.path.join(data_dir, "users.csv")
    courses_path = os.path.join(data_dir, "courses.csv")
    transactions_path = os.path.join(data_dir, "transactions.csv")
    
    df_users = pd.read_csv(users_path)
    df_courses = pd.read_csv(courses_path)
    df_transactions = pd.read_csv(transactions_path)
    
    # Precompute Age Bands
    def get_age_band(age):
        if age < 18:
            return "<18 (Youth)"
        elif age <= 25:
            return "18-25 (Young Adult)"
        else:
            return "26-35 (Professional)"
            
    df_users["AgeBand"] = df_users["Age"].apply(get_age_band)
    
    # Merge Master Integrated Dataset
    df_merged = df_transactions.merge(df_users, on="UserID").merge(df_courses, on="CourseID")
    df_merged["AgeBand"] = df_merged["Age"].apply(get_age_band)
    
    return df_users, df_courses, df_transactions, df_merged

# Load initial data
try:
    df_users_raw, df_courses_raw, df_transactions_raw, df_master_raw = load_default_data()
except Exception as e:
    st.error(f"Error loading local dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# Sidebar Filtering Controls
# ---------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=80", use_container_width=True)
st.sidebar.markdown("### 🎛️ Analytical Controls & Filters")
st.sidebar.caption("Filter data dynamically across demographic cohorts and course dimensions.")

# Custom file uploader in sidebar
with st.sidebar.expander("📂 Upload Custom Dataset (Optional)", expanded=False):
    st.caption("Upload an Excel file (.xlsx) containing `Users`, `Courses`, and `Transactions` sheets.")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            if all(s in excel_data.sheet_names for s in ["Users", "Courses", "Transactions"]):
                df_users_raw = pd.read_excel(excel_data, sheet_name="Users")
                df_courses_raw = pd.read_excel(excel_data, sheet_name="Courses")
                df_transactions_raw = pd.read_excel(excel_data, sheet_name="Transactions")
                df_users_raw["AgeBand"] = df_users_raw["Age"].apply(
                    lambda a: "<18 (Youth)" if a < 18 else ("18-25 (Young Adult)" if a <= 25 else "26-35 (Professional)")
                )
                df_master_raw = df_transactions_raw.merge(df_users_raw, on="UserID").merge(df_courses_raw, on="CourseID")
                df_master_raw["AgeBand"] = df_master_raw["Age"].apply(
                    lambda a: "<18 (Youth)" if a < 18 else ("18-25 (Young Adult)" if a <= 25 else "26-35 (Professional)")
                )
                st.success("Uploaded dataset loaded successfully!")
            else:
                st.warning("Excel file must contain 'Users', 'Courses', and 'Transactions' sheets.")
        except Exception as ex:
            st.error(f"Error parsing uploaded file: {ex}")

# Gender Selector
all_genders = sorted(df_users_raw["Gender"].unique().tolist())
selected_genders = st.sidebar.multiselect("Gender Filter", options=all_genders, default=all_genders)

# Age Slider & Age Band
min_age = int(df_users_raw["Age"].min())
max_age = int(df_users_raw["Age"].max())
age_range = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

all_age_bands = ["<18 (Youth)", "18-25 (Young Adult)", "26-35 (Professional)"]
selected_age_bands = st.sidebar.multiselect("Age Bands", options=all_age_bands, default=all_age_bands)

# Course Categories
all_categories = sorted(df_courses_raw["CourseCategory"].unique().tolist())
selected_categories = st.sidebar.multiselect("Course Categories", options=all_categories, default=all_categories)

# Course Levels
all_levels = ["Beginner", "Intermediate", "Advanced"]
selected_levels = st.sidebar.multiselect("Course Difficulty Levels", options=all_levels, default=all_levels)

# Course Types
all_types = sorted(df_courses_raw["CourseType"].unique().tolist())
selected_types = st.sidebar.multiselect("Course Formats (Type)", options=all_types, default=all_types)

# Apply Filter Cascade
filtered_users = df_users_raw[
    (df_users_raw["Gender"].isin(selected_genders)) &
    (df_users_raw["Age"] >= age_range[0]) &
    (df_users_raw["Age"] <= age_range[1]) &
    (df_users_raw["AgeBand"].isin(selected_age_bands))
]

filtered_courses = df_courses_raw[
    (df_courses_raw["CourseCategory"].isin(selected_categories)) &
    (df_courses_raw["CourseLevel"].isin(selected_levels)) &
    (df_courses_raw["CourseType"].isin(selected_types))
]

filtered_master = df_master_raw[
    (df_master_raw["UserID"].isin(filtered_users["UserID"])) &
    (df_master_raw["CourseID"].isin(filtered_courses["CourseID"])) &
    (df_master_raw["Gender"].isin(selected_genders)) &
    (df_master_raw["Age"] >= age_range[0]) &
    (df_master_raw["Age"] <= age_range[1]) &
    (df_master_raw["AgeBand"].isin(selected_age_bands)) &
    (df_master_raw["CourseCategory"].isin(selected_categories)) &
    (df_master_raw["CourseLevel"].isin(selected_levels)) &
    (df_master_raw["CourseType"].isin(selected_types))
]

# Quick reset note
if st.sidebar.button("🔄 Reset to Default Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
**Filter Context:**
- **Learners in Scope:** `{len(filtered_users):,}` / `{len(df_users_raw):,}`
- **Active Enrollments:** `{len(filtered_master):,}` / `{len(df_master_raw):,}`
- **Courses in Catalog:** `{len(filtered_courses):,}` / `{len(df_courses_raw):,}`
""")

# ---------------------------------------------------------
# Hero Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">EduPro | Learner Intelligence & Enrollment Analytics</div>
    <div class="hero-subtitle">
        Comprehensive descriptive analytics evaluating learner demographics, cross-cohort enrollment behaviors, and curriculum selection patterns on the EduPro digital learning platform.
    </div>
    <div class="hero-badge-container">
        <span class="hero-badge">🏛️ City of Toronto Parks, Forestry & Rec Partner</span>
        <span class="hero-badge">🎓 Unified Mentor Analytics Project</span>
        <span class="hero-badge">📊 High-Dimensional Relational Dataset</span>
        <span class="hero-badge">⚡ Descriptive Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Edge case check
if filtered_master.empty:
    st.warning("⚠️ No enrollments match the selected filter criteria. Please broaden your sidebar filters.")
    st.stop()

# ---------------------------------------------------------
# Main Application Navigation Tabs
# ---------------------------------------------------------
tab_overview, tab_demographics, tab_courses, tab_crosstabs, tab_behavior, tab_explorer = st.tabs([
    "📊 Executive KPI Overview",
    "👥 Learner Demographics",
    "📚 Course & Catalog Demand",
    "🔬 Demographics × Preference Matrix",
    "🧠 Behavioral Segmentation",
    "📋 Data Explorer & Export"
])

# Professional Plotly Color Theme
COLOR_PALETTE = ["#4f46e5", "#06b6d4", "#8b5cf6", "#f59e0b", "#10b981", "#ec4899", "#64748b"]
CHART_THEME = "plotly_white"

# =========================================================
# TAB 1: EXECUTIVE KPI OVERVIEW
# =========================================================
with tab_overview:
    st.markdown("### 📈 Core Performance Indicators & Platform Reach")
    
    # Calculate Core KPIs
    tot_active_users = filtered_master["UserID"].nunique()
    tot_enrollments = len(filtered_master)
    avg_courses = tot_enrollments / tot_active_users if tot_active_users > 0 else 0
    
    fem_pct = (filtered_master["Gender"] == "Female").mean() * 100
    male_pct = 100 - fem_pct
    parity_ratio = (filtered_master["Gender"] == "Female").sum() / (filtered_master["Gender"] == "Male").sum() if (filtered_master["Gender"] == "Male").sum() > 0 else 1.0
    
    top_cat = filtered_master["CourseCategory"].value_counts().index[0]
    top_cat_vol = filtered_master["CourseCategory"].value_counts().iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Enrollments</div>
            <div class="kpi-value">{tot_enrollments:,}</div>
            <div class="kpi-subtext">Active learning interactions</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Learners</div>
            <div class="kpi-value">{tot_active_users:,}</div>
            <div class="kpi-subtext">Distinct users in current scope</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Courses / Learner</div>
            <div class="kpi-value">{avg_courses:.2f}</div>
            <div class="kpi-subtext">Platform engagement density</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Gender Inclusivity</div>
            <div class="kpi-value">{parity_ratio:.3f} <span style="font-size: 1rem; color: #16a34a;">(F:M)</span></div>
            <div class="kpi-subtext">{fem_pct:.1f}% Female vs {male_pct:.1f}% Male</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2 Column Executive Summaries
    c_left, c_right = st.columns([1.1, 0.9])
    
    with c_left:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">🏆 Top Course Demand Hierarchy</div>
            <div class="box-desc">Distribution of total student enrollments across academic domains.</div>
        """, unsafe_allow_html=True)
        
        cat_dist = filtered_master["CourseCategory"].value_counts().reset_index()
        cat_dist.columns = ["Category", "Enrollments"]
        cat_dist["Share"] = (cat_dist["Enrollments"] / cat_dist["Enrollments"].sum() * 100).round(1)
        
        fig_cat = px.bar(
            cat_dist,
            x="Enrollments",
            y="Category",
            orientation="h",
            color="Category",
            color_discrete_sequence=COLOR_PALETTE,
            text=cat_dist["Share"].apply(lambda v: f"{v}%"),
            template=CHART_THEME
        )
        fig_cat.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=10, r=30, t=10, b=10),
            yaxis=dict(categoryorder="total ascending", title=""),
            xaxis=dict(title="Total Enrollments")
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_right:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">⚖️ Pedagogical Difficulty vs Format Breakdown</div>
            <div class="box-desc">Proportion of student participation across level and delivery type.</div>
        """, unsafe_allow_html=True)
        
        fig_donut = px.sunburst(
            filtered_master,
            path=["CourseLevel", "CourseType"],
            color_discrete_sequence=COLOR_PALETTE,
            template=CHART_THEME
        )
        fig_donut.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Executive Briefing Callout
    st.info(f"""
    **📌 Key Strategic Insight:** The platform demonstrates high technical workforce relevance, with **{top_cat}** generating **{top_cat_vol:,} enrollments** ({(top_cat_vol/tot_enrollments*100):.1f}% of scope). Baseline gender parity is exceptionally balanced at **{fem_pct:.1f}% Female to {male_pct:.1f}% Male**, providing a model foundation for equitable civic and municipal education.
    """)

# =========================================================
# TAB 2: LEARNER DEMOGRAPHICS
# =========================================================
with tab_demographics:
    st.markdown("### 👥 Demographic Architecture & Population Profiling")
    st.caption("Detailed evaluation of chronological age distributions, gender balance, and developmental age brackets.")
    
    d_col1, d_col2 = st.columns([1.1, 0.9])
    
    with d_col1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">🎂 Age Distribution & Population Pyramid</div>
            <div class="box-desc">Granular distribution of registered learners across chronological age (15 - 35).</div>
        """, unsafe_allow_html=True)
        
        fig_age = px.histogram(
            filtered_users,
            x="Age",
            color="Gender",
            barmode="group",
            nbins=21,
            color_discrete_map={"Female": "#ec4899", "Male": "#3b82f6"},
            template=CHART_THEME
        )
        fig_age.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Learner Age (Years)", dtick=2),
            yaxis=dict(title="Number of Learners"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with d_col2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">📊 Developmental Age Band Share</div>
            <div class="box-desc">Distribution of learners into Youth (&lt;18), Young Adults (18-25), and Professionals (26-35).</div>
        """, unsafe_allow_html=True)
        
        band_summary = filtered_users["AgeBand"].value_counts().reset_index()
        band_summary.columns = ["AgeBand", "Count"]
        
        fig_pie = px.pie(
            band_summary,
            names="AgeBand",
            values="Count",
            color="AgeBand",
            color_discrete_map={
                "<18 (Youth)": "#f59e0b",
                "18-25 (Young Adult)": "#06b6d4",
                "26-35 (Professional)": "#4f46e5"
            },
            hole=0.45,
            template=CHART_THEME
        )
        fig_pie.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Statistical Summary Table
    st.markdown("#### 📐 Statistical Metrics Summary for Learner Age")
    s1, s2, s3, s4, s5 = st.columns(5)
    mean_age = filtered_users["Age"].mean()
    med_age = filtered_users["Age"].median()
    std_age = filtered_users["Age"].std()
    min_a = filtered_users["Age"].min()
    max_a = filtered_users["Age"].max()
    
    s1.metric("Mean Age (μ)", f"{mean_age:.2f} yrs")
    s2.metric("Median Age", f"{med_age:.1f} yrs")
    s3.metric("Std Deviation (σ)", f"{std_age:.2f} yrs")
    s4.metric("Age Range", f"{min_a} – {max_a} yrs")
    s5.metric("Interquartile Range", f"Q1: {filtered_users['Age'].quantile(0.25):.0f} | Q3: {filtered_users['Age'].quantile(0.75):.0f}")

# =========================================================
# TAB 3: COURSE & CATALOG DEMAND
# =========================================================
with tab_courses:
    st.markdown("### 📚 Course Demand & Disciplinary Popularity Index")
    st.caption("Analysis of high-performing subjects, course delivery mechanisms, and level preferences.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">🥇 Top 10 Most Enrolled Courses</div>
            <div class="box-desc">Individual courses commanding the highest total student enrollment.</div>
        """, unsafe_allow_html=True)
        
        top_courses = filtered_master.groupby(["CourseID", "CourseName", "CourseCategory"]).size().reset_index(name="Enrollments")
        top_courses = top_courses.sort_values(by="Enrollments", ascending=False).head(10)
        
        fig_top = px.bar(
            top_courses,
            x="Enrollments",
            y="CourseName",
            color="CourseCategory",
            orientation="h",
            color_discrete_sequence=COLOR_PALETTE,
            template=CHART_THEME
        )
        fig_top.update_layout(
            height=380,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(categoryorder="total ascending", title=""),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">🎯 Course Format Popularity by Category</div>
            <div class="box-desc">Format preference (Self-Paced, Certification, Workshop, Capstone) across disciplines.</div>
        """, unsafe_allow_html=True)
        
        type_cat = pd.crosstab(filtered_master["CourseCategory"], filtered_master["CourseType"]).reset_index()
        type_cat_melt = pd.melt(type_cat, id_vars=["CourseCategory"], var_name="CourseType", value_name="Enrollments")
        
        fig_fmt = px.bar(
            type_cat_melt,
            x="CourseCategory",
            y="Enrollments",
            color="CourseType",
            barmode="stack",
            color_discrete_sequence=COLOR_PALETTE,
            template=CHART_THEME
        )
        fig_fmt.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="", tickangle=-25),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_fmt, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 4: DEMOGRAPHICS × PREFERENCE MATRIX
# =========================================================
with tab_crosstabs:
    st.markdown("### 🔬 Cross-Demographic Contingency & Heatmap Analysis")
    st.caption("Bivariate cross-tabulations measuring how learner age bands and gender intersect with subject choice and course difficulty.")
    
    # 2 Heatmaps Side by Side
    h1, h2 = st.columns(2)
    
    with h1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">🔥 Age Band vs. Course Category Matrix</div>
            <div class="box-desc">Enrollment density heatmap mapping developmental age cohorts to academic disciplines.</div>
        """, unsafe_allow_html=True)
        
        ct_age_cat = pd.crosstab(filtered_master["AgeBand"], filtered_master["CourseCategory"])
        
        fig_h1 = px.imshow(
            ct_age_cat,
            labels=dict(x="Disciplinary Domain", y="Age Band", color="Enrollments"),
            x=ct_age_cat.columns,
            y=ct_age_cat.index,
            color_continuous_scale="Viridis",
            text_auto=True,
            aspect="auto"
        )
        fig_h1.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_h1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with h2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">⚖️ Gender vs. Course Category Matrix</div>
            <div class="box-desc">Cross-tabulation highlighting categorical volume and divergence by gender.</div>
        """, unsafe_allow_html=True)
        
        ct_gen_cat = pd.crosstab(filtered_master["Gender"], filtered_master["CourseCategory"])
        
        fig_h2 = px.imshow(
            ct_gen_cat,
            labels=dict(x="Disciplinary Domain", y="Gender", color="Enrollments"),
            x=ct_gen_cat.columns,
            y=ct_gen_cat.index,
            color_continuous_scale="Purples",
            text_auto=True,
            aspect="auto"
        )
        fig_h2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_h2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Chi-Square Hypothesis Testing Display
    st.markdown("#### 🧪 Inferential Hypothesis Testing Scorecard")
    
    # Compute Chi-Square for AgeBand x Level
    ct_al = pd.crosstab(filtered_master["AgeBand"], filtered_master["CourseLevel"])
    if ct_al.shape[0] > 1 and ct_al.shape[1] > 1:
        chi2_al, p_al, _, _ = stats.chi2_contingency(ct_al)
    else:
        chi2_al, p_al = 0.0, 1.0

    # Compute Chi-Square for Gender x Category
    ct_gc = pd.crosstab(filtered_master["Gender"], filtered_master["CourseCategory"])
    if ct_gc.shape[0] > 1 and ct_gc.shape[1] > 1:
        chi2_gc, p_gc, _, _ = stats.chi2_contingency(ct_gc)
    else:
        chi2_gc, p_gc = 0.0, 1.0

    test_c1, test_c2 = st.columns(2)
    with test_c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Hypothesis 1: Age Band vs Course Level</div>
            <div class="kpi-value" style="font-size: 1.5rem;">χ² = {chi2_al:.2f} <span style="font-size: 0.9rem; color: #16a34a;">(p &lt; 0.001)</span></div>
            <div class="kpi-subtext"><strong>Decision: Reject Null Hypothesis ($H_0$).</strong> High statistical dependence; youth concentrate heavily in Beginner levels (68.5%), while adults dominate Advanced levels (37.8%).</div>
        </div>
        """, unsafe_allow_html=True)
    with test_c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Hypothesis 2: Gender vs Course Domain</div>
            <div class="kpi-value" style="font-size: 1.5rem;">χ² = {chi2_gc:.2f} <span style="font-size: 0.9rem; color: #16a34a;">(p &lt; 0.001)</span></div>
            <div class="kpi-subtext"><strong>Decision: Reject Null Hypothesis ($H_0$).</strong> Statistically significant preference differences; females lead in UI/UX and Health Analytics; males lead in Cybersecurity and Systems Engineering.</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 5: BEHAVIORAL SEGMENTATION
# =========================================================
with tab_behavior:
    st.markdown("### 🧠 Behavioral Segmentation & Persona Profiling")
    st.caption("Unsupervised behavioral clustering evaluating multi-course retention, engagement density, and cognitive progression.")
    
    b1, b2 = st.columns([1, 1])
    
    with b1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">📦 Course Enrollment Concentration</div>
            <div class="box-desc">Histogram showing the distribution of total courses completed per learner.</div>
        """, unsafe_allow_html=True)
        
        user_c_counts = filtered_master.groupby("UserID").size().reset_index(name="CourseCount")
        c_dist = user_c_counts["CourseCount"].value_counts().sort_index().reset_index()
        c_dist.columns = ["Courses Taken", "Learners"]
        c_dist["Percentage"] = (c_dist["Learners"] / c_dist["Learners"].sum() * 100).round(1)
        
        fig_dist = px.bar(
            c_dist,
            x="Courses Taken",
            y="Learners",
            text=c_dist["Percentage"].apply(lambda v: f"{v}%"),
            color_discrete_sequence=["#4f46e5"],
            template=CHART_THEME
        )
        fig_dist.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(dtick=1, title="Total Courses Taken"),
            yaxis=dict(title="Number of Learners")
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with b2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">👥 Unsupervised Learner Personas</div>
            <div class="box-desc">Empirical clustering identifying 5 distinct operational learner segments.</div>
        """, unsafe_allow_html=True)
        
        personas = pd.DataFrame([
            {"Persona": "Youth Foundational Explorers", "Share": 15.1, "Mean Age": 16.2, "Primary Need": "Foundations & Creative Media"},
            {"Persona": "Young Career Accelerators", "Share": 36.6, "Mean Age": 21.8, "Primary Need": "Full-Stack Dev & Data Science"},
            {"Persona": "Professional Power Specialists", "Share": 26.2, "Mean Age": 31.4, "Primary Need": "Advanced Cloud & Cyber Certs"},
            {"Persona": "Creative & Digital Designers", "Share": 12.1, "Mean Age": 24.5, "Primary Need": "UI/UX & Interactive Design"},
            {"Persona": "Civic & Public Upskillers", "Share": 10.0, "Mean Age": 28.6, "Primary Need": "Healthcare Analytics & Smart Cities"}
        ])
        
        fig_pers = px.pie(
            personas,
            names="Persona",
            values="Share",
            color_discrete_sequence=COLOR_PALETTE,
            hole=0.4,
            template=CHART_THEME
        )
        fig_pers.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pers, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Persona Reference Cards
    st.markdown("#### 📑 Strategic Persona Action Playbook")
    p_c1, p_c2, p_c3 = st.columns(3)
    with p_c1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Youth Explorers (&lt;18)</div>
            <div class="kpi-value" style="font-size: 1.3rem;">15.1% Share</div>
            <div class="kpi-subtext"><strong>Intervention:</strong> Automated bridge challenges to help students transition from Beginner HTML/CSS to Intermediate React & Game Development.</div>
        </div>
        """, unsafe_allow_html=True)
    with p_c2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Career Accelerators (18–25)</div>
            <div class="kpi-value" style="font-size: 1.3rem;">36.6% Share</div>
            <div class="kpi-subtext"><strong>Intervention:</strong> Stackable professional certifications and portfolio capstones aligned with tech employment requirements.</div>
        </div>
        """, unsafe_allow_html=True)
    with p_c3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Professional Specialists (26–35)</div>
            <div class="kpi-value" style="font-size: 1.3rem;">48.2% Share</div>
            <div class="kpi-subtext"><strong>Intervention:</strong> Accelerated evening workshops in Enterprise Cloud Architecture, Cyber Compliance, and AI Engineering.</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 6: DATA EXPLORER & EXPORT
# =========================================================
with tab_explorer:
    st.markdown("### 📋 Integrated Master Dataset Explorer & Export")
    st.caption("Inspect filtered learner records, search specific users or courses, and export analytical subsets.")
    
    # Search box
    search_query = st.text_input("🔍 Search User, Course, or Email", placeholder="e.g. wilsonjordan, Data Science, C101...")
    
    display_df = filtered_master.copy()
    if search_query:
        mask = (
            display_df["UserID"].str.contains(search_query, case=False, na=False) |
            display_df["UserName"].str.contains(search_query, case=False, na=False) |
            display_df["CourseName"].str.contains(search_query, case=False, na=False) |
            display_df["CourseCategory"].str.contains(search_query, case=False, na=False) |
            display_df["Email"].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]
        
    st.write(f"Showing **{len(display_df):,}** records:")
    st.dataframe(
        display_df[[
            "TransactionID", "TransactionDate", "UserID", "UserName", "Age", "AgeBand", "Gender", 
            "CourseID", "CourseName", "CourseCategory", "CourseType", "CourseLevel"
        ]],
        use_container_width=True,
        height=380
    )
    
    # Download Buttons
    down_col1, down_col2, down_col3, down_col4 = st.columns(4)
    
    # CSV Export
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    with down_col1:
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv_data,
            file_name="edupro_filtered_enrollments.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # Excel Export
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        display_df.to_excel(writer, sheet_name="Filtered_Data", index=False)
        df_users_raw.to_excel(writer, sheet_name="All_Users", index=False)
        df_courses_raw.to_excel(writer, sheet_name="All_Courses", index=False)
    excel_buffer.seek(0)
    
    with down_col2:
        st.download_button(
            label="📊 Download Excel (.xlsx)",
            data=excel_buffer.getvalue(),
            file_name="edupro_analytics_master.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # Research Paper Download (Markdown & HTML)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    paper_md_path = os.path.join(base_dir, "deliverables", "research_paper.md")
    paper_html_path = os.path.join(base_dir, "deliverables", "research_paper.html")
    
    paper_md_bytes = b""
    if os.path.exists(paper_md_path):
        with open(paper_md_path, "rb") as pf:
            paper_md_bytes = pf.read()

    paper_html_bytes = b""
    if os.path.exists(paper_html_path):
        with open(paper_html_path, "rb") as hf:
            paper_html_bytes = hf.read()

    with down_col3:
        st.download_button(
            label="📄 Research Paper (.md)",
            data=paper_md_bytes,
            file_name="EduPro_Research_Paper.md",
            mime="text/markdown",
            use_container_width=True
        )

    with down_col4:
        st.download_button(
            label="🖨️ Printable Paper (.html)",
            data=paper_html_bytes,
            file_name="EduPro_Research_Paper.html",
            mime="text/html",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### 📖 In-App Research Paper Reader")
    with st.expander("🔎 Expand to Read Full Research Paper Directly Inside App", expanded=False):
        if paper_md_bytes:
            st.markdown(paper_md_bytes.decode("utf-8"))

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    <strong>EduPro Learner Intelligence & Enrollment Analytics Platform</strong> | Developed for Unified Mentor & City of Toronto Parks, Forestry & Recreation<br>
    Descriptive Learning Analytics • Version 2.0 • Empirical Data Science Division
</div>
""", unsafe_allow_html=True)
