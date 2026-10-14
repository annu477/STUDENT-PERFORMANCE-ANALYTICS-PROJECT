# =============================================================================
# Student Performance Analytics System
# main.py – Streamlit dashboard entry point
# =============================================================================
# Tech: Python | Pandas | NumPy | Streamlit | Matplotlib
# Run : streamlit run main.py
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------------------------------------------------------
# Constants – Grading Rules
# ---------------------------------------------------------------------------
SUBJECTS = ["Math", "Science", "English", "Computer", "Physics"]
MAX_MARKS_PER_SUBJECT = 100
TOTAL_SUBJECTS = len(SUBJECTS)
MAX_TOTAL = MAX_MARKS_PER_SUBJECT * TOTAL_SUBJECTS  # 500

# Grade boundaries (based on percentage of total marks)
GRADE_BOUNDARIES = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),   # below 50 → Fail
]
PASS_PERCENTAGE = 50   # overall average must be >= 50 to pass


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def assign_grade(average: float) -> str:
    """Return letter grade based on average marks (0-100 scale)."""
    for threshold, grade in GRADE_BOUNDARIES:
        if average >= threshold:
            return grade
    return "F"


def assign_status(average: float) -> str:
    """Return Pass or Fail based on PASS_PERCENTAGE threshold."""
    return "Pass" if average >= PASS_PERCENTAGE else "Fail"


def compute_analytics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add computed columns to the dataframe:
      - Total      : sum of all subject marks
      - Average    : mean of subject marks (rounded to 2 dp)
      - Grade      : letter grade
      - Status     : Pass / Fail
    """
    df = df.copy()
    # Total marks using NumPy sum along axis=1
    df["Total"]   = df[SUBJECTS].apply(lambda row: np.sum(row.values), axis=1)
    # Average marks
    df["Average"] = (df["Total"] / TOTAL_SUBJECTS).round(2)
    # Grade and Status via our helper functions
    df["Grade"]   = df["Average"].apply(assign_grade)
    df["Status"]  = df["Average"].apply(assign_status)
    return df


def load_default_data() -> pd.DataFrame:
    """Load the bundled students.csv that ships with the project."""
    csv_path = os.path.join(os.path.dirname(__file__), "students.csv")
    df = pd.read_csv(csv_path)
    return compute_analytics(df)


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Parse an uploaded CSV file and add analytics columns."""
    df = pd.read_csv(uploaded_file)
    # Validate required columns
    required = ["StudentID", "Name", "Department"] + SUBJECTS
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Uploaded CSV is missing columns: {missing}")
        st.stop()
    return compute_analytics(df)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert dataframe to UTF-8 CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")


# ---------------------------------------------------------------------------
# Chart Functions – each returns a Matplotlib figure
# ---------------------------------------------------------------------------

def chart_subject_averages(df: pd.DataFrame):
    """Bar chart of class average per subject."""
    averages = [df[s].mean().round(2) for s in SUBJECTS]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(SUBJECTS, averages, color=["#4C72B0", "#DD8452", "#55A868",
                                              "#C44E52", "#8172B2"])
    ax.set_title("Class Average per Subject", fontsize=14, fontweight="bold")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)
    for bar, val in zip(bars, averages):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1, str(val),
                ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    return fig


def chart_grade_distribution(df: pd.DataFrame):
    """Pie chart of grade distribution."""
    grade_order = ["A+", "A", "B", "C", "D", "F"]
    counts = df["Grade"].value_counts().reindex(grade_order).dropna()
    colors = ["#2ecc71", "#27ae60", "#3498db", "#f39c12", "#e67e22", "#e74c3c"]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
           colors=colors[:len(counts)], startangle=140)
    ax.set_title("Grade Distribution", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def chart_top_students(df: pd.DataFrame, n: int = 10):
    """Horizontal bar chart for top-N students by total marks."""
    top = df.nlargest(n, "Total")[["Name", "Total"]].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(top["Name"][::-1], top["Total"][::-1], color="#4C72B0")
    ax.set_title(f"Top {n} Students by Total Marks", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Marks")
    ax.set_xlim(0, MAX_TOTAL)
    fig.tight_layout()
    return fig


def chart_pass_fail(df: pd.DataFrame):
    """Bar chart showing pass vs fail count."""
    counts = df["Status"].value_counts()
    colors = {"Pass": "#2ecc71", "Fail": "#e74c3c"}
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.bar(counts.index, counts.values,
           color=[colors.get(s, "#999") for s in counts.index])
    ax.set_title("Pass / Fail Distribution", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Students")
    for i, (label, val) in enumerate(counts.items()):
        ax.text(i, val + 0.3, str(val), ha="center", fontsize=11)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Page: Overview / Summary Statistics
# ---------------------------------------------------------------------------

def page_overview(df: pd.DataFrame):
    st.header("📊 Class Overview")

    total_students = len(df)
    passing        = int((df["Status"] == "Pass").sum())
    failing        = total_students - passing
    pass_pct       = round(passing / total_students * 100, 1)
    class_avg      = round(df["Average"].mean(), 2)
    highest        = df.loc[df["Total"].idxmax()]
    lowest         = df.loc[df["Total"].idxmin()]

    # KPI cards in four columns
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students",  total_students)
    c2.metric("Pass %",          f"{pass_pct}%")
    c3.metric("Class Average",   f"{class_avg} / 100")
    c4.metric("Highest Total",   f"{int(highest['Total'])} / {MAX_TOTAL}")

    st.divider()

    # Highest & Lowest scorers
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🏆 Top Scorer")
        st.write(f"**{highest['Name']}** ({highest['Department']})")
        st.write(f"Total: **{int(highest['Total'])}** | Grade: **{highest['Grade']}**")
    with col_b:
        st.subheader("⚠️ Lowest Scorer")
        st.write(f"**{lowest['Name']}** ({lowest['Department']})")
        st.write(f"Total: **{int(lowest['Total'])}** | Grade: **{lowest['Grade']}**")

    st.divider()

    # Subject-wise averages table
    st.subheader("📚 Subject-wise Class Averages")
    subj_avg = pd.DataFrame({
        "Subject": SUBJECTS,
        "Class Average": [round(df[s].mean(), 2) for s in SUBJECTS],
        "Highest":       [int(df[s].max()) for s in SUBJECTS],
        "Lowest":        [int(df[s].min()) for s in SUBJECTS],
    })
    st.dataframe(subj_avg, use_container_width=True, hide_index=True)

    st.divider()

    # Charts row
    st.subheader("📈 Visual Summaries")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(chart_subject_averages(df))
    with col2:
        st.pyplot(chart_grade_distribution(df))

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(chart_top_students(df))
    with col4:
        st.pyplot(chart_pass_fail(df))


# ---------------------------------------------------------------------------
# Page: Student Records (Search + Filter + Download)
# ---------------------------------------------------------------------------

def page_records(df: pd.DataFrame):
    st.header("📋 Student Records")

    # --- Filters ---
    with st.expander("🔍 Search & Filter", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 2])
        search_name  = col1.text_input("Search by Name")
        dept_options = ["All"] + sorted(df["Department"].unique().tolist())
        dept_filter  = col2.selectbox("Department", dept_options)
        grade_opts   = ["All"] + ["A+", "A", "B", "C", "D", "F"]
        grade_filter = col3.selectbox("Grade", grade_opts)

        col4, col5 = st.columns([2, 2])
        status_filter = col4.selectbox("Status", ["All", "Pass", "Fail"])
        min_avg, max_avg = col5.slider(
            "Average Marks Range", 0, 100, (0, 100), step=1
        )

    # Apply filters
    filtered = df.copy()
    if search_name:
        filtered = filtered[
            filtered["Name"].str.contains(search_name, case=False, na=False)
        ]
    if dept_filter != "All":
        filtered = filtered[filtered["Department"] == dept_filter]
    if grade_filter != "All":
        filtered = filtered[filtered["Grade"] == grade_filter]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]
    filtered = filtered[
        (filtered["Average"] >= min_avg) & (filtered["Average"] <= max_avg)
    ]

    st.write(f"Showing **{len(filtered)}** of **{len(df)}** students")

    # Display table – colour Status column
    st.dataframe(
        filtered[["StudentID", "Name", "Department"] + SUBJECTS +
                 ["Total", "Average", "Grade", "Status", "Attendance"]],
        use_container_width=True,
        hide_index=True,
    )

    # Download filtered results
    st.download_button(
        label="⬇️ Download Filtered Results (CSV)",
        data=to_csv_bytes(filtered),
        file_name="filtered_results.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Page: Top Performers
# ---------------------------------------------------------------------------

def page_top_performers(df: pd.DataFrame):
    st.header("🏅 Top Performers")

    n = st.slider("Show top N students", min_value=3, max_value=min(25, len(df)),
                  value=10, step=1)
    top = df.nlargest(n, "Total").reset_index(drop=True)
    top.index += 1  # rank from 1

    st.dataframe(
        top[["Name", "Department", "Total", "Average", "Grade",
             "Status", "Attendance"]],
        use_container_width=True,
    )

    st.pyplot(chart_top_students(df, n))


# ---------------------------------------------------------------------------
# Page: Upload CSV
# ---------------------------------------------------------------------------

def page_upload():
    st.header("📤 Upload Your CSV")
    st.info(
        "Upload a CSV with columns: **StudentID, Name, Department, "
        "Math, Science, English, Computer, Physics, Attendance**"
    )

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded:
        df_uploaded = load_uploaded_data(uploaded)
        st.success(f"Loaded {len(df_uploaded)} student records.")
        st.dataframe(df_uploaded, use_container_width=True, hide_index=True)

        st.download_button(
            label="⬇️ Download Analyzed Results (CSV)",
            data=to_csv_bytes(df_uploaded),
            file_name="analyzed_results.csv",
            mime="text/csv",
        )

        # Show overview charts for uploaded data
        if st.checkbox("Show Overview Charts for Uploaded Data"):
            page_overview(df_uploaded)


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title="Student Performance Analytics",
        page_icon="🎓",
        layout="wide",
    )

    # Sidebar navigation
    st.sidebar.title("🎓 Student Analytics")
    st.sidebar.markdown("---")
    pages = {
        "📊 Class Overview":    "overview",
        "📋 Student Records":   "records",
        "🏅 Top Performers":    "top",
        "📤 Upload CSV":        "upload",
    }
    choice = st.sidebar.radio("Navigate to", list(pages.keys()))

    # Grading rules reference in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Grading Rules**")
    st.sidebar.markdown(
        "| Grade | Average |\n"
        "|-------|----------|\n"
        "| A+    | ≥ 90     |\n"
        "| A     | ≥ 80     |\n"
        "| B     | ≥ 70     |\n"
        "| C     | ≥ 60     |\n"
        "| D     | ≥ 50     |\n"
        "| F     | < 50     |"
    )
    st.sidebar.markdown("**Pass criteria:** Average ≥ 50")

    # Load default data
    df = load_default_data()

    # Route to selected page
    page_key = pages[choice]
    if page_key == "overview":
        page_overview(df)
    elif page_key == "records":
        page_records(df)
    elif page_key == "top":
        page_top_performers(df)
    elif page_key == "upload":
        page_upload()


if __name__ == "__main__":
    main()
