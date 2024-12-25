import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Turn off scientific notation
pd.options.display.float_format = '{:,.2f}'.format

# Set page title
st.set_page_config(page_title="Brazilian E-commerce Analysis", layout="wide")

# Load data with specific columns
df = pd.read_csv("dashboard/main_data.csv", 
                usecols=['seller_state', 'customer_state', 'price', 
                        'order_id', 'order_purchase_timestamp',
                        'customer_id', 'seller_id'])

# Convert date column
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Get min and max dates for the filter
min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

# Title
st.title("Brazilian E-commerce Analysis Dashboard")

# Date Filter in sidebar
st.sidebar.header("Filters")
start_date = st.sidebar.date_input('Start Date', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('End Date', max_date, min_value=min_date, max_value=max_date)

# Filter data based on date
if start_date and end_date:
   mask = (df['order_purchase_timestamp'].dt.date >= start_date) & \
          (df['order_purchase_timestamp'].dt.date <= end_date)
   filtered_df = df.loc[mask]
else:
   filtered_df = df

# Analysis by State
st.header("State Analysis")
col1, col2 = st.columns(2)

with col1:
   st.subheader("Sales by Seller State")
   
   # Number of Orders
   fig1, ax1 = plt.subplots(figsize=(10, 6))
   seller_orders = filtered_df.groupby('seller_state')['order_id'].count().sort_values(ascending=True)
   seller_orders.plot(kind='barh')
   plt.title('Number of Orders by Seller State')
   plt.xlabel('Number of Orders')
   st.pyplot(fig1)
   
   # Total Money
   fig2, ax2 = plt.subplots(figsize=(10, 6))
   seller_money = filtered_df.groupby('seller_state')['price'].sum().sort_values(ascending=True)
   seller_money.plot(kind='barh')
   plt.title('Total Sales by Seller State (R$)')
   ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
   plt.xlabel('Total Sales (R$)')
   st.pyplot(fig2)

with col2:
   st.subheader("Orders by Customer State")
   
   # Number of Orders
   fig3, ax3 = plt.subplots(figsize=(10, 6))
   customer_orders = filtered_df.groupby('customer_state')['order_id'].count().sort_values(ascending=True)
   customer_orders.plot(kind='barh')
   plt.title('Number of Orders by Customer State')
   plt.xlabel('Number of Orders')
   st.pyplot(fig3)
   
   # Total Money
   fig4, ax4 = plt.subplots(figsize=(10, 6))
   customer_money = filtered_df.groupby('customer_state')['price'].sum().sort_values(ascending=True)
   customer_money.plot(kind='barh')
   plt.title('Total Purchases by Customer State (R$)')
   ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
   plt.xlabel('Total Purchases (R$)')
   st.pyplot(fig4)

# Add Donut Charts
st.header("Top 8 States Distribution")
col1, col2 = st.columns(2)

with col1:
   st.subheader("Seller States Distribution")
   
   # Calculate seller state distribution
   seller_dist = filtered_df.groupby('seller_state')['seller_id'].nunique()
   seller_dist = seller_dist.sort_values(ascending=False)
   
   # Separate top 8 and others
   top_8_sellers = seller_dist.head(8)
   others_sellers = pd.Series({'Others': seller_dist[8:].sum()})
   seller_plot_data = pd.concat([top_8_sellers, others_sellers])
   
   # Create donut chart
   fig5, ax5 = plt.subplots(figsize=(10, 10))
   plt.pie(seller_plot_data, labels=seller_plot_data.index, autopct='%1.1f%%', pctdistance=0.85)
   centre_circle = plt.Circle((0,0), 0.70, fc='white')
   fig5.gca().add_artist(centre_circle)
   plt.title("Distribution of Sellers by State (Top 8)")
   st.pyplot(fig5)

with col2:
   st.subheader("Customer States Distribution")
   
   # Calculate customer state distribution
   customer_dist = filtered_df.groupby('customer_state')['customer_id'].nunique()
   customer_dist = customer_dist.sort_values(ascending=False)
   
   # Separate top 8 and others
   top_8_customers = customer_dist.head(8)
   others_customers = pd.Series({'Others': customer_dist[8:].sum()})
   customer_plot_data = pd.concat([top_8_customers, others_customers])
   
   # Create donut chart
   fig6, ax6 = plt.subplots(figsize=(10, 10))
   plt.pie(customer_plot_data, labels=customer_plot_data.index, autopct='%1.1f%%', pctdistance=0.85)
   centre_circle = plt.Circle((0,0), 0.70, fc='white')
   fig6.gca().add_artist(centre_circle)
   plt.title("Distribution of Customers by State (Top 8)")
   st.pyplot(fig6)

# Key Metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
   st.metric("Total Orders", format(len(filtered_df), ','))
with col2:
   st.metric("Total Sales", f"R$ {filtered_df['price'].sum():,.2f}")
with col3:
   st.metric("Average Order Value", f"R$ {filtered_df['price'].mean():,.2f}")