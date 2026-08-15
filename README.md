# E-Commerce Sales Analysis with Python

## Project Overview
This project analyzes e-commerce sales data using Python. It demonstrates data loading, cleaning, business metric calculation, product analysis, category analysis, and data visualization.

## Objectives
- Calculate total revenue
- Calculate total units sold
- Identify the best-selling product
- Identify the highest-revenue product
- Analyze sales performance by category
- Generate business insights
- Create visualizations automatically

## Technologies Used
- Python
- Pandas
- Matplotlib
- Git
- GitHub

## Project Structure

ecommerce-sales-analysis-python/
│
├── data/
│   └── sales.csv
├── outputs/
│   ├── cleaned_sales_data.csv
│   ├── product_summary.csv
│   ├── category_summary.csv
│   ├── business_summary.txt
│   ├── revenue_by_product.png
│   ├── units_sold_by_product.png
│   └── revenue_by_category.png
├── sales_analysis.py
├── requirements.txt
├── .gitignore
└── README.md

## Analysis Performed
The project:
1. Loads sales data from a CSV file.
2. Checks whether the required columns exist.
3. Removes duplicate and invalid records.
4. Converts quantity and price into numeric values.
5. Calculates revenue for each record.
6. Calculates important business KPIs.
7. Groups results by product and category.
8. Generates charts.
9. Saves processed results into the outputs folder.

## Key Metrics
The analysis identifies:
- Total Revenue
- Total Units Sold
- Average Revenue
- Best-Selling Product
- Highest-Revenue Product

## Visualizations
The project automatically generates:
- Revenue by Product
- Units Sold by Product
- Revenue by Category

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
