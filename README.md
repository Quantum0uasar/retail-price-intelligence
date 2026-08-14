# Retail Price Elasticity & Demand Intelligence Dashboard

A data science project that analyzes Brazilian e-commerce transactions to identify **price-sensitive product categories, customer segments, and potential pricing opportunities**.

## Business Problem

Retail companies need to understand how customers react to different prices.

This project turns historical sales data into insights that can help pricing and consulting teams make more informed commercial decisions.

## What This Project Does

* Cleans raw Olist e-commerce data using **Python and Pandas**
* Loads cleaned data into a **SQLite database**
* Uses **SQL queries** to analyze revenue, prices, order trends, and freight costs
* Estimates **price elasticity of demand** by product category using OLS regression
* Creates customer groups using **RFM analysis and K-Means clustering**
* Simulates how price changes could affect demand and revenue
* Displays the results in an interactive **Streamlit + Plotly dashboard**

## Tech Stack

* Python
* Pandas
* SQLite
* SQL
* Statsmodels
* Scikit-learn
* Streamlit
* Plotly

## Data Pipeline

```text
Olist CSV Files
      ↓
Python + Pandas ETL
      ↓
SQLite Database
      ↓
SQL Business Analysis
      ↓
Price Elasticity + Customer Segmentation
      ↓
Streamlit + Plotly Dashboard
```

## ETL Pipeline

The raw Olist CSV files are first loaded using Pandas.

The pipeline then:

1. Removes duplicate records
2. Handles missing values
3. Converts dates into usable datetime values
4. Filters for completed customer orders
5. Validates price and freight values
6. Loads cleaned datasets into SQLite

This creates one structured database that can be queried using SQL.

## SQL Analysis

The project uses SQL to answer business questions such as:

* Which product categories generate the most revenue?
* How does order volume change over time?
* What are the average, minimum, and maximum prices by category?
* Which categories have high shipping costs relative to product price?

## Price Elasticity Analysis

Price elasticity estimates how strongly customer demand changes when product prices change.

The project uses a log-log OLS regression:

```text
log(quantity) = β0 + β1 × log(price)
```

The price coefficient represents the estimated elasticity.

For example:

```text
Elasticity = -2.0
```

This means that historically, a **1% higher price was associated with roughly 2% lower demand**.

More negative values indicate stronger price sensitivity.

## Price Change Simulator

The Streamlit dashboard includes an interactive slider that allows a user to simulate a price increase or decrease.

Using the estimated elasticity, the dashboard calculates:

* Estimated demand change
* Estimated revenue change

This allows users to explore possible pricing scenarios visually.

## Customer Segmentation

Customers are analyzed using RFM:

* **Recency** — how recently the customer purchased
* **Frequency** — how often the customer purchased
* **Monetary** — how much the customer spent

The RFM variables are standardized using `StandardScaler`.

K-Means clustering then groups customers into four behavioral segments.

These groups can help a retailer understand differences between high-value, frequent, recent, and lower-spending customers.

## Category Commercial Performance

The dashboard compares product categories using:

* Revenue
* Average selling price
* Units sold
* Freight burden

The Plotly visualization makes it easier to identify categories with strong sales performance or unusually high shipping costs.

## Strategic Pricing Use Case

A pricing or consulting team could use this type of analysis to:

* Identify categories where customers appear highly price-sensitive
* Evaluate potential risks from price increases
* Identify categories where moderate price changes may be less risky
* Understand valuable customer groups
* Compare commercial performance across categories
* Support pricing recommendations using historical data instead of intuition alone

## Important Limitations

The Olist dataset is observational rather than experimental.

Therefore, the elasticity estimates represent **historical associations**, not guaranteed causal effects.

Other factors such as promotions, seasonality, product mix, seller behavior, and competition may also influence demand.

The dataset also does not provide product cost or COGS information, so this project analyzes **commercial performance rather than true profitability**.

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**

The dataset contains approximately:

* 99,000 customers
* 96,000 delivered orders
* 112,000 order items
* 32,000 products

## Running the Project

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline:

```bash
python src/etl.py
```

Run the price elasticity model:

```bash
python models/elasticity.py
```

Run the customer segmentation model:

```bash
python models/segmentation.py
```

Start the dashboard:

```bash
streamlit run dashboard/app.py
```

## Project Structure

```text
retail-price-intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── retail.db
│
├── src/
│   └── etl.py
│
├── sql/
│   └── analysis.sql
│
├── models/
│   ├── elasticity.py
│   └── segmentation.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## Project Goal

The goal of this project is to demonstrate how **data engineering, SQL, statistics, machine learning, and interactive visualization** can be combined to support real-world retail pricing decisions.
