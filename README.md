# Brazilian E-Commerce Analysis by Haikal Assyauqi

## Overview
This project is a comprehensive analysis of Brazilian E-Commerce data sourced from the Olist platform. Conducted as part of the IDCamp Data Analysis program, the analysis spans transactions from 2016 to 2018. The dataset encompasses various dimensions such as orders, customers, products, and sellers. Out of the eight available tables, the analysis focuses on four key ones:

- **Orders**
- **Customers**
- **Order Items**
- **Products**

## Key Objectives
1. Identify patterns and trends in the e-commerce data.
2. Provide actionable insights to improve business strategies.
3. Visualize key metrics through an interactive dashboard.

---

## Prerequisites
Ensure you have the following tools installed before running the project:

```bash
pip install jupyter notebook pandas matplotlib seaborn streamlit
```

---

## Installation & Setup

### 1. Clone the Repository
Clone the project repository to your local machine:

```bash
git clone https://github.com/Haikalin/Streamlit_Data.git
```

### 2. Navigate to the Project Directory
Change the current directory to the project folder:

```bash
cd Streamlit_Data
```

### 3. Install Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Run Jupyter Notebook
To explore the analysis and run individual cells:

Click on the `notebook.ipynb` file and click "Run" on each cell or "Run All" to execute the entire notebook.

### Run Streamlit Dashboard Locally
For an interactive dashboard:

```bash
streamlit run dashboard/dashboard.py
```

### Access the Online Dashboard
Alternatively, view the dashboard hosted online:

[**Online Dashboard**](https://haikal-brazilmarket.streamlit.app/)

---

## Project Structure
The repository is structured as follows:

```
.
Streamlit_Data
    │   notebook.ipynb
    │   README.md
    │   requirements.txt
    │   url.txt
    │   
    ├───dashboard
    │       dashboard.py
    │       main_data.csv
    │       
    └───dataset
            customers_dataset.csv
            orders_dataset.csv
            order_items_dataset.csv
            sellers_dataset.csv
```

---

## Tech Stack
The following technologies and libraries were used in this project:

- **Python 3.x**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib**: Visualization library for static plots.
- **Seaborn**: Statistical data visualization.
- **Streamlit**: Framework for building the interactive dashboard.

---

## Features
1. **Descriptive Analysis**: Summary statistics for orders, products, and customers.
2. **Trend Analysis**: Time-series analysis to identify key patterns.
3. **Product Insights**: Breakdown of product categories, prices, and sales.
4. **Customer Behavior**: Analysis of purchase frequency and locations.
5. **Interactive Dashboard**: Dynamic visualizations for deeper insights.

---

## Author
This project was developed by **Haikal Assyauqi** as part of the IDCamp Data Analysis program.

For inquiries or collaboration, feel free to reach out via GitHub: [Haikalin](https://github.com/Haikalin).

---

## Future Enhancements
- Incorporate additional tables from the dataset for deeper insights.
- Implement machine learning models for predictive analytics.
- Expand dashboard functionalities with advanced visualizations.