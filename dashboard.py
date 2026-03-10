import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def millions(x, pos):
    return f"{x/1_000_000:.1f}M"


df = pd.read_csv("data/sales_data_sample.csv", encoding="latin1")


st.title("Sales Dashboard")

st.markdown("Interactive dashboard analyzing sales performance by country, product category and time.")


country = st.selectbox("Select Country", df["COUNTRY"].unique())

filtered_df = df[df["COUNTRY"] == country]


st.write("Preview of dataset")
st.write(filtered_df.head())


st.subheader("Key Metrics")

total_sales = filtered_df["SALES"].sum()
average_sales = filtered_df["SALES"].mean()
number_of_orders = filtered_df["ORDERNUMBER"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"{total_sales:,.2f}")

with col2:
    st.metric("Average Sale", f"{average_sales:,.2f}")

with col3:
    st.metric("Number of Orders", number_of_orders)


st.subheader("Sales by Country")

sales_country = filtered_df.groupby("COUNTRY")["SALES"].sum()

fig, ax = plt.subplots()
sales_country.sort_values().plot(kind="barh", ax=ax)

ax.set_xlabel("Sales")
ax.set_ylabel("Country")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(millions))

st.pyplot(fig)


st.subheader("Sales by Product Category")

product_category = (
    filtered_df.groupby("PRODUCTLINE")["SALES"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
product_category.sort_values().plot(kind="barh", ax=ax2)

ax2.set_xlabel("Sales")
ax2.set_ylabel("Product Category")
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(millions))

st.pyplot(fig2)

st.subheader("Sales Over Time")

sales_year = filtered_df.groupby("YEAR_ID")["SALES"].sum()

fig3, ax3 = plt.subplots()
ax3.plot(sales_year.index, sales_year.values, marker="o")

ax3.set_xticks(sales_year.index)
ax3.set_xticklabels(sales_year.index.astype(int))
ax3.set_xlabel("Year")
ax3.set_ylabel("Sales")
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(millions))

st.pyplot(fig3)