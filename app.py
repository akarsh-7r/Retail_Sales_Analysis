import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="Retail SQL Dashboard", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
<style>
/* Page background and text */
.stApp {
    background: linear-gradient(to bottom right, #f9f9f9, #dce3f3);
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}

/* Title */
h1 {
    font-size: 2.5rem !important;
    font-weight: 700;
    color: #2c3e50;
    padding-top: 10px;
}

/* Subheaders */
h2, h3 {
    color: #2c3e50;
    margin-top: 1rem;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    color: #1a1a1a !important;
    font-weight: 600;
    text-align: center;
}

/* Visual blocks */
.stDataFrame, .stPyplot, .element-container:has(> .stPlotlyChart) {
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
    background-color: #ffffff;
    padding: 1.2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background-color: #ccc;
    margin: 2rem 0;
}

/* Footer */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🛍️ Retail Sales SQL Dashboard")
st.markdown("Explore retail sales data by category, gender, and more. Powered by SQL + Python + Streamlit.")

# --- Load CSV ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Data_Set.csv")
        df.columns = df.columns.str.lower()  # Normalize column names
        return df
    except FileNotFoundError:
        st.error("❌ Data_Set.csv not found in the working directory.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Create DuckDB table
    duckdb.sql("CREATE OR REPLACE TABLE retail_sales AS SELECT * FROM df")

    # --- Sidebar Filters ---
    st.sidebar.header("📌 Filters")
    category = st.sidebar.selectbox("Select Category", sorted(df["category"].dropna().unique()))
    gender = st.sidebar.selectbox("Select Gender", sorted(df["gender"].dropna().unique()))
    show_chart = st.sidebar.checkbox("Show Sales Chart", value=True)
    show_table = st.sidebar.checkbox("Show Data Table", value=True)

    # --- Tabs Layout ---
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔎 Filtered Analysis", "📊 Full Category Breakdown"])

    # --- Tab 1: KPIs ---
    with tab1:
        total_sales = df["total_sale"].sum()
        total_customers = df["customer_id"].nunique()
        avg_sale = df["total_sale"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"₹{total_sales:,.0f}")
        col2.metric("Unique Customers", f"{total_customers}")
        col3.metric("Average Sale", f"₹{avg_sale:.2f}")

    # --- Tab 2: Filtered SQL Analysis ---
    with tab2:
        st.subheader(f"Sales Summary for {category} - {gender}")
        query = """
        SELECT category, gender, COUNT(*) AS transactions, SUM(total_sale) AS total_sale
        FROM retail_sales
        WHERE category = ? AND gender = ?
        GROUP BY category, gender
        """
        result = duckdb.sql(query, [category, gender]).df()
        st.dataframe(result)

        if show_chart:
            st.subheader("Sales Trend by Age")
            age_sales_query = """
            SELECT age, SUM(total_sale) AS total_sale
            FROM retail_sales
            WHERE category = ? AND gender = ?
            GROUP BY age
            ORDER BY age
            """
            sales_by_age = duckdb.sql(age_sales_query, [category, gender]).df()

            fig, ax = plt.subplots()
            sns.set_style("whitegrid")
            sns.lineplot(data=sales_by_age, x="age", y="total_sale", marker="o", ax=ax)
            ax.set_title(f"Age-wise Sales for {category} - {gender}")
            st.pyplot(fig)

    # --- Tab 3: Full Category Breakdown ---
    with tab3:
        st.subheader("📊 Sales by Category")
        breakdown_query = """
        SELECT category, SUM(total_sale) AS total_sale
        FROM retail_sales
        GROUP BY category
        ORDER BY total_sale DESC
        """
        sales_by_category = duckdb.sql(breakdown_query).df()

        col1, col2 = st.columns([2, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=sales_by_category, y="category", x="total_sale", ax=ax, palette="viridis")
            ax.set_xlabel("Total Sale")
            ax.set_ylabel("Category")
            st.pyplot(fig)

        with col2:
            if show_table:
                st.dataframe(sales_by_category)

    # --- Footer ---
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and SQL | [GitHub](https://github.com) | [LinkedIn](https://linkedin.com)")
