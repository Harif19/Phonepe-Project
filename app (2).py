import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json

# -------------------------------
# DB Path & Connection
# -------------------------------
DB_PATH = "/content/project_files/phonepe_pulse.db"

@st.cache_data
def load_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Load India GeoJSON
with open("/content/India states.geojson", "r") as f:
    india_geo = json.load(f)

# -------------------------------
# Helper: Normalize state names
# -------------------------------
def normalize_state_names(df, column="state"):
    mapping = {
        "andaman-&-nicobar-islands": "Andaman and Nicobar",
        "dadara-&-nagar-havelli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
        "jammu-&-kashmir": "Jammu and Kashmir",
        "delhi": "Delhi",
        "odisha": "Odisha",
        "pondicherry": "Puducherry"
    }
    df[column] = df[column].str.replace("-", " ").str.title().replace(mapping)
    return df

# -------------------------------
# Helper: Download button
# -------------------------------
def add_download_button(df, label):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"⬇️ Download {label} as CSV",
        data=csv,
        file_name=f"{label.replace(' ','_').lower()}.csv",
        mime="text/csv"
    )

# -------------------------------
# Streamlit Layout
# -------------------------------
st.set_page_config(page_title="PhonePe Pulse Project", layout="wide")

st.title("📊 PhonePe Pulse Project")
st.markdown("An interactive dashboard inspired by **PhonePe Pulse** using our SQLite DB.")

# Sidebar Filters
st.sidebar.header("🔎 Explore Data")
data_type = st.sidebar.radio("Select Data Type", ["Transactions", "Insurance"])
year = st.sidebar.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])

# -------------------------------
# Home Page Map + Bar
# -------------------------------
if data_type == "Transactions":
    query = f"""
    SELECT state, SUM(amount) as total_amount
    FROM aggregated_transaction
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_amount DESC;
    """
    df = load_data(query)
    st.subheader(f"💰 Transactions - {year} Q{quarter}")

    if not df.empty:
        df = normalize_state_names(df, "state")

        # Debug: Compare DB vs GeoJSON states
        st.write("📝 DB States:", df["state"].unique())
        st.write("🗺️ GeoJSON States:", [s["properties"]["name"] for s in india_geo["features"]])

        fig_map = px.choropleth(
            df,
            geojson=india_geo,
            featureidkey="properties.name",  # ✅ fixed
            locations="state",
            color="total_amount",
            color_continuous_scale="Blues",
            title="Transaction Amount by State"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)

        fig_bar = px.bar(df, x="state", y="total_amount",
                         title="Transaction Amount by State",
                         labels={"total_amount": "₹ Amount"}, text_auto=".2s")
        st.plotly_chart(fig_bar, use_container_width=True)

        add_download_button(df, "Transaction_Data")

else:
    query = f"""
    SELECT state, SUM(amount) as total_amount
    FROM aggregated_insurance
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_amount DESC;
    """
    df = load_data(query)
    st.subheader(f"🛡️ Insurance - {year} Q{quarter}")

    if not df.empty:
        df = normalize_state_names(df, "state")

        st.write("📝 DB States:", df["state"].unique())
        st.write("🗺️ GeoJSON States:", [s["properties"]["name"] for s in india_geo["features"]])

        fig_map = px.choropleth(
            df,
            geojson=india_geo,
            featureidkey="properties.name",  # ✅ fixed
            locations="state",
            color="total_amount",
            color_continuous_scale="Greens",
            title="Insurance Amount by State"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)

        fig_bar = px.bar(df, x="state", y="total_amount",
                         title="Insurance Amount by State",
                         labels={"total_amount": "₹ Amount"}, text_auto=".2s")
        st.plotly_chart(fig_bar, use_container_width=True)

        add_download_button(df, "Insurance_Data")

# -------------------------------
# Business Case Studies (Tabs)
# -------------------------------
st.markdown("## 📂 Business Case Studies")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Case Study 1: Transaction Dynamics",
    "Case Study 2: Device Dominance",
    "Case Study 3: Insurance Growth",
    "Case Study 4: User Engagement",
    "Case Study 5: Geo Transactions"
])

# CASE 1
with tab1:
    st.subheader("Case Study 1: Decoding Transaction Dynamics")
    query = """
    SELECT year, SUM(amount) AS yearly_amount
    FROM aggregated_transaction
    GROUP BY year
    ORDER BY year;
    """
    df = load_data(query)
    fig = px.line(df, x="year", y="yearly_amount", markers=True,
                  title="Yearly Transaction Growth")
    st.plotly_chart(fig, use_container_width=True)
    add_download_button(df, "Case1_Yearly_Transactions")

# CASE 2
with tab2:
    st.subheader("Case Study 2: Device Dominance and User Engagement")
    query = """
    SELECT brand, SUM(count) AS total_users
    FROM aggregated_user
    WHERE brand != 'TOTAL'
    GROUP BY brand
    ORDER BY total_users DESC
    LIMIT 10;
    """
    df = load_data(query)
    fig = px.bar(df, x="brand", y="total_users",
                 title="Top Device Brands by Users", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)
    add_download_button(df, "Case2_Device_Dominance")

# CASE 3
with tab3:
    st.subheader("Case Study 3: Insurance Penetration & Growth")
    query = """
    SELECT year, SUM(amount) AS yearly_insurance_amount
    FROM aggregated_insurance
    GROUP BY year
    ORDER BY year;
    """
    df = load_data(query)
    fig = px.line(df, x="year", y="yearly_insurance_amount", markers=True,
                  title="Yearly Insurance Growth")
    st.plotly_chart(fig, use_container_width=True)
    add_download_button(df, "Case3_Insurance_Growth")

# CASE 4
with tab4:
    st.subheader("Case Study 4: User Engagement and Growth")
    query = """
    SELECT year, SUM(count) AS yearly_users
    FROM aggregated_user
    WHERE brand = 'TOTAL'
    GROUP BY year
    ORDER BY year;
    """
    df = load_data(query)
    fig = px.line(df, x="year", y="yearly_users", markers=True,
                  title="Yearly Registered Users")
    st.plotly_chart(fig, use_container_width=True)
    add_download_button(df, "Case4_User_Engagement")

# CASE 5
with tab5:
    st.subheader("Case Study 5: Transaction Analysis Across Geo")
    query = """
    SELECT state, SUM(amount) AS total_amount
    FROM aggregated_transaction
    WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
    GROUP BY state
    ORDER BY total_amount DESC
    LIMIT 10;
    """
    df = load_data(query)
    df = normalize_state_names(df, "state")
    fig = px.bar(df, x="state", y="total_amount",
                 title="Top States by Transaction Amount (Latest Year)", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)
    add_download_button(df, "Case5_Geo_Transactions")
