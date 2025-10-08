📊 PhonePe Pulse Data Analysis & Visualization
📁 Project Overview

This project provides an end-to-end data analysis and visualization pipeline using the PhonePe Pulse dataset — a comprehensive collection of digital transaction data across India.
It extracts, processes, analyzes, and visualizes the data to uncover business insights and user transaction patterns.

## Objectives

Extract JSON data from the PhonePe Pulse GitHub repository

Transform and store data into a SQLite database

Perform SQL-based analytics for multiple business case studies

Build an interactive Streamlit dashboard with map visualization

Present state-wise and category-wise insights into digital payments in Indi

---

# 📂 Project Structure

project/
│-- project_files/
│   ├── data_extraction.py           # Extracts JSON → SQLite database
│   ├── case1_transactions.py        # Transaction performance analysis
│   ├── case2_users.py               # User growth and behavior
│   ├── case3_insurance.py           # Insurance adoption & trends
│   ├── case4_top_category.py        # Top transaction categories by state
│   ├── case5_map_visualization.py   # Geo-map for regional insights
│   ├── phonepe_pulse.db             # SQLite database file
│   ├── utils.py                     # Helper functions
│   └── run_all_cases.py             # Integrates all analyses
│
│-- app.py                          # Streamlit dashboard (final visualization)
│-- India_States.geojson             # GeoJSON file for India map boundaries
│-- Project Final.ipynb              # End-to-end notebook version
│-- README.md                        # Project documentation



---

Business Case Studies

Transaction Analysis → Top states, category share, and quarterly growth

User Trends → Registered users, app opens, and active ratios

Insurance Insights → Yearly growth, total value, penetration patterns

Top Categories → Contribution of top-performing transaction categories

Geo Visualization → Regional transaction heatmap by state and district 

---

## Dashboard Demo


<img width="1914" height="894" alt="Dashboard Homepage" src="https://github.com/user-attachments/assets/a9997ff3-002c-40b8-9685-ef0743e2b705" />

<img width="1913" height="873" alt="Case Studies Page" src="https://github.com/user-attachments/assets/cb510abc-7bd7-45ab-93cb-46382f72703a" />

<img width="1914" height="885" alt="Case Studies Page 2" src="https://github.com/user-attachments/assets/f05469a7-53c3-4744-b39f-391c80004358" />
---


## 📈 Key Insights

Digital transactions in India have grown 10× from 2018–2024

Maharashtra, Karnataka, Tamil Nadu lead in total transaction value

Peer-to-Peer (P2P) transfers dominate payment types

Xiaomi, Samsung, Vivo remain top devices among users

Insurance coverage shows consistent year-over-year growth

Southern states show higher engagement and digital adoption

---

## #▶️ Run Locally
1. Clone repository
git clone https://github.com/yourusername/phonepe_pulse_project.git
cd phonepe_pulse_project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run main.py



