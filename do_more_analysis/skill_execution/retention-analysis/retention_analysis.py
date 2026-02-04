#!/usr/bin/env python3
"""
Comprehensive Retention Analysis for Olist E-commerce Dataset
Focus: Understanding 0% repeat purchase rate and customer lifecycle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# File paths
DATA_DIR = '/home/user/claude-data-analysis-ultra-main/data_storage'
OUTPUT_DIR = '/home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/retention-analysis'

print("=" * 80)
print("OLIST E-COMMERCE RETENTION ANALYSIS")
print("=" * 80)
print()

# ============================================================================
# STEP 1: DATA LOADING AND PREPARATION
# ============================================================================
print("STEP 1: Loading and preparing data...")
print("-" * 80)

# Load datasets
orders_df = pd.read_csv(f'{DATA_DIR}/Orders.csv')
customers_df = pd.read_csv(f'{DATA_DIR}/Customers.csv')
order_items_df = pd.read_csv(f'{DATA_DIR}/Order Items.csv')

print(f"Orders loaded: {len(orders_df):,} records")
print(f"Customers loaded: {len(customers_df):,} records")
print(f"Order Items loaded: {len(order_items_df):,} records")
print()

# Convert timestamp columns to datetime
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])

# Merge orders with customers to get unique customer IDs
orders_customers = orders_df.merge(customers_df, on='customer_id', how='left')

# Calculate order value from order items
order_values = order_items_df.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum'
}).reset_index()
order_values['total_value'] = order_values['price'] + order_values['freight_value']

# Merge order values
orders_customers = orders_customers.merge(order_values[['order_id', 'total_value']],
                                          on='order_id', how='left')

print(f"Combined dataset: {len(orders_customers):,} records")
print(f"Date range: {orders_customers['order_purchase_timestamp'].min()} to {orders_customers['order_purchase_timestamp'].max()}")
print()

# ============================================================================
# STEP 2: REPEAT PURCHASE ANALYSIS
# ============================================================================
print("STEP 2: Analyzing repeat purchase behavior...")
print("-" * 80)

# Group by unique customer ID and count orders
customer_orders = orders_customers.groupby('customer_unique_id').agg({
    'order_id': 'count',
    'order_purchase_timestamp': ['min', 'max'],
    'total_value': 'sum',
    'customer_state': 'first',
    'customer_city': 'first'
}).reset_index()

customer_orders.columns = ['customer_unique_id', 'order_count', 'first_purchase_date',
                          'last_purchase_date', 'total_spent', 'state', 'city']

# Calculate repeat purchase metrics
total_customers = len(customer_orders)
repeat_customers = len(customer_orders[customer_orders['order_count'] > 1])
one_time_customers = len(customer_orders[customer_orders['order_count'] == 1])
repeat_rate = (repeat_customers / total_customers) * 100

print(f"Total Unique Customers: {total_customers:,}")
print(f"One-time Buyers: {one_time_customers:,} ({(one_time_customers/total_customers)*100:.2f}%)")
print(f"Repeat Customers: {repeat_customers:,} ({repeat_rate:.2f}%)")
print()

if repeat_customers > 0:
    print("Order Count Distribution for Repeat Customers:")
    repeat_dist = customer_orders[customer_orders['order_count'] > 1]['order_count'].value_counts().sort_index()
    for orders, count in repeat_dist.items():
        print(f"  {orders} orders: {count:,} customers")
    print()

# Save repeat customer details
if repeat_customers > 0:
    repeat_customer_details = customer_orders[customer_orders['order_count'] > 1].copy()
    repeat_customer_details = repeat_customer_details.sort_values('order_count', ascending=False)
    repeat_customer_details.to_csv(f'{OUTPUT_DIR}/repeat_customers_detailed.csv', index=False)
    print(f"Saved: repeat_customers_detailed.csv ({len(repeat_customer_details)} repeat customers)")
    print()

# ============================================================================
# STEP 3: COHORT ANALYSIS
# ============================================================================
print("STEP 3: Performing cohort analysis...")
print("-" * 80)

# Prepare cohort data
orders_cohort = orders_customers[['customer_unique_id', 'order_purchase_timestamp']].copy()
orders_cohort['order_month'] = orders_cohort['order_purchase_timestamp'].dt.to_period('M')

# Get first purchase month for each customer (cohort)
customer_cohort = orders_cohort.groupby('customer_unique_id')['order_month'].min().reset_index()
customer_cohort.columns = ['customer_unique_id', 'cohort_month']

# Merge cohort information back to orders
orders_cohort = orders_cohort.merge(customer_cohort, on='customer_unique_id')

# Calculate periods since cohort
orders_cohort['periods'] = (orders_cohort['order_month'] - orders_cohort['cohort_month']).apply(lambda x: x.n)

# Create cohort matrix
cohort_data = orders_cohort.groupby(['cohort_month', 'periods'])['customer_unique_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='periods', values='customer_unique_id')

# Calculate retention rates
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100

print(f"Cohorts created: {len(cohort_pivot)} monthly cohorts")
print(f"Cohort date range: {cohort_pivot.index.min()} to {cohort_pivot.index.max()}")
print()
print("Sample Retention Matrix (first 5 cohorts, first 6 months):")
print(retention_matrix.iloc[:5, :6].round(2))
print()

# Save cohort retention matrix
retention_matrix.to_csv(f'{OUTPUT_DIR}/cohort_retention_matrix.csv')
print(f"Saved: cohort_retention_matrix.csv")
print()

# ============================================================================
# STEP 4: CHURN ANALYSIS
# ============================================================================
print("STEP 4: Analyzing churn patterns...")
print("-" * 80)

# Calculate days since last purchase for each customer
analysis_date = orders_customers['order_purchase_timestamp'].max()
customer_orders['days_since_last_purchase'] = (analysis_date - customer_orders['last_purchase_date']).dt.days

# Calculate customer lifespan (for repeat customers)
customer_orders['customer_lifespan_days'] = (customer_orders['last_purchase_date'] -
                                             customer_orders['first_purchase_date']).dt.days

# Define churn threshold (industry standard: 90-180 days)
churn_threshold = 180
customer_orders['is_churned'] = customer_orders['days_since_last_purchase'] > churn_threshold

churned_customers = customer_orders['is_churned'].sum()
churn_rate = (churned_customers / total_customers) * 100

print(f"Churn threshold: {churn_threshold} days")
print(f"Churned customers: {churned_customers:,} ({churn_rate:.2f}%)")
print(f"Active customers: {total_customers - churned_customers:,} ({100-churn_rate:.2f}%)")
print()

# Time-to-churn analysis (using days since last purchase as proxy)
churn_bins = [0, 30, 60, 90, 180, 365, 730, float('inf')]
churn_labels = ['0-30 days', '31-60 days', '61-90 days', '91-180 days',
                '181-365 days', '366-730 days', '730+ days']
customer_orders['dormancy_segment'] = pd.cut(customer_orders['days_since_last_purchase'],
                                             bins=churn_bins, labels=churn_labels)

dormancy_dist = customer_orders['dormancy_segment'].value_counts().sort_index()
print("Customer Dormancy Distribution:")
for segment, count in dormancy_dist.items():
    pct = (count / total_customers) * 100
    print(f"  {segment}: {count:,} customers ({pct:.2f}%)")
print()

# Churn analysis by segment
churn_analysis = customer_orders.groupby('dormancy_segment').agg({
    'customer_unique_id': 'count',
    'total_spent': 'mean',
    'order_count': 'mean',
    'customer_lifespan_days': 'mean'
}).reset_index()
churn_analysis.columns = ['dormancy_segment', 'customer_count', 'avg_spent',
                         'avg_orders', 'avg_lifespan_days']

churn_analysis.to_csv(f'{OUTPUT_DIR}/churn_analysis.csv', index=False)
print(f"Saved: churn_analysis.csv")
print()

# ============================================================================
# STEP 5: CUSTOMER LIFECYCLE ANALYSIS
# ============================================================================
print("STEP 5: Analyzing customer lifecycle...")
print("-" * 80)

# Customer lifecycle metrics
lifecycle_metrics = {
    'avg_customer_lifespan_days': customer_orders['customer_lifespan_days'].mean(),
    'median_customer_lifespan_days': customer_orders['customer_lifespan_days'].median(),
    'avg_days_since_last_purchase': customer_orders['days_since_last_purchase'].mean(),
    'median_days_since_last_purchase': customer_orders['days_since_last_purchase'].median(),
    'avg_orders_per_customer': customer_orders['order_count'].mean(),
    'avg_revenue_per_customer': customer_orders['total_spent'].mean()
}

print("Customer Lifecycle Metrics:")
for metric, value in lifecycle_metrics.items():
    print(f"  {metric}: {value:.2f}")
print()

# Save customer lifecycle data
customer_lifecycle = customer_orders[['customer_unique_id', 'order_count', 'first_purchase_date',
                                      'last_purchase_date', 'customer_lifespan_days',
                                      'days_since_last_purchase', 'total_spent', 'state', 'city']]
customer_lifecycle.to_csv(f'{OUTPUT_DIR}/customer_lifecycle.csv', index=False)
print(f"Saved: customer_lifecycle.csv")
print()

# Dormancy segments
dormancy_segments = customer_orders.groupby('dormancy_segment').agg({
    'customer_unique_id': 'count',
    'total_spent': ['sum', 'mean'],
    'order_count': 'mean'
}).reset_index()
dormancy_segments.columns = ['dormancy_segment', 'customer_count', 'total_revenue',
                             'avg_revenue_per_customer', 'avg_orders']
dormancy_segments.to_csv(f'{OUTPUT_DIR}/dormancy_segments.csv', index=False)
print(f"Saved: dormancy_segments.csv")
print()

# ============================================================================
# STEP 6: SURVIVAL ANALYSIS
# ============================================================================
print("STEP 6: Performing survival analysis...")
print("-" * 80)

# Create RFM segments for survival analysis
rfm_data = customer_orders.copy()
rfm_data['recency'] = rfm_data['days_since_last_purchase']
rfm_data['frequency'] = rfm_data['order_count']
rfm_data['monetary'] = rfm_data['total_spent']

# Rank customers
rfm_data['recency_rank'] = rfm_data['recency'].rank(ascending=True)
rfm_data['frequency_rank'] = rfm_data['frequency'].rank(ascending=False)
rfm_data['monetary_rank'] = rfm_data['monetary'].rank(ascending=False)

# Calculate RFM scores (quintiles)
rfm_data['R_score'] = pd.qcut(rfm_data['recency'], 5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
rfm_data['F_score'] = pd.qcut(rfm_data['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
rfm_data['M_score'] = pd.qcut(rfm_data['monetary'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
rfm_data['RFM_score'] = rfm_data['R_score'] + rfm_data['F_score'] + rfm_data['M_score']

# Segment customers
def segment_customer(rfm_score):
    if rfm_score >= 12:
        return 'Champions'
    elif rfm_score >= 9:
        return 'Loyal'
    elif rfm_score >= 6:
        return 'At Risk'
    else:
        return 'Lost'

rfm_data['segment'] = rfm_data['RFM_score'].apply(segment_customer)

print("Customer Segments (RFM-based):")
segment_dist = rfm_data['segment'].value_counts()
for segment, count in segment_dist.items():
    pct = (count / total_customers) * 100
    print(f"  {segment}: {count:,} customers ({pct:.2f}%)")
print()

# Survival analysis by segment
survival_data = []

for segment in rfm_data['segment'].unique():
    segment_customers = rfm_data[rfm_data['segment'] == segment]

    # Create survival curve (percentage of customers still active over time)
    for days in range(0, 731, 30):  # 0 to 730 days, 30-day intervals
        active = len(segment_customers[segment_customers['days_since_last_purchase'] <= days])
        total = len(segment_customers)
        survival_rate = (active / total) * 100 if total > 0 else 0

        survival_data.append({
            'segment': segment,
            'days': days,
            'survival_rate': survival_rate,
            'active_customers': active,
            'total_customers': total
        })

survival_df = pd.DataFrame(survival_data)

print("Sample Survival Rates (at 180 days):")
survival_180 = survival_df[survival_df['days'] == 180]
for _, row in survival_180.iterrows():
    print(f"  {row['segment']}: {row['survival_rate']:.2f}%")
print()

# ============================================================================
# STEP 7: RETENTION METRICS SUMMARY
# ============================================================================
print("STEP 7: Generating retention metrics summary...")
print("-" * 80)

retention_metrics = {
    'analysis_date': analysis_date.strftime('%Y-%m-%d'),
    'total_unique_customers': int(total_customers),
    'one_time_customers': int(one_time_customers),
    'repeat_customers': int(repeat_customers),
    'repeat_purchase_rate': float(round(repeat_rate, 2)),
    'churn_rate': float(round(churn_rate, 2)),
    'avg_customer_lifespan_days': float(round(lifecycle_metrics['avg_customer_lifespan_days'], 2)),
    'median_customer_lifespan_days': float(round(lifecycle_metrics['median_customer_lifespan_days'], 2)),
    'avg_days_since_last_purchase': float(round(lifecycle_metrics['avg_days_since_last_purchase'], 2)),
    'avg_orders_per_customer': float(round(lifecycle_metrics['avg_orders_per_customer'], 2)),
    'avg_revenue_per_customer': float(round(lifecycle_metrics['avg_revenue_per_customer'], 2)),
    'cohort_count': int(len(cohort_pivot)),
    'date_range_start': orders_customers['order_purchase_timestamp'].min().strftime('%Y-%m-%d'),
    'date_range_end': orders_customers['order_purchase_timestamp'].max().strftime('%Y-%m-%d'),
    'segment_distribution': {
        segment: int(count) for segment, count in segment_dist.items()
    },
    'dormancy_distribution': {
        str(segment): int(count) for segment, count in dormancy_dist.items()
    }
}

with open(f'{OUTPUT_DIR}/retention_metrics.json', 'w') as f:
    json.dump(retention_metrics, f, indent=2)

print("Retention Metrics Summary saved to retention_metrics.json")
print()

print("=" * 80)
print("Analysis complete! Proceeding to visualizations...")
print("=" * 80)
