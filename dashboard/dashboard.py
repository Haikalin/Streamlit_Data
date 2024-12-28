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
                        'customer_id', 'seller_id', 'freight_value'])

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
   seller_dist = df.groupby('seller_state')['seller_id'].nunique()
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
   customer_dist = df.groupby('customer_state')['customer_id'].nunique()
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

st.header("Freight Value Analysis")
col1, col2 = st.columns(2)
freight_df = filtered_df.groupby(['customer_state', 'seller_state'])['freight_value'].mean().reset_index()
freight_df['state_to_state'] = freight_df['customer_state'] + ' to ' + freight_df['seller_state']
freight_df = freight_df.drop(['customer_state', 'seller_state'], axis=1)

with col1:
   top_25_freight = freight_df.nlargest(25, 'freight_value')
   st.subheader("Top 25 State-to-State Freight Values")
   fig7, ax = plt.subplots(figsize=(10, 15))
   sns.barplot(data=top_25_freight, x='freight_value', y='state_to_state', ax=ax)
   plt.title("Top 25 State-to-State Freight Values")
   st.pyplot(fig7)

with col2:
   bottom_25_freight = freight_df.nsmallest(25, 'freight_value')
   st.subheader("Bottom 25 State-to-State Freight Values")
   fig8, ax = plt.subplots(figsize=(10, 15))
   sns.barplot(data=bottom_25_freight, x='freight_value', y='state_to_state', ax=ax)
   plt.title("Bottom 25 State-to-State Freight Values")
   st.pyplot(fig8)

#RFM Analysis
#Recency
#Recency
rfm_df = filtered_df.groupby('customer_id').agg(
   last_purchase=('order_purchase_timestamp', 'max')
).reset_index()

max_date = pd.to_datetime(rfm_df['last_purchase']).max()
rfm_df['recency'] = (max_date - pd.to_datetime(rfm_df['last_purchase'])).dt.days

#Frequency
frequency = filtered_df.groupby('customer_id').agg(
   frequency=('order_id', 'count')
).reset_index()

#Monetary 
monetary = filtered_df.groupby('customer_id').agg(
   monetary=('price', 'sum')
).reset_index()

# Merge metrics
rfm_df = rfm_df.merge(frequency, on='customer_id').merge(monetary, on='customer_id')

def r_score(x):
   if x <= 100:
       return 4
   elif x <= 200:
       return 3
   elif x <= 300:
       return 2
   elif x <= 400:
       return 1
   else:
       return 0

def f_score(x):
   if x > 5:
       return 4
   elif x > 4:
       return 3
   elif x > 3:
       return 2
   elif x > 2:
       return 1
   else:
       return 0

def m_score(x):
   if x > 2000:
       return 4
   elif x > 1500:
       return 3
   elif x > 1000:
       return 2
   elif x > 500:
       return 1
   else:
       return 0

# Apply scoring to create new columns
rfm_df['R'] = rfm_df['recency'].apply(r_score)
rfm_df['F'] = rfm_df['frequency'].apply(f_score)
rfm_df['M'] = rfm_df['monetary'].apply(m_score)
rfm_df['Total_RFM'] = rfm_df['R'] + rfm_df['F'] + rfm_df['M']

st.header("RFM Analysis")

fig9, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=rfm_df['Total_RFM'], bins=12)
plt.title("RFM Score Distribution")
st.pyplot(fig9)
   
# Key Metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
   st.metric("Total Orders", format(len(filtered_df), ','))
with col2:
   st.metric("Total Sales", f"R$ {filtered_df['price'].sum():,.2f}")
with col3:
   st.metric("Average Order Value", f"R$ {filtered_df['price'].mean():,.2f}")