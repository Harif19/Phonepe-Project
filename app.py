import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import requests
from pyngrok import ngrok
import time

# -------------------------------
# NGROK SETUP
# -------------------------------
NGROK_TOKEN = "33W8aNQvOwRd7wbQB2rRLIy1tod_6oZzTz9tBRRzehoJEJVJd"
ngrok.set_auth_token(NGROK_TOKEN)

# -------------------------------
# DATABASE PATH
# -------------------------------
DB_PATH = "/content/project_files/phonepe_pulse.db"

# -------------------------------
# Cached DB Loader
# -------------------------------
@st.cache_data
def load_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# -------------------------------
# GeoJSON for India Map
# -------------------------------
geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
india_geo = requests.get(geojson_url).json()

# -------------------------------
# Helper Functions
# -------------------------------
def normalize_state_names(df, column="state"):
    df[column] = df[column].str.replace("-", " ").str.title()
    mapping = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Nct Of Delhi": "Delhi",
        "Jammu & Kashmir": "Jammu And Kashmir",
        "Dadra & Nagar Havelli & Daman & Diu": "Dadra And Nagar Haveli And Daman And Diu"
    }
    df[column] = df[column].replace(mapping)
    return df

def add_download_button(df, label):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {label} (CSV)",
        data=csv,
        file_name=f"{label.replace(' ','_').lower()}.csv",
        mime="text/csv"
    )

# -------------------------------
# PAGE CONFIG + STYLING
# -------------------------------
st.set_page_config(page_title="PhonePe Pulse Analytics", layout="wide")

st.markdown('''
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1c1c1e;
}
[data-testid="stSidebar"] {
    background-color: #1f2937;
    color: #f5f5f7;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
    color: #f5f5f7 !important;
}
h1 { font-size: 28px !important; color: #111827; margin-bottom: 0.5em; }
.metric-dark {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 10px;
    color: white !important;
    text-align: center;
}
</style>
''', unsafe_allow_html=True)

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("📈 Dashboard Navigation")
page = st.sidebar.radio("Select Section", ["Overview", "Case Studies"])

# -------------------------------
# OVERVIEW PAGE
# -------------------------------
if page == "Overview":
    st.title("PhonePe Pulse Analytics Dashboard")
    st.caption("A professional insights dashboard for transaction and insurance analytics across India.")
    st.markdown("---")

    data_type = st.sidebar.radio("Data Type", ["Transactions", "Insurance"])
    year = st.sidebar.selectbox("Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
    quarter = st.sidebar.selectbox("Quarter", [1, 2, 3, 4])

    if data_type == "Transactions":
        query = f'''SELECT state, SUM(amount) as total_amount
FROM aggregated_transaction
WHERE year = {year} AND quarter = {quarter}
GROUP BY state
ORDER BY total_amount DESC;'''
        df = load_data(query)
        st.subheader(f"Transactions Overview — {year} Q{quarter}")

        if not df.empty:
            df = normalize_state_names(df)
            col1, col2 = st.columns([2, 1])
            with col1:
                fig_map = px.choropleth(df, geojson=india_geo, featureidkey="properties.ST_NM",
                                        locations="state", color="total_amount",
                                        color_continuous_scale="blues", title="State-wise Transaction Values")
                fig_map.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig_map, use_container_width=True)
            with col2:
                st.markdown("<div class='metric-dark'>", unsafe_allow_html=True)
                st.markdown(f"<h4>Top Performing State</h4><h2>{df.iloc[0]['state']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h4>Total Value (₹)</h4><h2>{df['total_amount'].sum():,.0f}</h2>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
            fig_bar = px.bar(df, x="state", y="total_amount", text_auto=".2s", color="total_amount",
                             title="Transaction Value by State")
            st.plotly_chart(fig_bar, use_container_width=True)
            add_download_button(df, "Transaction_Data")

    else:
        query = f'''SELECT state, SUM(amount) as total_amount
FROM aggregated_insurance
WHERE year = {year} AND quarter = {quarter}
GROUP BY state
ORDER BY total_amount DESC;'''
        df = load_data(query)
        st.subheader(f"Insurance Overview — {year} Q{quarter}")

        if not df.empty:
            df = normalize_state_names(df)
            col1, col2 = st.columns([2, 1])
            with col1:
                fig_map = px.choropleth(df, geojson=india_geo, featureidkey="properties.ST_NM",
                                        locations="state", color="total_amount",
                                        color_continuous_scale="greens", title="State-wise Insurance Distribution")
                fig_map.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig_map, use_container_width=True)
            with col2:
                st.markdown("<div class='metric-dark'>", unsafe_allow_html=True)
                st.markdown(f"<h4>Top State (Insurance)</h4><h2>{df.iloc[0]['state']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h4>Total Value (₹)</h4><h2>{df['total_amount'].sum():,.0f}</h2>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
            fig_bar = px.bar(df, x="state", y="total_amount", text_auto=".2s", color="total_amount",
                             title="Insurance Amount by State")
            st.plotly_chart(fig_bar, use_container_width=True)
            add_download_button(df, "Insurance_Data")

# -------------------------------
# CASE STUDIES PAGE
# -------------------------------
elif page == "Case Studies":
    st.title("Analytical Case Studies")
    st.caption("In-depth exploration of PhonePe Pulse data across multiple analytical perspectives.")
    st.markdown("---")

    case_selected = st.selectbox(
        "Select Case Study",
        [
            "Case Study 1: Transaction Dynamics",
            "Case Study 2: Device Dominance & User Engagement",
            "Case Study 3: Insurance Growth & Penetration",
            "Case Study 4: User Growth & Engagement",
            "Case Study 5: Geo-based Transaction Insights"
        ]
    )

    # -----------------------------------------------------
    # ✅ CASE STUDY 1 — Transaction Dynamics (Updated Q4, Q5)
    # -----------------------------------------------------
    if "Case Study 1" in case_selected:
        st.subheader("Case Study 1 — Transaction Dynamics")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])

        # Q1
        with tabs[0]:
            df = load_data("SELECT state, SUM(amount) AS total_amount FROM aggregated_transaction GROUP BY state ORDER BY total_amount DESC LIMIT 10;")
            st.header("Top 10 States by Transaction Amount")
            fig = px.bar(df, x="state", y="total_amount", text_auto=".2s")
            st.plotly_chart(fig)

        # Q2
        with tabs[1]:
            df = load_data("SELECT year, SUM(amount) AS yearly_amount FROM aggregated_transaction GROUP BY year;")
            st.header("Yearly Transaction Trend")
            fig = px.line(df, x="year", y="yearly_amount", markers=True)
            st.plotly_chart(fig)

        # Q3
        with tabs[2]:
            df = load_data("SELECT state, year, quarter, SUM(amount) AS total_amount FROM aggregated_transaction WHERE state='karnataka' GROUP BY state, year, quarter;")
            st.header("Quarterly Growth — Karnataka")
            fig = px.line(df, x="quarter", y="total_amount", color="year", markers=True)
            st.plotly_chart(fig)

        # Q4
        with tabs[3]:
            df = load_data("""SELECT category, year,
                   ROUND(SUM(amount)/10000000, 2) AS total_amount_cr,
                   ROUND(SUM(amount)*100.0/SUM(SUM(amount)) OVER(PARTITION BY year),2) AS category_share_percent
            FROM aggregated_transaction
            GROUP BY category, year
            ORDER BY year, total_amount_cr DESC;""")
            st.header("Category Growth & Share by Year")
            fig = px.bar(df, x="category", y="total_amount_cr", color="year", barmode="group")
            st.plotly_chart(fig)

        # Q5
        with tabs[4]:
            df = load_data("""WITH yearly_data AS (
                SELECT category, year, SUM(amount) AS total_amount
                FROM aggregated_transaction
                WHERE year IN (2022,2023)
                GROUP BY category, year
            ),
            pivoted AS (
                SELECT category,
                       SUM(CASE WHEN year=2022 THEN total_amount ELSE 0 END) AS amt_2022,
                       SUM(CASE WHEN year=2023 THEN total_amount ELSE 0 END) AS amt_2023
                FROM yearly_data GROUP BY category
            )
            SELECT category,
                   ROUND(amt_2022/10000000,2) AS amount_2022_cr,
                   ROUND(amt_2023/10000000,2) AS amount_2023_cr,
                   ROUND(((amt_2023-amt_2022)*100.0/NULLIF(amt_2022,0)),2) AS growth_percent
            FROM pivoted ORDER BY growth_percent DESC LIMIT 10;""")
            st.header("Emerging Categories (2022 → 2023)")
            fig = px.bar(df, x="category", y="growth_percent", color="growth_percent")
            st.plotly_chart(fig)

    # -----------------------------------------------------
    # ✅ CASE STUDY 2 — Device Dominance (Updated Q3)
    # -----------------------------------------------------
    elif "Case Study 2" in case_selected:
        st.subheader("Case Study 2 — Device Dominance & User Engagement")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])

        # Q1 — Top Device Brands
        with tabs[0]:
            df = load_data("SELECT brand, SUM(count) AS total_users FROM aggregated_user WHERE brand != 'TOTAL' GROUP BY brand ORDER BY total_users DESC LIMIT 10;")
            st.header("Top 10 Device Brands (All Years)")
            st.plotly_chart(px.bar(df, x="brand", y="total_users", color="total_users"))

        # Q2 — Yearly App Opens
        with tabs[1]:
            df = load_data("SELECT year, SUM(percentage) AS total_app_opens FROM aggregated_user WHERE brand='TOTAL' GROUP BY year ORDER BY year;")
            st.header("Yearly App Opens Across India")
            st.plotly_chart(px.line(df, x="year", y="total_app_opens", markers=True))

        # Q3 — Device Market Share (Updated)
        with tabs[2]:
            df = load_data("""WITH valid_year AS (
                SELECT MAX(year) AS yr FROM aggregated_user WHERE brand != 'TOTAL'
            ),
            top_state AS (
                SELECT state FROM aggregated_user WHERE brand='TOTAL'
                GROUP BY state ORDER BY SUM(count) DESC LIMIT 1
            )
            SELECT au.state, au.brand, SUM(au.count) AS total_users,
                   ROUND(SUM(au.count)*100.0 / SUM(SUM(au.count)) OVER(), 2) AS market_share_percent
            FROM aggregated_user au
            JOIN top_state ts ON au.state = ts.state
            JOIN valid_year vy ON au.year = vy.yr
            WHERE au.brand != 'TOTAL'
            GROUP BY au.state, au.brand
            ORDER BY total_users DESC;""")
            st.header("Device Market Share in Top State (Latest Valid Year)")
            st.plotly_chart(px.pie(df, names="brand", values="market_share_percent"))

        # Q4 — Top States by Registered Users
        with tabs[3]:
            df = load_data("SELECT state, SUM(count) AS total_users FROM aggregated_user WHERE brand='TOTAL' AND year=(SELECT MAX(year) FROM aggregated_user) GROUP BY state ORDER BY total_users DESC LIMIT 5;")
            st.header("Top 5 States by Registered Users (Latest Year)")
            st.plotly_chart(px.bar(df, x="state", y="total_users", color="total_users"))

        # Q5 — Xiaomi Quarterly Trend
        with tabs[4]:
            df = load_data("SELECT year, quarter, SUM(count) AS xiaomi_users FROM aggregated_user WHERE brand='Xiaomi' GROUP BY year, quarter ORDER BY year, quarter;")
            df["period"] = df["year"].astype(str) + '-Q' + df["quarter"].astype(str)
            st.header("Xiaomi Quarterly User Growth (All India)")
            st.plotly_chart(px.line(df, x="period", y="xiaomi_users", markers=True))


    # -----------------------------------------------------
    # ✅ CASE STUDY 3 — Insurance Growth
    # -----------------------------------------------------
    elif "Case Study 3" in case_selected:
        st.subheader("Case Study 3 — Insurance Growth & Penetration")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])
        with tabs[0]:
            df = load_data("SELECT state, SUM(amount) AS total_insurance_amount FROM aggregated_insurance GROUP BY state ORDER BY total_insurance_amount DESC LIMIT 10;")
            st.header("Top 10 States by Insurance Amount")
            fig = px.bar(df, x="state", y="total_insurance_amount", text_auto=".2s")
            st.plotly_chart(fig)
        with tabs[1]:
            df = load_data("SELECT year, SUM(amount) AS yearly_insurance_amount FROM aggregated_insurance GROUP BY year;")
            st.header("Yearly Insurance Growth")
            fig = px.line(df, x="year", y="yearly_insurance_amount", markers=True)
            st.plotly_chart(fig)
        with tabs[2]:
            df = load_data("SELECT year, quarter, SUM(amount) AS quarterly_amount FROM aggregated_insurance WHERE state='karnataka' GROUP BY year, quarter;")
            st.header("Quarterly Growth — Karnataka")
            fig = px.line(df, x="quarter", y="quarterly_amount", color="year", markers=True)
            st.plotly_chart(fig)
        with tabs[3]:
            df = load_data("SELECT state, SUM(amount) AS total_amount FROM aggregated_insurance GROUP BY state ORDER BY total_amount DESC LIMIT 5;")
            st.header("Top 5 States by Total Insurance")
            fig = px.bar(df, x="state", y="total_amount", text_auto=".2s")
            st.plotly_chart(fig)
        with tabs[4]:
            df = load_data("""SELECT t.state, ROUND(SUM(i.amount)/SUM(t.amount)*100,2) AS penetration_percent
            FROM aggregated_transaction t JOIN aggregated_insurance i ON t.state=i.state
            GROUP BY t.state ORDER BY penetration_percent DESC LIMIT 10;""")
            st.header("Insurance Penetration by State")
            fig = px.bar(df, x="state", y="penetration_percent", color="penetration_percent")
            st.plotly_chart(fig)

    # -----------------------------------------------------
    # ✅ CASE STUDY 4 — User Growth
    # -----------------------------------------------------
    elif "Case Study 4" in case_selected:
        st.subheader("Case Study 4 — User Growth & Engagement")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])
        with tabs[0]:
            df = load_data("SELECT state, SUM(count) AS total_users FROM aggregated_user WHERE brand='TOTAL' AND year=(SELECT MAX(year) FROM aggregated_user) GROUP BY state ORDER BY total_users DESC LIMIT 10;")
            st.header("Top 10 States by Registered Users")
            fig = px.bar(df, x="state", y="total_users", text_auto=".2s")
            st.plotly_chart(fig)
        with tabs[1]:
            df = load_data("SELECT year, SUM(count) AS yearly_users FROM aggregated_user WHERE brand='TOTAL' GROUP BY year;")
            st.header("Yearly User Growth")
            fig = px.line(df, x="year", y="yearly_users", markers=True)
            st.plotly_chart(fig)
        with tabs[2]:
            df = load_data("SELECT year, quarter, SUM(percentage) AS total_app_opens FROM aggregated_user WHERE brand='TOTAL' AND state='karnataka' GROUP BY year, quarter;")
            st.header("App Opens — Karnataka")
            fig = px.line(df, x="quarter", y="total_app_opens", color="year")
  # -----------------------------------------------------
    # ✅ CASE STUDY 5 — Geo-based Transaction Insights (Updated Q3)
    # -----------------------------------------------------
    elif "Case Study 5" in case_selected:
        st.subheader("Case Study 5 — Geo-based Transaction Insights")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])

        # Q1 — Top States
        with tabs[0]:
            df = load_data("""SELECT state, SUM(amount) AS total_amount
                               FROM aggregated_transaction
                               WHERE year=(SELECT MAX(year) FROM aggregated_transaction)
                               GROUP BY state
                               ORDER BY total_amount DESC
                               LIMIT 10;""")
            st.header("Top 10 States by Transaction Value (Latest Year)")
            fig = px.bar(df, x="state", y="total_amount", text_auto=".2s", color="total_amount")
            st.plotly_chart(fig)
            add_download_button(df, "Top_States")

        # Q2 — Top Districts
        with tabs[1]:
            df = load_data("""SELECT entityName AS district, SUM(amount) AS total_amount
                               FROM top_transaction
                               WHERE level='districts'
                               GROUP BY entityName
                               ORDER BY total_amount DESC
                               LIMIT 10;""")
            st.header("Top 10 Districts by Transaction Value")
            fig = px.bar(df, x="district", y="total_amount", text_auto=".2s", color="total_amount")
            st.plotly_chart(fig)
            add_download_button(df, "Top_Districts")

        # Q3 — UPDATED: Fastest-Growing States (2022 → 2023)
        with tabs[2]:
            df = load_data("""WITH yearly_data AS (
                                SELECT state, year, SUM(amount) AS total_amount
                                FROM aggregated_transaction
                                WHERE year IN (2022, 2023)
                                GROUP BY state, year
                             ),
                             pivoted AS (
                                SELECT state,
                                       SUM(CASE WHEN year=2022 THEN total_amount ELSE 0 END) AS amt_2022,
                                       SUM(CASE WHEN year=2023 THEN total_amount ELSE 0 END) AS amt_2023
                                FROM yearly_data GROUP BY state
                             )
                             SELECT state,
                                    ROUND(amt_2022/10000000,2) AS amount_2022_cr,
                                    ROUND(amt_2023/10000000,2) AS amount_2023_cr,
                                    ROUND(((amt_2023-amt_2022)*100.0/NULLIF(amt_2022,0)),2) AS growth_percent
                             FROM pivoted
                             ORDER BY growth_percent DESC
                             LIMIT 10;""")
            st.header("Fastest-Growing States by Transaction Value (2022 → 2023)")
            fig = px.bar(df, x="state", y="growth_percent", color="growth_percent",
                         text_auto=".2f", title="Top 10 Fastest-Growing States (%)")
            st.plotly_chart(fig)
            add_download_button(df, "State_Growth_2022_2023")

        # Q4 — Yearly Transaction Growth
        with tabs[3]:
            df = load_data("""SELECT year, SUM(amount) AS yearly_amount
                               FROM aggregated_transaction
                               GROUP BY year
                               ORDER BY year;""")
            st.header("Yearly Transaction Growth Across India")
            fig = px.line(df, x="year", y="yearly_amount", markers=True)
            st.plotly_chart(fig)
            add_download_button(df, "Yearly_Transaction_Growth")

        # Q5 — State Contribution Share (Latest Year)
        with tabs[4]:
            df = load_data("""WITH total AS (
                                SELECT SUM(amount) AS national_total
                                FROM aggregated_transaction
                                WHERE year=(SELECT MAX(year) FROM aggregated_transaction)
                             )
                             SELECT state,
                                    SUM(amount) AS state_total,
                                    ROUND(SUM(amount)*100.0/(SELECT national_total FROM total),2) AS contribution_percent
                             FROM aggregated_transaction
                             WHERE year=(SELECT MAX(year) FROM aggregated_transaction)
                             GROUP BY state
                             ORDER BY state_total DESC
                             LIMIT 10;""")
            st.header("Top 10 States by National Contribution Share")
            fig = px.bar(df, x="state", y="contribution_percent", color="contribution_percent",
                         text_auto=".2f", title="State Contribution to National Total (%)")
            st.plotly_chart(fig)
            add_download_button(df, "State_Contribution_Share")

