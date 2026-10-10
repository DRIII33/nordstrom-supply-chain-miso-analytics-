from google.colab import auth
from google.cloud import bigquery
import pandas as pd
import numpy as np
from scipy import stats

# 1. Authenticate with Google Cloud inside Colab
print("Authenticating user...")
auth.authenticate_user()

# 2. Initialize BigQuery Client using your Project ID
project_id = 'driiiportfolio'
print(f"Connecting to Google BigQuery project: {project_id}...")
client = bigquery.Client(project=project_id)

# 3. Write SQL query to pull the modeled data directly from the fact table
query = """
    SELECT
        tier,
        lead_time_variance_days
    FROM
        `driiiportfolio.nordstrom_supply_chain.fact_inventory_flow`
    WHERE
        tier IS NOT NULL
        AND lead_time_variance_days IS NOT NULL
"""

# Execute query and load results directly into a Pandas DataFrame
analysis_df = client.query(query).to_dataframe()
print(f"Successfully loaded {len(analysis_df):,} rows from BigQuery.")

# 4. Output descriptive summary statistics by supplier tier
print("\n--- Descriptive Statistics by Supplier Tier (BigQuery Source) ---")
tier_summary = analysis_df.groupby('tier')['lead_time_variance_days'].agg(
    count='count',
    mean_variance='mean',
    std_variance='std',
    median_variance='median'
).round(2)
print(tier_summary)

# 5. Prepare data groups dynamically for One-Way ANOVA
tier_groups = [group['lead_time_variance_days'].values for name, group in analysis_df.groupby('tier')]

# 6. Execute One-Way ANOVA testing lead time variance across tiers
f_stat, p_val = stats.f_oneway(*tier_groups)

print("\n--- Inferential Statistics: One-Way ANOVA ---")
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value:     {p_val:.4e}")

# 7. Hypothesis Evaluation (Alpha = 0.05)
alpha = 0.05
print("\n--- Hypothesis Test Conclusion ---")
if p_val <= alpha:
    print(f"Result: Reject the Null Hypothesis (p = {p_val:.4e} <= {alpha}).")
    print("Conclusion: There is a statistically significant difference in lead time variance across supplier tiers.")
else:
    print(f"Result: Fail to Reject the Null Hypothesis (p = {p_val:.4e} > {alpha}).")
    print("Conclusion: No statistically significant difference in lead time variance across supplier tiers was detected.")
