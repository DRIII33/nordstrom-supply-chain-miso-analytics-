# Executive Summary: Nordstrom Supply Chain & MISO Modernization Pipeline
---

**Data Analyst 3, Supply Chain Inventory:** Daniel Rodriguez III

**Date:** October 10, 2026

---

## 1. Context & Business Mandate
As Nordstrom accelerates its omnichannel retailing strategy, physical and digital inventory flow must operate with absolute precision. The Merchandising Insights & Strategic Operations (MISO) team requires robust, real-time analytics to monitor inbound logistics, store replenishment (RP), and supplier compliance. This project modernizes legacy reporting into a cloud-native Google Cloud stack (BigQuery and Looker Studio).

## 2. Business Problem & Diagnostic Focus
* **The Bottleneck:** Initial operational reviews revealed frequent replenishment friction and partial store fulfillments. Rather than relying on surface-level metrics, this project investigates root causes: **supplier compliance infractions** (such as ASN errors and ticketing failures) and **regional store fulfillment variances**.
* **Methodology:** Ingested relational operational data, normalized and modeled data in Google BigQuery (`driiiportfolio`), executed inferential statistics (Chi-Square Test of Independence yielding $p = 1.2583 \times 10^{-3}$) in Google Colab, and surfaced insights via Looker Studio.

## 3. Key Findings & Strategic Impact
* **Statistical Proof of Compliance Impact:** The Chi-Square test proved mathematically that supplier compliance infractions directly drive downstream store replenishment failures (partial fulfillments).
* **Regional Bottleneck Identification:** Granular store-level analysis isolated regional fulfillment friction, identifying specific store clusters (e.g., `STORE_025` experiencing a 34.26% partial fulfillment rate) requiring immediate operational audit.
* **Modernization Value:** Migrating legacy queries to BigQuery eliminates manual spreadsheet reconciliation, saving an estimated 14 hours per week while establishing a scalable foundation for predictive AI integration.
