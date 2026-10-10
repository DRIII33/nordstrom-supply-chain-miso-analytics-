import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_suppliers = 50
n_shipments = 5000
n_replenishments = 10000

# 1. Suppliers Dataset
supplier_ids = [f"SUPP_{i:03d}" for i in range(1, n_suppliers + 1)]
tiers = ['Tier 1', 'Tier 2', 'Tier 3']
suppliers_df = pd.DataFrame({
    'supplier_id': supplier_ids,
    'supplier_name': [f"Nordstrom Vendor Partner {i}" for i in range(1, n_suppliers + 1)],
    'tier': np.random.choice(tiers, n_suppliers, p=[0.25, 0.50, 0.25]),
    'contract_lead_time_days': np.random.randint(5, 21, n_suppliers)
})

# 2. Inbound Shipments Dataset
start_date = datetime(2025, 1, 1)
shipment_dates = [start_date + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_shipments)]

shipments_df = pd.DataFrame({
    'shipment_id': [f"SHP_{i:05d}" for i in range(1, n_shipments + 1)],
    'supplier_id': np.random.choice(supplier_ids, n_shipments),
    'po_number': [f"PO_{np.random.randint(10000, 99999)}" for _ in range(n_shipments)],
    'shipped_date': shipment_dates,
})

def simulate_delivery(row, sup_df):
    sup_info = sup_df[sup_df['supplier_id'] == row['supplier_id']].iloc[0]
    contract_lt = sup_info['contract_lead_time_days']
    actual_lt = contract_lt + np.random.choice([0, 1, 2, 3, 5, -1, 10], p=[0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05])
    actual_delivery = row['shipped_date'] + timedelta(days=int(actual_lt))
    expected_delivery = row['shoped_date'] if 'shoped_date' in row else row['shipped_date'] + timedelta(days=int(contract_lt))
    
    is_late = actual_delivery > expected_delivery
    compliance_issue = 'None'
    if is_late:
        compliance_issue = 'Late Delivery'
    elif np.random.rand() < 0.12:
        compliance_issue = 'Incorrect Ticketing / ASN Failure'
        
    return pd.Series({
        'expected_delivery_date': expected_delivery,
        'actual_delivery_date': actual_delivery,
        'lead_time_variance_days': actual_lt - contract_lt,
        'compliance_status': compliance_issue,
        'units_shipped': int(np.random.randint(500, 5000)),
        'units_received': int(np.random.randint(450, 5000))
    })

shipments_df = pd.concat([shipments_df, shipments_df.apply(lambda r: simulate_delivery(r, suppliers_df), axis=1)], axis=1)

# 3. Store Replenishment (RP) Dataset (CORRECTED & ADDED)
store_ids = [f"STORE_{i:03d}" for i in range(1, 26)] # 25 retail locations
sku_ids = [f"SKU_{i:04d}" for i in range(1, 201)] # 200 SKUs

replenishment_df = pd.DataFrame({
    'replenishment_id': [f"RP_{i:06d}" for i in range(1, n_replenishments + 1)],
    'store_id': np.random.choice(store_ids, n_replenishments),
    'sku_id': np.random.choice(sku_ids, n_replenishments),
    'shipment_id': np.random.choice(shipments_df['shipment_id'], n_replenishments),
    'order_date': [start_date + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_replenishments)],
    'requested_units': np.random.randint(20, 300, n_replenishments),
})

def simulate_fulfillment(row):
    allocated = int(row['requested_units'] * np.random.choice([1.0, 0.9, 0.75, 0.5], p=[0.7, 0.15, 0.1, 0.05]))
    status = 'Fully Fulfilled' if allocated == row['requested_units'] else 'Partially Fulfilled'
    if allocated == 0:
        status = 'Stockout'
    return pd.Series({
        'allocated_units': allocated,
        'fulfillment_status': status
    })

replenishment_df = pd.concat([replenishment_df, replenishment_df.apply(simulate_fulfillment, axis=1)], axis=1)

# Export all three datasets to CSV
suppliers_df.to_csv('raw_suppliers.csv', index=False)
shipments_df.to_csv('raw_inbound_shipments.csv', index=False)
replenishment_df.to_csv('raw_store_replenishment.csv', index=False)

print("All 3 relational datasets (suppliers, shipments, replenishment) generated successfully.")
