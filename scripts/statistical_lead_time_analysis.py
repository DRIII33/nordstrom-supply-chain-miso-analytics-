from google.cloud import bigquery
import pandas as pd
import scipy.stats as stats

# 1. Initialize BigQuery Client
project_id = 'driiiportfolio'
print(f"Connecting to Google BigQuery project: {project_id}...")
client = bigquery.Client(project=project_id)

# 2. Extract compliance and fulfillment data from the modeled fact table
query = """
    SELECT
        compliance_status,
        fulfillment_status,
        store_id,
        tier
    FROM
        `driiiportfolio.nordstrom_supply_chain.fact_inventory_flow`
    WHERE
        compliance_status IS NOT NULL
        AND fulfillment_status IS NOT NULL
"""

df = client.query(query).to_dataframe()
print(f"Successfully loaded {len(df):,} rows for compliance and fulfillment analysis.")

# 3. Build a Contingency Table: Compliance Status vs. Fulfillment Status
print("\n--- Contingency Table: Compliance Infractions vs. Fulfillment Status ---")
contingency_table = pd.crosstab(df['compliance_status'], df['fulfillment_status'])
print(contingency_table)

# 4. Execute Chi-Square Test of Independence
chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)

print("\n--- Inferential Statistics: Chi-Square Test of Independence ---")
print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"Degrees of Freedom:   {dof}")
print(f"p-value:              {p_val:.4e}")

# 5. Hypothesis Evaluation (Alpha = 0.05)
alpha = 0.05
print("\n--- Hypothesis Test Conclusion ---")
if p_val <= alpha:
    print(f"Result: Reject the Null Hypothesis (p = {p_val:.4e} <= {alpha}).")
    print("Conclusion: There is a statistically significant dependency between supplier compliance issues and store replenishment fulfillment failures.")
else:
    print(f"Result: Fail to Reject the Null Hypothesis (p = {p_val:.4e} > {alpha}).")
    print("Conclusion: No statistically significant dependency detected between compliance status and store fulfillment status.")

# 6. Regional Bottleneck Summary (Store-level Partial Fulfillment Rates)
print("\n--- Operational Insight: Top Regional Store Bottlenecks (Partial Fulfillment Rates) ---")
store_perf = df.groupby('store_id').agg(
    total_orders=('fulfillment_status', 'count'),
    partial_fulfillments=('fulfillment_status', lambda x: (x == 'Partially Fulfilled').sum())
).reset_index()

store_perf['partial_fulfillment_rate_%'] = (store_perf['partial_fulfillments'] / store_perf['total_orders']) * 100
print(store_perf.sort_values(by='partial_fulfillment_rate_%', ascending=False).head(5))
