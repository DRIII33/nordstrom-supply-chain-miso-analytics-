CREATE OR REPLACE TABLE `driiiportfolio.nordstrom_supply_chain.stg_suppliers` AS
SELECT
  TRIM(supplier_id) AS supplier_id,
  TRIM(supplier_name) AS supplier_name,
  TRIM(tier) AS tier,
  SAFE_CAST(contract_lead_time_days AS INT64) AS contract_lead_time_days
FROM `driiiportfolio.nordstrom_supply_chain.raw_suppliers`;

CREATE OR REPLACE TABLE `driiiportfolio.nordstrom_supply_chain.stg_inbound_shipments` AS
SELECT
  TRIM(shipment_id) AS shipment_id,
  TRIM(supplier_id) AS supplier_id,
  TRIM(po_number) AS po_number,
  SAFE_CAST(shipped_date AS DATE) AS shipped_date,
  SAFE_CAST(expected_delivery_date AS DATE) AS expected_delivery_date,
  SAFE_CAST(actual_delivery_date AS DATE) AS actual_delivery_date,
  SAFE_CAST(lead_time_variance_days AS INT64) AS lead_time_variance_days,
  COALESCE(TRIM(compliance_status), 'None') AS compliance_status,
  GREATEST(SAFE_CAST(units_shipped AS INT64), 0) AS units_shipped,
  GREATEST(SAFE_CAST(units_received AS INT64), 0) AS units_received,
  SAFE_DIVIDE(SAFE_CAST(units_received AS FLOAT64), SAFE_CAST(units_shipped AS FLOAT64)) AS shipment_fill_rate
FROM `driiiportfolio.nordstrom_supply_chain.raw_inbound_shipments`
WHERE shipment_id IS NOT NULL;

CREATE OR REPLACE TABLE `driiiportfolio.nordstrom_supply_chain.stg_store_replenishment` AS
SELECT
  TRIM(replenishment_id) AS replenishment_id,
  TRIM(store_id) AS store_id,
  TRIM(sku_id) AS sku_id,
  TRIM(shipment_id) AS shipment_id,
  SAFE_CAST(order_date AS DATE) AS order_date,
  GREATEST(SAFE_CAST(requested_units AS INT64), 0) AS requested_units,
  GREATEST(SAFE_CAST(allocated_units AS INT64), 0) AS allocated_units,
  COALESCE(TRIM(fulfillment_status), 'Unknown') AS fulfillment_status,
  SAFE_DIVIDE(SAFE_CAST(allocated_units AS FLOAT64), SAFE_CAST(requested_units AS FLOAT64)) AS rp_fill_rate
FROM `driiiportfolio.nordstrom_supply_chain.raw_store_replenishment`
WHERE replenishment_id IS NOT NULL; 
