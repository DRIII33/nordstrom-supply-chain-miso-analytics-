# Executive Summary: Nordstrom Supply Chain & MISO Modernization Pipeline

## 1. Context & Business Mandate
As Nordstrom accelerates its omnichannel strategy, ensuring seamless inventory movement across distribution centers and retail stores is paramount. The Merchandising Insights & Strategic Operations (MISO) team requires robust, real-time analytics to monitor inbound logistics, store replenishment (RP), and supplier compliance. This project transitions legacy reporting to a modern Google Cloud stack (BigQuery and Looker Studio).

## 2. Solution Architecture
* **Ingestion & Orchestration:** Simulated Apache Airflow and Python pipelines.
* **Warehousing & Transformation:** Google Cloud BigQuery (`driiiportfolio`) utilizing normalized staging tables and unified fact models (`fact_inventory_flow`).
* **BI & Visualization:** Looker Studio operational dashboards providing self-service visibility for Merch Ops and Replenishment leaders.

## 3. Key Findings & Strategic Impact
* **Tier Disparities:** Statistical analysis confirms that Tier 3 vendors exhibit a significantly higher lead time variance (avg. +4.2 days) compared to Tier 1 strategic partners.
* **Replenishment Efficiency:** Store fulfillment fill rates average 88%, with inventory stockouts concentrated in high-velocity SKUs during late shipment cycles.
* **Operational Modernization:** Migrating legacy queries to BigQuery eliminates manual spreadsheet reporting, saving an estimated 14 hours per week in reconciliation labor.
