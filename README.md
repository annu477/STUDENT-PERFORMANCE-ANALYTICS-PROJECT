# Student Performance Analytics System

A beginner-friendly web dashboard built with **Python, Pandas, NumPy, Streamlit, and Matplotlib** that analyses student academic performance from a CSV dataset.

---

## Quick Start

### 1. Install dependencies
```bash
cd student_performance
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run main.py
```
The app opens automatically at **http://localhost:8501**

---

## Project Structure
```
student_performance/
├── main.py           # Streamlit dashboard (all logic)
├── students.csv      # Sample dataset (25 students)
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── Project_Documentation.md
```

---

## Features
| Feature | Description |
|---------|-------------|
| Class Overview | KPI cards, subject averages, highest/lowest scorer |
| Student Records | Searchable & filterable table with CSV download |
| Top Performers | Ranked leaderboard with adjustable N |
| Upload CSV | Analyse your own dataset and download results |
| Charts | Subject averages bar, grade distribution pie, pass/fail bar, top-students bar |

---

## Grading Rules
| Grade | Average Marks |
|-------|--------------|
| A+    | ≥ 90 |
| A     | ≥ 80 |
| B     | ≥ 70 |
| C     | ≥ 60 |
| D     | ≥ 50 |
| F     | < 50 |

**Pass criterion:** Overall average ≥ 50

---

## Dataset Columns
`StudentID, Name, Department, Math, Science, English, Computer, Physics, Attendance`

---

## GitHub Upload
```bash
git init
git add .
git commit -m "Initial commit: Student Performance Analytics System"
git remote add origin https://github.com/<your-username>/student-performance-analytics.git
git push -u origin main
```
