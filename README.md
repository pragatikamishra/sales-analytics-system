# SALES-ANALYTICS-SYSTEM

**Student Name:** pragatika Mishra
**Student ID:** bitsom_ba_25071756
**Email:** pragatika18mishra@gmail.com
**Date:** 20/01/2026


## Project Overview

The Sales Analytics System is designed to automate the processing, analysis, enrichment, and reporting of sales data. It helps businesses understand sales trends, top-performing products, customer behavior, and region-wise performance, while integrating external product data for enriched insights.

## Repository Structure

sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt (provided)
  |   |__ enriched_sales_data.txt (generated)
  ├── output/
  |   |__ sales_report.txt (generated)
  └── requirements.txt


## Key Learnings

Data Processing & Validation: Learned to clean, parse, and validate raw sales data from .txt files with custom delimiters.

Analytics & Insights: Gained experience calculating total revenue, average order value, top products/customers, region-wise performance, and daily sales trends.

API Integration & Enrichment: Learned to fetch product details via APIs and enrich transactions with category, brand, and rating while handling mismatches.

Reporting & Automation: Built automated, structured text reports and managed input/output files in a GitHub repository.

Modular Design & Error Handling: Developed modular Python code with robust error handling for smooth end-to-end workflow execution.

## Challenges Faced

Data Quality: Inconsistent formatting, missing fields, and extra delimiters in raw sales data.

Validation & Filtering: Ensuring only valid transactions pass and handling cases where filters exclude most data.

API Integration: Mapping ProductIDs and handling missing or unmatched API products.

Data Aggregation & Reporting: Calculating metrics accurately and formatting readable reports.

Debugging & Error Handling: Tracing errors across multiple modules and ensuring the workflow runs smoothly.
