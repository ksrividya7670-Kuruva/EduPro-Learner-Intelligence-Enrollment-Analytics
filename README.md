# 🎓 EduPro: Learner Demographics and Course Enrollment Behavior Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Analytics](https://img.shields.io/badge/Domain-Educational%20Data%20Mining-indigo.svg)]()
[![Partner](https://img.shields.io/badge/Partner-Toronto%20Parks%2C%20Forestry%20%26%20Rec-emerald.svg)]()

> **A High-Dimensional Empirical Investigation into Educational Participation, Cross-Demographic Course Selection, and Behavioral Segmentation on EduPro.**

---

## 📌 Executive Summary

Modern online learning platforms cater to diverse learners with varying ages, gender distributions, and educational objectives. For a digital education platform like **EduPro**, understanding who learners are and how they choose courses is foundational for designing relevant curricula, improving retention, targeted community outreach, and enhancing inclusivity.

This repository hosts the complete codebase, high-dimensional datasets, academic research paper, policy briefings, and production Streamlit analytics dashboard developed in collaboration with **Unified Mentor** and the **City of Toronto Government – Parks, Forestry & Recreation**.

---

## 🚀 Key Performance Indicators (KPIs)

| Metric | Empirical Value | Context & Benchmark |
| :--- | :---: | :--- |
| **Total Registered Learners** | **2,017** | 100% data preservation and referential integrity across all source records. |
| **Total Course Enrollments** | **4,228** | Active learning interactions spanning 2024–2026. |
| **Average Enrollments per User** | **2.10 courses** | Healthy multi-course engagement (66.8% multi-course retention). |
| **Platform Gender Parity** | **1.037 : 1 (F:M)** | **50.92% Female (1,027)** vs. **49.08% Male (990)**; high baseline accessibility. |
| **Youth Participation (<18)** | **15.12% (305 learners)** | Concentrated in Beginner coursework (**68.49%**); prime youth hub focus. |
| **Young Adults (18–25)** | **36.64% (739 learners)** | Core intermediate demographic (**43.98%**) preparing for the tech workforce. |
| **Working Professionals (26–35)**| **48.24% (973 learners)** | Accounts for **53.57% of total enrollments** and **74.6% of advanced certifications**. |
| **Technical Demand Share** | **64.29%** | AI/Data Science (22.8%), Software Engineering (21.9%), Cybersecurity (19.6%). |

---

## 🔬 Core Empirical Findings & Statistical Tests

### 1. Age Maturity Governs Course Difficulty ($\chi^2 = 640.94, p < 10^{-100}$)
* **Adolescents (<18)** concentrate heavily in **Beginner courses (68.49%)**, exploring foundational coding and digital media.
* **Young Adults (18–25)** form the core **Intermediate tier (43.98%)**.
* **Working Professionals (26–35)** drive the vast majority of **Advanced certifications (74.6%)**.

### 2. Disciplinary Variation by Gender ($\chi^2 = 293.24, p < 10^{-60}$)
* **Female Learners:** Higher engagement in *Data Science & AI* (24.9% vs. 20.6%), *Digital Design & UI/UX* (14.9% vs. 9.2%), and *Public Health Analytics* (11.5% vs. 8.8%).
* **Male Learners:** Higher participation in *Cybersecurity & Cloud* (23.9% vs. 15.3%) and *Software Engineering* (24.4% vs. 19.5%).
* **Business & Leadership:** Near-perfect gender parity (13.9% Female vs. 13.0% Male).

### 3. Five Unsupervised Learner Personas ($K$-Means)
1. **Youth Foundational Explorers (15.1%):** Mean age 16.2 yrs; beginner coding & digital arts.
2. **Young Career Accelerators (36.6%):** Mean age 21.8 yrs; full-stack dev and data science certifications.
3. **Professional Power Specialists (26.2%):** Mean age 31.4 yrs; advanced cyber, big data & cloud architecture.
4. **Creative Digital Practitioners (12.1%):** Mean age 24.5 yrs; UI/UX, interaction prototyping & Figma.
5. **Civic & Public Upskillers (10.0%):** Mean age 28.6 yrs; healthcare systems and community recreation analytics.

---

## 📂 Project Repository Structure

```
EduPro-Learner-Intelligence-Enrollment-Analytics/
├── app.py                                   # Production Streamlit Analytics Dashboard
├── requirements.txt                         # Python dependencies
├── README.md                                # Comprehensive project documentation
├── .gitignore                               # Git ignored files
│
├── data/                                    # Datasets & analytical summaries
│   ├── users.csv                            # 2,017 verified learner profiles
│   ├── courses.csv                          # 36 high-dimensional course catalog
│   ├── transactions.csv                     # 4,228 transactional enrollment records
│   ├── integrated_dataset.csv               # Merged analytical master view
│   ├── edupro_dataset.xlsx                  # 4-sheet master Excel workbook
│   └── eda_summary.json                     # Precomputed statistical metrics
│
├── deliverables/                            # Academic & policy deliverables
│   ├── research_paper.md                    # Formal Academic Research Paper (APA/IEEE)
│   ├── research_paper.html                  # Print-ready, styled pre-print paper (Save as PDF)
│   └── executive_summary_stakeholders.md    # Briefing for Toronto Parks, Forestry & Rec
│
└── scripts/                                 # Data generation & processing pipelines
    ├── convert_paper.py                     # Markdown to academic HTML converter
    ├── generate_datasets.py                 # Referential data synthesis script
    └── run_eda.py                           # EDA and Chi-Square statistical pipeline
```

---

## ⚡ Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ksrividya7670-Kuruva/EduPro-Learner-Intelligence-Enrollment-Analytics.git
cd EduPro-Learner-Intelligence-Enrollment-Analytics
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the Interactive Dashboard
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📑 Deliverables Overview

* 📄 **[Academic Research Paper](deliverables/research_paper.md):** Complete academic research paper documenting methodology, empirical findings, contingency tables, hypothesis testing, and pedagogical recommendations.
* 🏛️ **[Executive Summary for Stakeholders](deliverables/executive_summary_stakeholders.md):** Policy and operational roadmap tailored for municipal leadership.
* 📊 **[Master Excel Dataset](data/edupro_dataset.xlsx):** Relational workbook containing `Users`, `Courses`, `Transactions`, and `Integrated_Data`.

---

## 🤝 Stakeholders & Acknowledgments
* **Unified Mentor:** Academic research guidance and learning analytics framework.
* **City of Toronto Government – Parks, Forestry & Recreation:** Civic public upskilling partnership and youth digital literacy context.
