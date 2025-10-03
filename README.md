# Phonepe-Project
An end-to-end Data Analysis &amp; Visualization project built on the official PhonePePulse dataset .  

# PhonePe Pulse - Transaction Insights

 
The project extracts raw JSON data, loads it into a SQL database, performs business analysis, and visualizes insights in an **interactive Streamlit dashboard**.

---

##  Features
- Extracted & cleaned **PhonePe Pulse JSON data**
- Built **SQLite database** with multiple tables
- Designed **25+ SQL queries** across 5 business case studies
- Developed an **interactive dashboard** with:
  - India Map (GeoJSON-based)
  - Sidebar filters (Year, Quarter, Data Type)
  - Tabs for business case studies
- Exportable **CSV downloads** for all insights

---

## Tech Stack
- **Python**: pandas, sqlite3, json
- **SQL**: SQLite (can migrate to MySQL/PostgreSQL)
- **Streamlit**: Dashboard UI
- **Plotly Express**: Interactive charts & maps
- **GeoJSON**: India State boundaries
- **GitHub**: Version control

---

# 📂 Project Structure

project/
│-- data_extraction/ # Scripts to parse JSON → DB
│-- project_files/
│ ├── phonepe_pulse.db # SQLite database
│ ├── case1_transactions.py
│ ├── case2_devices.py
│ ├── case3_insurance.py
│ ├── case4_engagement.py
│ ├── case5_transactions_geo.py
│ ├── utils.py
│ └── run_all_cases.py
│-- app.py # Streamlit dashboard
│-- India states.geojson # India map file
│-- README.md # Documentation


---

## Business Case Studies
1. **Transaction Dynamics** → Top states, yearly & quarterly growth, payment categories  
2. **Device Dominance** → Top devices, Xiaomi quarterly trend, state device share  
3. **Insurance Growth** → Yearly growth, state contribution, penetration analysis  
4. **User Engagement** → Registered users, app opens, engagement ratio  
5. **Geo Transactions** → Hotspots by state, district, and pincode  

---

## Dashboard Demo
<img width="1910" height="904" alt="Dashboard 1" src="https://github.com/user-attachments/assets/20b4c8bc-937c-4b90-9244-563b4a6ca97b" />

<img width="1914" height="886" alt="Dashboard 2" src="https://github.com/user-attachments/assets/c0603eb4-2a64-4a16-8a27-b57a8c6f6208" />



---

## 📈 Key Insights
- Transactions grew **10x from 2018–2024**
- **Maharashtra, Karnataka, Telangana** lead in transactions
- **Xiaomi, Samsung, Vivo** dominate device usage
- Insurance is **under-penetrated** but growing fast
- Engagement ratio higher in **Southern states**

---

## ▶️ Run Locally
```bash
# 1. Clone repo
git clone https://github.com/yourusername/phonepe_pulse_project.git
cd phonepe_pulse_project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit app
streamlit run app.py


