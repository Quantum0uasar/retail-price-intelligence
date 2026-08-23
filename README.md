# Retail Demand & Price Intelligence Dashboard

A portfolio data analytics project that analyzes public Brazilian e-commerce transaction data to surface patterns in category performance, customer behavior, pricing, demand, and freight costs.

The project uses Python and SQL to clean, validate, model, and prepare data for an interactive Tableau dashboard. Findings are based on historical public data and are intended for portfolio analysis only.

## Business Problem

Retail pricing and category-management teams need a clear way to monitor commercial performance and identify areas that may warrant further pricing review.

This project transforms historical e-commerce transactions into decision-support analysis that helps users explore:

- Which product categories generate the most revenue and sales volume
- How sales trends change over time
- How average prices, units sold, and freight burden differ across categories
- Which categories appear more price-sensitive in historical data
- Which customer groups demonstrate different purchasing behavior
- Which categories may deserve further commercial or pricing review

## Project Features

- Cleans and validates raw Olist e-commerce data using Python and Pandas
- Loads cleaned data into a SQLite database
- Uses SQL queries and views to calculate business metrics
- Estimates category-level price elasticity using log-log OLS regression
- Segments customers with RFM analysis and K-Means clustering
- Exports analytics-ready datasets for Tableau
- Presents commercial performance, pricing patterns, and customer insights in Tableau Public

## Tableau Dashboard

> **Tableau Public dashboard:** [Retail Demand & Price Intelligence Dashboard](https://public.tableau.com/app/profile/jaideep.singh4215/viz/RetailDemandPriceIntelligenceDashboard/Dashboard1#1)

The Tableau dashboard contains the following analysis views:

- **Executive Overview:** KPI cards, monthly revenue trends, category performance, and geographic performance
- **Pricing & Demand:** Price-versus-quantity analysis, average price comparisons, freight burden, and estimated category elasticity
- **Customer Segmentation:** RFM-based customer groups and spending behavior
- **Category Drill-Down:** Filters for category, date, and commercial metrics
- **Insights & Recommendations:** Portfolio findings that identify patterns for additional pricing or category review

> **Tableau Public dashboard:** Add your published Tableau Public link here after publishing.

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- Statsmodels
- Scikit-learn
- Tableau Public
- Git and GitHub

## Data Pipeline

```text
Olist Public CSV Files
        ↓
Python + Pandas ETL and Validation
        ↓
SQLite Database
        ↓
SQL Business Analysis and Analytics Views
        ↓
Elasticity Modeling + Customer Segmentation
        ↓
Tableau-Ready CSV Exports
        ↓
Interactive Tableau Dashboard
```

## ETL and Validation

The raw Olist CSV files are loaded and processed with Pandas before analysis.

Key preparation steps include:

1. Removing duplicate records
2. Handling missing values
3. Converting date columns to valid datetime values
4. Filtering for completed customer orders
5. Validating prices, freight values, and quantities
6. Creating analysis fields such as order month, revenue, average price, and freight burden
7. Loading cleaned tables into SQLite

Validation rules and assumptions should be documented in the project methodology.

## SQL Analysis

SQL is used to prepare business metrics and Tableau-ready tables, including:

- Monthly revenue and order trends
- Category revenue, units sold, and average selling price
- Product-level sales performance
- Freight cost relative to product price
- Customer purchase behavior
- Top- and bottom-performing categories
- Analytics views for Tableau reporting

## Price Elasticity Analysis

The project estimates category-level price elasticity using a log-log OLS regression model:

```text
log(quantity) = β0 + β1 × log(price)
```

The price coefficient, \(β1\), represents the estimated elasticity.

For example:

```text
Elasticity = -2.0
```

This means a 1% higher historical price was associated with approximately 2% lower demand in the model.

More negative values suggest stronger historical price sensitivity. These estimates are descriptive associations and should not be interpreted as causal evidence.

## Customer Segmentation

Customers are grouped with RFM analysis:

- **Recency:** How recently a customer purchased
- **Frequency:** How often a customer purchased
- **Monetary:** How much a customer spent

RFM measures are standardized with `StandardScaler`, then K-Means clustering assigns customers to behavioral segments.

This helps illustrate differences among high-value, repeat, recent, and lower-spending customer groups.

## Commercial Performance Analysis

The dashboard evaluates category performance through metrics such as:

- Revenue
- Orders and units sold
- Average selling price
- Average freight cost
- Freight burden relative to product price
- Historical estimated elasticity
- Customer-segment contribution

These metrics help users compare categories and identify areas that may merit further business review.

## Strategic Use Case

A retail pricing, consulting, or analytics team could use an analysis like this to:

- Monitor category-level revenue and demand trends
- Identify categories with historically price-sensitive demand
- Compare sales volume, prices, and freight burden across product groups
- Explore potential risks associated with price changes
- Understand differences among customer segments
- Prioritize categories for deeper pricing, promotion, or operational analysis

## Important Limitations

The Olist dataset is public, historical, and observational.

- Elasticity estimates represent historical associations, not proven causal effects
- Promotions, seasonality, product mix, seller behavior, product quality, competition, and other factors may affect demand
- The dataset does not include full product cost or COGS information, so this project does not measure true profitability
- Findings are portfolio analysis and are not real-world business recommendations
- Tableau visualizations are intended to support exploration of the dataset, not to make automated pricing decisions

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**

The dataset contains approximately:

- 99,000 customers
- 96,000 delivered orders
- 112,000 order items
- 32,000 products

Add the original dataset source and license link here.

## Running the Project

Create and activate a virtual environment:

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

Create Tableau-ready data exports:

```bash
python src/export_tableau_data.py
```

Open the exported files in Tableau Desktop or Tableau Public, build the dashboard, and publish it to Tableau Public.

## Project Structure

```text
retail-price-intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── tableau/
│
├── database/
│   └── retail.db
│
├── src/
│   ├── etl.py
│   └── export_tableau_data.py
│
├── sql/
│   ├── analysis.sql
│   └── tableau_marts.sql
│
├── models/
│   ├── elasticity.py
│   └── segmentation.py
│
├── dashboard/
│   ├── tableau_screenshots/
│   └── tableau_public_link.txt
│
├── docs/
│   ├── data_dictionary.md
│   └── methodology.md
│
├── requirements.txt
└── README.md
```

## Project Goal

The goal of this project is to demonstrate a practical analytics workflow that combines data cleaning, data validation, SQL, statistical modeling, customer segmentation, and Tableau dashboard development.

It is designed to show how raw public transaction data can be converted into reproducible, business-oriented analysis for retail pricing and category-management use cases.
