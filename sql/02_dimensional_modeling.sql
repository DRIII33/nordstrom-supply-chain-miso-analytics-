CREATE OR REPLACE TABLE `driiiportfolio.nordstrom_supply_chain.fact_inventory_flow` AS
SELECT
  r.replenishment_id,
  r.store_id,
  r.sku_id,
  sup.supplier_id,
  sup.supplier_name,
  sup.tier,
  r.order_date,
  i.actual_delivery_date,
  r.requested_units,
  r.allocated_units,
  r.fulfillment_status,  -- [ADDED] Explicitly included from stg_store_replenishment
  r.rp_fill_rate,
  i.lead_time_variance_days,
  i.compliance_status,
  CASE WHEN i.compliance_status != 'None' THEN 1 ELSE 0 END AS has_compliance_infraction
FROM `driiiportfolio.nordstrom_supply_chain.stg_store_replenishment` r
LEFT JOIN `driiiportfolio.nordstrom_supply_chain.stg_inbound_shipments` i
  ON r.shipment_id = i.shipment_id
LEFT JOIN `driiiportfolio.nordstrom_supply_chain.stg_suppliers` sup
  ON i.supplier_id = sup.supplier_id;
