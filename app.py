import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Sales Analysis", layout="wide")

# Title
st.title("Retail Sales Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales.csv")
    return df

df = load_data()

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Filtered SQL Analysis", "Top Products"])

# --- Tab 1: Overview ---
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Basic Statistics")
    st.write(df.describe())

    st.subheader("Category Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="category", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Tab 2: Filtered SQL Analysis ---
with tab2:
    category = st.selectbox("Select Category", sorted(df["category"].unique()))
    gender = st.selectbox("Select Gender", sorted(df["gender"].unique()))
    show_chart = st.checkbox("Show Age-wise Sales Trend")

    st.subheader(f"Sales Summary for {category} - {gender}")
    query = """
    SELECT category, gender, COUNT(*) AS transactions, SUM(total_sale) AS total_sale
    FROM df
    WHERE category = ? AND gender = ?
    GROUP BY category, gender
    """
    result = duckdb.execute(query, [category, gender]).df()
    st.dataframe(result)

    if show_chart:
        st.subheader("Sales Trend by Age")
        age_sales_query = """
        SELECT age, SUM(total_sale) AS total_sale
        FROM df
        WHERE category = ? AND gender = ?
        GROUP BY age
        ORDER BY age
        """
        sales_by_age = duckdb.execute(age_sales_query, [category, gender]).df()

        fig, ax = plt.subplots()
        sns.set_style("whitegrid")
        sns.lineplot(data=sales_by_age, x="age", y="total_sale", marker="o", ax=ax)
        ax.set_title(f"Age-wise Sales for {category} - {gender}")
        st.pyplot(fig)

# --- Tab 3: Top Products ---
with tab3:
    st.subheader("Top Selling Products")
    top_n = st.slider("Select Number of Products", min_value=5, max_value=50, value=10)
    query = """
    SELECT product_id, product_name, SUM(total_sale) AS total_sale
    FROM df
    GROUP BY product_id, product_name
    ORDER BY total_sale DESC
    LIMIT ?
    """
    top_products = duckdb.execute(query, [top_n]).df()
    st.dataframe(top_products)

    fig, ax = plt.subplots()
    sns.barplot(data=top_products, x="total_sale", y="product_name", ax=ax)
    ax.set_title(f"Top {top_n} Selling Products")
    st.pyplot(fig)
