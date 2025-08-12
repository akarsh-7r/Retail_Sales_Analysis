# 🛒 SQL Retail Sales Analysis Project

## 📌 Project Overview

This project focuses on analyzing retail sales data using SQL. The goal is to perform data cleaning, exploration, and business-focused analysis to gain insights into customer behavior, product performance, and sales trends.

---

## 🗃️ Database & Table Structure

- **Database Name**: `sql_project_p2`
- **Table Name**: `retail_sales`

### Table Schema:

| Column Name       | Data Type   | Description                                 |
|-------------------|-------------|---------------------------------------------|
| transaction_id    | INT         | Unique identifier for each transaction      |
| sale_date         | DATE        | Date of sale                                |
| sale_time         | TIME        | Time of sale                                |
| customer_id       | INT         | Unique identifier for the customer          |
| gender            | VARCHAR(15) | Gender of the customer                      |
| age               | INT         | Age of the customer                         |
| category          | VARCHAR(15) | Product category                            |
| quantity          | INT         | Number of items sold                        |
| price_per_unit    | FLOAT       | Price per unit item                         |
| cogs              | FLOAT       | Cost of goods sold                          |
| total_sale        | FLOAT       | Total sale amount for the transaction       |

---

## 🧹 Data Cleaning

The data was checked for and cleaned by removing any rows with `NULL` values in key columns such as:

- `transaction_id`
- `sale_date`
- `sale_time`
- `gender`
- `category`
- `quantity`
- `cogs`
- `total_sale`

---

## 🔍 Data Exploration

### Key Questions Answered:

| Question No. | Description |
|--------------|-------------|
| Q1 | Sales made on a specific date |
| Q2 | Clothing sales with quantity > 10 in Nov 2022 |
| Q3 | Total sales per category |
| Q4 | Average age of customers in the 'Beauty' category |
| Q5 | Transactions with total sale > 1000 |
| Q6 | Transactions count by gender and category |
| Q7 | Best-selling month each year based on average sale |
| Q8 | Top 5 customers by total sales |
| Q9 | Unique customers per category |
| Q10 | Orders by shift: Morning, Afternoon, Evening |

---

## 📊 Sample Insights

- 📆 **Best-selling month**: Identified using average monthly sales with `RANK()`.
- 🧍‍♀️ **Gender insights**: Grouped by `category` and `gender` to understand preferences.
- 🛍️ **Top category by revenue**: Found by aggregating `total_sale`.
- 🕒 **Shift analysis**: Orders grouped by time of day (Morning <12, Afternoon 12–17, Evening >17).
- 💰 **High-value customers**: Top 5 customers by total spend identified.

---

## 🛠️ Technologies Used

- SQL (PostgreSQL / MySQL compatible queries)
- SQL functions: `EXTRACT()`, `RANK()`, `CASE`, `GROUP BY`, `JOIN` (optional)
- Database Tools: pgAdmin / MySQL Workbench / DB Browser for SQLite

---

## 📁 How to Run

1. Create the database:
   ```sql
   CREATE DATABASE sql_project_p2;
2. Create the table:
3. Use the CREATE TABLE retail_sales schema shown above.

4. Import the dataset into the retail_sales table using your SQL tool or CSV import utility.

5. Run analysis queries from any SQL editor to generate insights and answer the business questions listed.

📌 Conclusion
This project offers a complete introduction to SQL data analysis using real-world retail data. From setting up the database and cleaning data to exploring trends and answering business questions, it helps build foundational SQL skills crucial for data analyst roles.

---

## 📁 LIVE SITE
https://retailsalesanalysis-ku9bcfqlow9sozsilihupk.streamlit.app/

