#!/usr/bin/env python3
"""
Create visualizations for retention analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

OUTPUT_DIR = '/home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/retention-analysis'

print("Creating visualizations...")
print("=" * 80)

# Load necessary data
retention_matrix = pd.read_csv(f'{OUTPUT_DIR}/cohort_retention_matrix.csv', index_col=0)
customer_orders = pd.read_csv(f'{OUTPUT_DIR}/customer_lifecycle.csv')
dormancy_segments = pd.read_csv(f'{OUTPUT_DIR}/dormancy_segments.csv')

# Calculate days since last purchase for visualizations
analysis_date = pd.to_datetime(customer_orders['last_purchase_date']).max()
customer_orders['days_since_last_purchase'] = (analysis_date - pd.to_datetime(customer_orders['last_purchase_date'])).dt.days

# ============================================================================
# VISUALIZATION 1: Cohort Retention Heatmap
# ============================================================================
print("1. Creating cohort retention heatmap...")

fig, ax = plt.subplots(figsize=(16, 10))

# Prepare data for heatmap (limit to first 12 months for readability)
heatmap_data = retention_matrix.iloc[:, :min(12, retention_matrix.shape[1])]

# Create heatmap
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn',
            vmin=0, vmax=100, linewidths=0.5, ax=ax, cbar_kws={'label': 'Retention Rate (%)'})

ax.set_title('Cohort Retention Analysis - Monthly Cohorts\n(% of customers who made another purchase)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Months Since First Purchase', fontsize=12, fontweight='bold')
ax.set_ylabel('Cohort Month', fontsize=12, fontweight='bold')

# Format y-axis labels
y_labels = [str(idx) for idx in heatmap_data.index]
ax.set_yticklabels(y_labels, rotation=0)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/cohort_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("   Saved: cohort_heatmap.png")

# ============================================================================
# VISUALIZATION 2: Retention Curve
# ============================================================================
print("2. Creating retention curve...")

fig, ax = plt.subplots(figsize=(12, 7))

# Calculate overall retention rate by period
overall_retention = retention_matrix.mean(axis=0)
periods = range(len(overall_retention))

ax.plot(periods, overall_retention, marker='o', linewidth=2, markersize=8,
        color='#e74c3c', label='Average Retention Rate', zorder=3)

# Add industry benchmark (typical e-commerce: starts at 100%, drops to 20-30% by month 6)
max_periods = len(periods)
industry_benchmark = [100] + [max(20, 100 - (i * 12)) for i in range(1, max_periods)]
industry_benchmark = industry_benchmark[:max_periods]
ax.plot(periods, industry_benchmark, linestyle='--', linewidth=2,
        color='#3498db', label='Industry Benchmark', alpha=0.7, zorder=2)

ax.set_title('Customer Retention Curve Over Time', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Months Since First Purchase', fontsize=12, fontweight='bold')
ax.set_ylabel('Retention Rate (%)', fontsize=12, fontweight='bold')
ax.legend(fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3, zorder=1)
ax.set_ylim(0, 105)

# Add text annotation for Olist vs Industry gap
if len(overall_retention) >= 6:
    olist_6m = overall_retention.iloc[min(6, len(overall_retention)-1)]
    industry_6m = industry_benchmark[min(6, len(industry_benchmark)-1)]
    gap = industry_6m - olist_6m
    ax.annotate(f'Gap at 6 months:\n{gap:.1f}%',
                xy=(min(6, len(overall_retention)-1), (olist_6m + industry_6m)/2),
                xytext=(10, 50), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/retention_curve.png', dpi=300, bbox_inches='tight')
plt.close()
print("   Saved: retention_curve.png")

# ============================================================================
# VISUALIZATION 3: Churn Distribution
# ============================================================================
print("3. Creating churn distribution...")

fig, ax = plt.subplots(figsize=(12, 7))

churn_threshold = 180
bins = [0, 30, 60, 90, 180, 365, 730, customer_orders['days_since_last_purchase'].max() + 1]
counts, edges, patches = ax.hist(customer_orders['days_since_last_purchase'],
                                bins=bins, edgecolor='black', linewidth=1.2)

# Color bars based on churn threshold
colors_bars = ['#27ae60' if edge < churn_threshold else '#e74c3c' for edge in edges[:-1]]
for patch, color in zip(patches, colors_bars):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.axvline(x=churn_threshold, color='red', linestyle='--', linewidth=2,
          label=f'Churn Threshold ({churn_threshold} days)', zorder=3)

ax.set_title('Customer Dormancy Distribution\n(Days Since Last Purchase)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Days Since Last Purchase', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y', zorder=1)

# Add value labels on bars
for i, count in enumerate(counts):
    if count > 0:
        ax.text(edges[i] + (edges[i+1] - edges[i])/2, count + max(counts)*0.02, f'{int(count):,}',
               ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/churn_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   Saved: churn_distribution.png")

# ============================================================================
# VISUALIZATION 4: Dormancy Analysis
# ============================================================================
print("4. Creating dormancy analysis...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Subplot 1: Customer count by dormancy segment
dormancy_counts = dormancy_segments.set_index('dormancy_segment')['customer_count']
colors_dormancy = ['#27ae60', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b', '#7f8c8d']
colors_dormancy = colors_dormancy[:len(dormancy_counts)]

bars1 = ax1.bar(range(len(dormancy_counts)), dormancy_counts, color=colors_dormancy,
               edgecolor='black', linewidth=1.2, alpha=0.8)

ax1.set_title('Customers by Dormancy Segment', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Dormancy Segment', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Customers', fontsize=11, fontweight='bold')
ax1.set_xticks(range(len(dormancy_counts)))
ax1.set_xticklabels(dormancy_counts.index, rotation=45, ha='right')
ax1.grid(True, alpha=0.3, axis='y', zorder=1)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + max(dormancy_counts)*0.02,
            f'{int(height):,}', ha='center', va='bottom', fontweight='bold')

# Subplot 2: Revenue by dormancy segment
dormancy_revenue = dormancy_segments.set_index('dormancy_segment')['total_revenue']
bars2 = ax2.bar(range(len(dormancy_revenue)), dormancy_revenue, color=colors_dormancy,
               edgecolor='black', linewidth=1.2, alpha=0.8)

ax2.set_title('Total Revenue by Dormancy Segment', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Dormancy Segment', fontsize=11, fontweight='bold')
ax2.set_ylabel('Total Revenue ($)', fontsize=11, fontweight='bold')
ax2.set_xticks(range(len(dormancy_revenue)))
ax2.set_xticklabels(dormancy_revenue.index, rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y', zorder=1)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    if height >= 1000:
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(dormancy_revenue)*0.02,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
    else:
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(dormancy_revenue)*0.02,
                f'${height:.0f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dormancy_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("   Saved: dormancy_analysis.png")

# ============================================================================
# VISUALIZATION 5: Survival Curves by Segment
# ============================================================================
print("5. Creating survival curves...")

# Create RFM segments
customer_orders_sorted = customer_orders.copy()
customer_orders_sorted['recency_rank'] = customer_orders_sorted['days_since_last_purchase'].rank(ascending=True)
customer_orders_sorted['frequency_rank'] = customer_orders_sorted['order_count'].rank(ascending=False)
customer_orders_sorted['monetary_rank'] = customer_orders_sorted['total_spent'].rank(ascending=False)

# Calculate RFM scores
customer_orders_sorted['R_score'] = pd.qcut(customer_orders_sorted['days_since_last_purchase'], 
                                            5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
customer_orders_sorted['F_score'] = pd.qcut(customer_orders_sorted['order_count'].rank(method='first'), 
                                            5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
customer_orders_sorted['M_score'] = pd.qcut(customer_orders_sorted['total_spent'].rank(method='first'), 
                                            5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
customer_orders_sorted['RFM_score'] = (customer_orders_sorted['R_score'] + 
                                       customer_orders_sorted['F_score'] + 
                                       customer_orders_sorted['M_score'])

def segment_customer(rfm_score):
    if rfm_score >= 12:
        return 'Champions'
    elif rfm_score >= 9:
        return 'Loyal'
    elif rfm_score >= 6:
        return 'At Risk'
    else:
        return 'Lost'

customer_orders_sorted['segment'] = customer_orders_sorted['RFM_score'].apply(segment_customer)

# Calculate survival rates
survival_data = []
for segment in customer_orders_sorted['segment'].unique():
    segment_customers = customer_orders_sorted[customer_orders_sorted['segment'] == segment]
    
    for days in range(0, 731, 30):
        active = len(segment_customers[segment_customers['days_since_last_purchase'] <= days])
        total = len(segment_customers)
        survival_rate = (active / total) * 100 if total > 0 else 0
        
        survival_data.append({
            'segment': segment,
            'days': days,
            'survival_rate': survival_rate
        })

survival_df = pd.DataFrame(survival_data)

fig, ax = plt.subplots(figsize=(12, 7))

colors = {'Champions': '#27ae60', 'Loyal': '#3498db', 'At Risk': '#f39c12', 'Lost': '#e74c3c'}

for segment in ['Champions', 'Loyal', 'At Risk', 'Lost']:
    if segment in survival_df['segment'].values:
        segment_data = survival_df[survival_df['segment'] == segment]
        ax.plot(segment_data['days'], segment_data['survival_rate'],
                marker='o', linewidth=2, label=segment, color=colors.get(segment, '#95a5a6'))

ax.set_title('Customer Survival Analysis by Segment\n(% of customers still active)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Days Since First Purchase', fontsize=12, fontweight='bold')
ax.set_ylabel('Survival Rate (%)', fontsize=12, fontweight='bold')
ax.legend(title='Customer Segment', fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/survival_curves.png', dpi=300, bbox_inches='tight')
plt.close()
print("   Saved: survival_curves.png")

print()
print("=" * 80)
print("All visualizations created successfully!")
print("=" * 80)
