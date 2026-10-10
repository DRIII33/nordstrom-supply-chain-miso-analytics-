# Nordstrom MISO Inventory Flow & Supplier Compliance Analytics

## Overview
This repository contains an end-to-end data analytics project built for the Data Analyst 3 role within Nordstrom's MISO Inventory team. It demonstrates advanced SQL data warehousing in Google BigQuery, Python-based data generation and orchestration, statistical hypothesis testing, and Looker Studio dashboarding.

## Repository Structure
* `/data`: Raw synthetic relational datasets (suppliers, shipments, replenishment).
* `/sql`: BigQuery SQL scripts for cleaning, staging, and dimensional modeling.
* `/scripts`: Google Colab notebooks for synthetic data generation and statistical analysis.
* `/dashboard`: Looker Studio schema and layout specifications.

## Getting Started
1. Clone the repository.
2. Execute `synthetic_data_generator.ipynb` in Google Colab to generate all required CSV files.
3. Upload CSVs into your Google BigQuery project (`driiiportfolio`).
4. Run SQL scripts sequentially (`01` through `02`) to build production analytical tables.
5. Connect Looker Studio to `fact_inventory_flow` for visualization.
