# Project Documentation
## Student Performance Analytics System

---

## 1. Project Objectives

1. Build a fully functional student performance analytics dashboard using Python.
2. Demonstrate core Python concepts: functions, loops, conditions, Pandas DataFrames, and NumPy calculations.
3. Provide a clean, interactive UI using Streamlit without requiring machine learning or APIs.
4. Enable educators/students to load, analyse, filter, and download academic data effortlessly.

---

## 2. Tech Stack

| Technology | Role |
|------------|------|
| Python 3.10+ | Core programming language |
| Pandas | Data loading, filtering, and manipulation |
| NumPy | Numerical calculations (totals, averages) |
| Streamlit | Web dashboard / UI |
| Matplotlib | Charts and visualisations |

---

## 3. Dataset Description (`students.csv`)

25 student records with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| StudentID | string | Unique identifier (e.g., S001) |
| Name | string | Full name |
| Department | string | CS / Electronics / Mechanical / Civil |
| Math | int | Marks out of 100 |
| Science | int | Marks out of 100 |
| English | int | Marks out of 100 |
| Computer | int | Marks out of 100 |
| Physics | int | Marks out of 100 |
| Attendance | int | Attendance percentage |

**Total possible marks:** 500 (5 subjects × 100)

---

## 4. Implementation

### File: `main.py`

The entire application is in one file for simplicity. It is organised as:

```
Constants → Helper Functions → Chart Functions → Page Functions → main()
```

#### Key sections

| Section | Description |
|---------|-------------|
| `compute_analytics(df)` | Adds Total, Average, Grade, Status columns using Pandas + NumPy |
| `assign_grade(avg)` | Loop over boundary list to return letter grade |
| `assign_status(avg)` | Returns "Pass" if avg ≥ 50 else "Fail" |
| `chart_*()` | Each function returns a Matplotlib `Figure` |
| `page_overview()` | KPI cards, subject averages, 4 charts |
| `page_records()` | Searchable/filterable table + CSV download |
| `page_top_performers()` | Ranked table + bar chart |
| `page_upload()` | CSV upload, analytics, download |
| `main()` | Page config, sidebar navigation, data loading, routing |

---

## 5. Grading Rules

```
Average ≥ 90  →  A+
Average ≥ 80  →  A
Average ≥ 70  →  B
Average ≥ 60  →  C
Average ≥ 50  →  D   (PASS boundary)
Average < 50  →  F   (FAIL)
```

Pass criterion: overall average across 5 subjects ≥ 50.

---

## 6. Features

### 📊 Class Overview
- Total students, pass percentage, class average, highest total
- Top scorer and lowest scorer at a glance
- Subject-wise average, highest, and lowest marks table
- Four charts: subject averages, grade distribution, top students, pass/fail

### 📋 Student Records
- Full data table with all computed columns
- Filter by: name search, department, grade, status, average range
- Download filtered results as CSV

### 🏅 Top Performers
- Adjustable leaderboard (top 3–25 students)
- Ranked by total marks

### 📤 Upload CSV
- Upload any compatible CSV
- Auto-computes analytics
- Download analyzed results
- Optional chart preview

---

## 7. Sample Results (from bundled dataset)

| Metric | Value |
|--------|-------|
| Total Students | 25 |
| Pass % | 92.0% |
| Class Average | 71.16 / 100 |
| Top Scorer | Pooja Joshi (CS) — 469 / 500 |
| Lowest Scorer | Manish Tiwari (Electronics) — 235 / 500 |
| Failing Students | 2 (Amit Kumar, Manish Tiwari) |
| Grade A+ students | 3 (Pooja Joshi, Ishaan Kapoor, Sneha Gupta) |

### Screenshots

> **Add your screenshots here before submission.**

**Class Overview page**
![Class Overview](screenshots/overview.png)

**Student Records page (with filters)**
![Student Records](screenshots/records.png)

**Top Performers page**
![Top Performers](screenshots/top_performers.png)

**Upload CSV page**
![Upload CSV](screenshots/upload.png)

*(Take screenshots by running `streamlit run main.py`, navigating to each page, and saving the images to a `screenshots/` folder inside the project.)*

---

## 8. Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| CSV column validation on upload | Check required columns before processing; show clear error |
| NaN values from empty CSV rows | `dropna()` can be added before compute_analytics if needed |
| Responsive layout | Streamlit `st.columns()` for multi-column layouts |
| Chart clarity | Added value labels on bars; used distinct colour palettes |

---

## 9. Learning Outcomes

After completing this project, you will have practised:

- Reading and manipulating tabular data with **Pandas**
- Performing array-level calculations with **NumPy**
- Writing reusable **functions** with clear inputs/outputs
- Using **conditions and loops** for grading logic
- Building a **multi-page Streamlit** web app
- Creating **Matplotlib** bar, pie, and horizontal bar charts
- Implementing **file upload and download** in a web app

---

## 10. Running the Project

```bash
# Step 1 – navigate to project folder
cd student_performance

# Step 2 – install dependencies
pip install -r requirements.txt

# Step 3 – launch dashboard
streamlit run main.py
```

The browser opens at http://localhost:8501 automatically.

---

## 11. GitHub Upload Instructions

> **Replace `<your-username>` with your actual GitHub username before running these commands.**

```bash
# Inside the student_performance/ folder:
git init
git add .
git commit -m "feat: Student Performance Analytics System"
git branch -M main
git remote add origin https://github.com/<your-username>/student-performance-analytics.git
git push -u origin main
```

**Repository URL:** `https://github.com/<your-username>/student-performance-analytics`

Recommended `.gitignore` entries:
```
__pycache__/
*.pyc
.streamlit/
screenshots/
```

---

*Project developed as part of a Python internship assignment.*
