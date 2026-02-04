"""
RFM Customer Segmentation Analysis for Olist E-commerce Dataset
Analyzes customer behavior using Recency, Frequency, and Monetary metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
output_dir = '/home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/rfm-customer-segmentation'
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("RFM CUSTOMER SEGMENTATION ANALYSIS")
print("=" * 80)
print("\nLoading datasets...")

# Load datasets
orders = pd.read_csv('/home/user/claude-data-analysis-ultra-main/data_storage/Orders.csv')
order_items = pd.read_csv('/home/user/claude-data-analysis-ultra-main/data_storage/Order Items.csv')
customers = pd.read_csv('/home/user/claude-data-analysis-ultra-main/data_storage/Customers.csv')

print(f"✓ Orders: {len(orders):,} records")
print(f"✓ Order Items: {len(order_items):,} records")
print(f"✓ Customers: {len(customers):,} records")

# Data preprocessing
print("\n" + "=" * 80)
print("DATA PREPROCESSING")
print("=" * 80)

# Convert timestamp to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Filter only delivered orders
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()
print(f"\n✓ Delivered orders: {len(orders_delivered):,} ({len(orders_delivered)/len(orders)*100:.1f}%)")

# Merge order items with orders to get prices
order_data = orders_delivered.merge(order_items, on='order_id', how='left')
print(f"✓ Merged order data: {len(order_data):,} records")

# Calculate total price (price + freight)
order_data['total_price'] = order_data['price'] + order_data['freight_value']

# Get analysis date (most recent order date)
analysis_date = orders_delivered['order_purchase_timestamp'].max()
print(f"\n✓ Analysis date (most recent order): {analysis_date.strftime('%Y-%m-%d')}")

# RFM CALCULATION
print("\n" + "=" * 80)
print("RFM METRICS CALCULATION")
print("=" * 80)

# Calculate RFM metrics per customer
rfm = order_data.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id': 'nunique',  # Frequency
    'total_price': 'sum'  # Monetary
}).reset_index()

# Rename columns
rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Remove any rows with missing values
rfm = rfm.dropna()

print(f"\n✓ RFM data calculated for {len(rfm):,} customers")
print(f"\nRFM Summary Statistics:")
print(rfm[['recency', 'frequency', 'monetary']].describe())

# Calculate RFM Scores (1-5 scale, 5 being the best)
print("\n" + "=" * 80)
print("RFM SCORING (1-5 Scale)")
print("=" * 80)

# Recency score (lower recency is better, so we reverse)
rfm['r_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')

# Frequency score (higher is better)
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

# Monetary score (higher is better)
rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

# Convert to integers
rfm['r_score'] = rfm['r_score'].astype(int)
rfm['f_score'] = rfm['f_score'].astype(int)
rfm['m_score'] = rfm['m_score'].astype(int)

# Create RFM score string
rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

print(f"✓ RFM scores calculated")
print(f"\nScore Distribution:")
print(f"  R-Score: {rfm['r_score'].value_counts().sort_index()}")
print(f"  F-Score: {rfm['f_score'].value_counts().sort_index()}")
print(f"  M-Score: {rfm['m_score'].value_counts().sort_index()}")

# CUSTOMER SEGMENTATION
print("\n" + "=" * 80)
print("CUSTOMER SEGMENTATION")
print("=" * 80)

def segment_customers(df):
    """Assign customers to segments based on RFM scores"""
    segments = []

    for _, row in df.iterrows():
        r, f, m = row['r_score'], row['f_score'], row['m_score']

        # Champions: High R, F, M
        if r >= 4 and f >= 4 and m >= 4:
            segments.append('Champions')

        # Loyal Customers: High F
        elif f >= 4:
            segments.append('Loyal')

        # Potential Loyalist: Recent customers with good frequency
        elif r >= 3 and f >= 3:
            segments.append('Potential Loyalist')

        # New Customers: High recency, low frequency
        elif r >= 4 and f <= 2:
            segments.append('New Customers')

        # Promising: Recent customers, moderate spending
        elif r >= 3 and m >= 3:
            segments.append('Promising')

        # Need Attention: Moderate scores
        elif r >= 2 and f >= 2 and m >= 2:
            segments.append('Need Attention')

        # At Risk: Low recency, but previously good customers
        elif r <= 2 and f >= 3:
            segments.append('At Risk')

        # Can't Lose: Low recency, high monetary
        elif r <= 2 and m >= 4:
            segments.append("Can't Lose")

        # Hibernating: Low recency and frequency
        elif r <= 2 and f <= 2:
            segments.append('Hibernating')

        # Lost: Very low scores
        else:
            segments.append('Lost')

    return segments

rfm['rfm_segment'] = segment_customers(rfm)

# Segment statistics
segment_stats = rfm.groupby('rfm_segment').agg({
    'customer_id': 'count',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['mean', 'sum']
}).round(2)

segment_stats.columns = ['customer_count', 'avg_recency', 'avg_frequency', 'avg_monetary', 'total_revenue']
segment_stats = segment_stats.sort_values('total_revenue', ascending=False)
segment_stats['revenue_percentage'] = (segment_stats['total_revenue'] / segment_stats['total_revenue'].sum() * 100).round(2)

print(f"\n✓ Customers segmented into {rfm['rfm_segment'].nunique()} segments")
print(f"\nSegment Distribution:")
print(rfm['rfm_segment'].value_counts().sort_values(ascending=False))

print(f"\nSegment Statistics:")
print(segment_stats)

# Identify VIP Customers (Top 5% by monetary value)
print("\n" + "=" * 80)
print("VIP CUSTOMER IDENTIFICATION")
print("=" * 80)

vip_threshold = rfm['monetary'].quantile(0.95)
vip_customers = rfm[rfm['monetary'] >= vip_threshold].copy()
vip_customers = vip_customers.sort_values('monetary', ascending=False)

print(f"\n✓ VIP Threshold: ${vip_threshold:,.2f}")
print(f"✓ VIP Customers: {len(vip_customers):,} ({len(vip_customers)/len(rfm)*100:.1f}%)")
print(f"✓ VIP Total Revenue: ${vip_customers['monetary'].sum():,.2f} ({vip_customers['monetary'].sum()/rfm['monetary'].sum()*100:.1f}% of total)")

print(f"\nTop 10 VIP Customers:")
print(vip_customers[['customer_id', 'recency', 'frequency', 'monetary', 'rfm_segment']].head(10))

# SAVE OUTPUTS
print("\n" + "=" * 80)
print("SAVING OUTPUTS")
print("=" * 80)

# 1. Save RFM analysis data
rfm.to_csv(f'{output_dir}/rfm_analysis.csv', index=False)
print(f"✓ Saved: rfm_analysis.csv ({len(rfm):,} records)")

# 2. Save customer segments summary
segment_stats.to_csv(f'{output_dir}/customer_segments.csv')
print(f"✓ Saved: customer_segments.csv ({len(segment_stats)} segments)")

# 3. Save VIP customers
vip_customers.to_csv(f'{output_dir}/vip_customers.csv', index=False)
print(f"✓ Saved: vip_customers.csv ({len(vip_customers)} VIP customers)")

# 4. Save RFM summary JSON
rfm_summary = {
    'analysis_date': analysis_date.strftime('%Y-%m-%d'),
    'total_customers': int(len(rfm)),
    'total_orders': int(orders_delivered['order_id'].nunique()),
    'total_revenue': float(rfm['monetary'].sum()),
    'avg_customer_value': float(rfm['monetary'].mean()),
    'median_customer_value': float(rfm['monetary'].median()),
    'avg_order_frequency': float(rfm['frequency'].mean()),
    'avg_recency_days': float(rfm['recency'].mean()),
    'vip_customers': int(len(vip_customers)),
    'vip_revenue': float(vip_customers['monetary'].sum()),
    'vip_revenue_percentage': float(vip_customers['monetary'].sum() / rfm['monetary'].sum() * 100),
    'segments': rfm['rfm_segment'].value_counts().to_dict(),
    'segment_revenue': segment_stats['total_revenue'].to_dict()
}

with open(f'{output_dir}/rfm_summary.json', 'w') as f:
    json.dump(rfm_summary, f, indent=2)
print(f"✓ Saved: rfm_summary.json")

# VISUALIZATIONS
print("\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

# 1. Segment Distribution Bar Chart
plt.figure(figsize=(14, 8))
segment_counts = rfm['rfm_segment'].value_counts().sort_values(ascending=True)
colors = plt.cm.viridis(np.linspace(0, 1, len(segment_counts)))

plt.barh(segment_counts.index, segment_counts.values, color=colors)
plt.xlabel('Number of Customers', fontsize=12, fontweight='bold')
plt.ylabel('Customer Segment', fontsize=12, fontweight='bold')
plt.title('RFM Customer Segment Distribution\nOlist E-commerce Dataset',
          fontsize=14, fontweight='bold', pad=20)

# Add value labels
for i, v in enumerate(segment_counts.values):
    plt.text(v + 50, i, f'{v:,}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/rfm_segments_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: rfm_segments_distribution.png")
plt.close()

# 2. Monetary Distribution with VIP Threshold
plt.figure(figsize=(14, 8))
plt.hist(rfm['monetary'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(vip_threshold, color='red', linestyle='--', linewidth=2, label=f'VIP Threshold (${vip_threshold:,.0f})')
plt.xlabel('Customer Lifetime Value ($)', fontsize=12, fontweight='bold')
plt.ylabel('Number of Customers', fontsize=12, fontweight='bold')
plt.title('Customer Monetary Value Distribution\nWith VIP Threshold (Top 5%)',
          fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/monetary_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: monetary_distribution.png")
plt.close()

# 3. RFM 3D Scatter Plot (sample for performance)
from mpl_toolkits.mplot3d import Axes3D

# Sample data for visualization (too many points make it hard to see)
sample_size = min(5000, len(rfm))
rfm_sample = rfm.sample(n=sample_size, random_state=42)

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Color by segment
segments_unique = rfm_sample['rfm_segment'].unique()
colors_map = dict(zip(segments_unique, plt.cm.tab10(np.linspace(0, 1, len(segments_unique)))))

for segment in segments_unique:
    segment_data = rfm_sample[rfm_sample['rfm_segment'] == segment]
    ax.scatter(segment_data['recency'],
               segment_data['frequency'],
               segment_data['monetary'],
               c=[colors_map[segment]],
               label=segment,
               alpha=0.6,
               s=50)

ax.set_xlabel('Recency (Days)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('Frequency (Orders)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_zlabel('Monetary ($)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title(f'3D RFM Analysis\n(Sample: {sample_size:,} customers)',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=9, bbox_to_anchor=(1.05, 1))

plt.tight_layout()
plt.savefig(f'{output_dir}/rfm_3d_scatter.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: rfm_3d_scatter.png")
plt.close()

# 4. Segment Revenue Contribution
plt.figure(figsize=(14, 8))
segment_revenue = segment_stats.sort_values('total_revenue', ascending=True)
colors = plt.cm.plasma(np.linspace(0, 1, len(segment_revenue)))

plt.barh(segment_revenue.index, segment_revenue['total_revenue'], color=colors)
plt.xlabel('Total Revenue ($)', fontsize=12, fontweight='bold')
plt.ylabel('Customer Segment', fontsize=12, fontweight='bold')
plt.title('Revenue Contribution by Customer Segment\nOlist E-commerce Dataset',
          fontsize=14, fontweight='bold', pad=20)

# Add percentage labels
for i, (idx, row) in enumerate(segment_revenue.iterrows()):
    plt.text(row['total_revenue'] + 5000, i,
             f"${row['total_revenue']:,.0f} ({row['revenue_percentage']:.1f}%)",
             va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/segment_revenue_contribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: segment_revenue_contribution.png")
plt.close()

# 5. RFM Heatmap by Segment
plt.figure(figsize=(12, 8))
segment_rfm_avg = rfm.groupby('rfm_segment')[['r_score', 'f_score', 'm_score']].mean()
sns.heatmap(segment_rfm_avg, annot=True, fmt='.2f', cmap='RdYlGn',
            cbar_kws={'label': 'Score (1-5)'}, linewidths=0.5)
plt.xlabel('RFM Dimension', fontsize=12, fontweight='bold')
plt.ylabel('Customer Segment', fontsize=12, fontweight='bold')
plt.title('Average RFM Scores by Customer Segment\nHeatmap Analysis',
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{output_dir}/rfm_segment_heatmap.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: rfm_segment_heatmap.png")
plt.close()

# CREATE MARKDOWN REPORTS
print("\n" + "=" * 80)
print("GENERATING REPORTS")
print("=" * 80)

# Marketing Strategies Report
strategies_md = f"""# RFM Customer Segmentation - Marketing Strategies

**Analysis Date:** {analysis_date.strftime('%Y-%m-%d')}
**Total Customers Analyzed:** {len(rfm):,}
**Total Revenue:** ${rfm['monetary'].sum():,.2f}

---

## Customer Segment Strategies

### 1. Champions ({rfm[rfm['rfm_segment'] == 'Champions'].shape[0]:,} customers)
**Characteristics:** Recent, frequent, and high-value customers
**Revenue Contribution:** ${segment_stats.loc['Champions', 'total_revenue'] if 'Champions' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Reward with exclusive VIP programs and early access to new products
- Request testimonials and referrals
- Offer personalized premium experiences
- Create brand ambassador programs
- Send personalized thank-you messages
- Provide dedicated customer service

---

### 2. Loyal Customers ({rfm[rfm['rfm_segment'] == 'Loyal'].shape[0]:,} customers)
**Characteristics:** Frequent purchasers, moderate to high value
**Revenue Contribution:** ${segment_stats.loc['Loyal', 'total_revenue'] if 'Loyal' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Upsell higher-value products
- Introduce loyalty rewards program
- Ask for product reviews and feedback
- Offer bundle deals and cross-sell opportunities
- Send personalized product recommendations
- Create engagement campaigns

---

### 3. Potential Loyalist ({rfm[rfm['rfm_segment'] == 'Potential Loyalist'].shape[0]:,} customers)
**Characteristics:** Recent customers with good engagement potential
**Revenue Contribution:** ${segment_stats.loc['Potential Loyalist', 'total_revenue'] if 'Potential Loyalist' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Offer membership or loyalty programs
- Recommend related products based on purchase history
- Send targeted educational content
- Provide incentives for next purchase
- Nurture with email marketing campaigns
- Offer time-limited promotions

---

### 4. New Customers ({rfm[rfm['rfm_segment'] == 'New Customers'].shape[0]:,} customers)
**Characteristics:** Recent first-time buyers
**Revenue Contribution:** ${segment_stats.loc['New Customers', 'total_revenue'] if 'New Customers' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Welcome email series with onboarding
- Provide educational content about products
- Offer first-time buyer incentives for second purchase
- Build relationship through engagement campaigns
- Request feedback on first purchase experience
- Introduce them to best-selling products

---

### 5. Promising ({rfm[rfm['rfm_segment'] == 'Promising'].shape[0]:,} customers)
**Characteristics:** Recent customers with moderate spending
**Revenue Contribution:** ${segment_stats.loc['Promising', 'total_revenue'] if 'Promising' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Create awareness about premium product offerings
- Offer time-sensitive deals
- Send personalized product recommendations
- Increase engagement with content marketing
- Provide excellent customer service
- Gather feedback to improve experience

---

### 6. Need Attention ({rfm[rfm['rfm_segment'] == 'Need Attention'].shape[0]:,} customers)
**Characteristics:** Moderate scores, declining engagement
**Revenue Contribution:** ${segment_stats.loc['Need Attention', 'total_revenue'] if 'Need Attention' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Re-engagement campaigns with special offers
- Send "We miss you" communications
- Provide limited-time discounts
- Survey to understand needs and preferences
- Showcase new products and improvements
- Personalized recommendations based on past purchases

---

### 7. At Risk ({rfm[rfm['rfm_segment'] == 'At Risk'].shape[0]:,} customers)
**Characteristics:** Previously good customers, declining recency
**Revenue Contribution:** ${segment_stats.loc['At Risk', 'total_revenue'] if 'At Risk' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Win-back campaigns with compelling offers
- Send personalized reactivation emails
- Offer significant discounts or incentives
- Survey to identify pain points
- Highlight improvements or new features
- Create urgency with time-limited offers

---

### 8. Can't Lose ({rfm[rfm['rfm_segment'] == "Can't Lose"].shape[0]:,} customers)
**Characteristics:** High-value customers at risk of churning
**Revenue Contribution:** ${segment_stats.loc["Can't Lose", 'total_revenue'] if "Can't Lose" in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- **PRIORITY:** Personal outreach from account managers
- Offer exclusive deals and VIP treatment
- Conduct one-on-one interviews to understand issues
- Provide dedicated support and problem resolution
- Create customized retention offers
- Send handwritten notes or personal calls

---

### 9. Hibernating ({rfm[rfm['rfm_segment'] == 'Hibernating'].shape[0]:,} customers)
**Characteristics:** Low engagement, dormant customers
**Revenue Contribution:** ${segment_stats.loc['Hibernating', 'total_revenue'] if 'Hibernating' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Low-cost re-engagement campaigns
- Send "We've changed" messages highlighting improvements
- Offer significant comeback incentives
- A/B test different reactivation approaches
- Consider opt-in confirmations
- Showcase new product lines

---

### 10. Lost ({rfm[rfm['rfm_segment'] == 'Lost'].shape[0]:,} customers)
**Characteristics:** Very low scores, likely churned
**Revenue Contribution:** ${segment_stats.loc['Lost', 'total_revenue'] if 'Lost' in segment_stats.index else 0:,.2f}

**Marketing Strategies:**
- Minimal investment in reactivation
- Final win-back campaign with strong incentives
- Survey for churn reasons (improve for others)
- Consider removing from active marketing lists
- Focus budget on higher-potential segments
- Use for lookalike audience exclusion

---

## Priority Action Items

### Immediate Actions (Week 1)
1. **Launch VIP Program for Champions** - Retain top {len(vip_customers)} customers
2. **Re-engagement Campaign for "Can't Lose"** - High-value at-risk customers
3. **Welcome Series for New Customers** - Convert first-timers to repeat buyers

### Short-term Actions (Month 1)
4. **Loyalty Program Rollout** - Target Loyal and Potential Loyalist segments
5. **Win-back Campaign for At Risk** - Prevent further churn
6. **Cross-sell Campaign for Promising** - Increase average order value

### Medium-term Actions (Quarter 1)
7. **Customer Feedback Survey** - Understand needs across all segments
8. **Personalization Engine** - Implement AI-driven recommendations
9. **Segment-specific Content Strategy** - Tailored messaging per segment

---

## ROI Projections

**High-Priority Segments (Focus 70% of budget):**
- Champions: Retention rate target 95% → Projected revenue retention: ${segment_stats.loc['Champions', 'total_revenue'] * 0.95 if 'Champions' in segment_stats.index else 0:,.2f}
- Can't Lose: Win-back rate target 40% → Projected revenue recovery: ${segment_stats.loc["Can't Lose", 'total_revenue'] * 0.40 if "Can't Lose" in segment_stats.index else 0:,.2f}
- Loyal: Upsell target 20% → Additional revenue: ${segment_stats.loc['Loyal', 'total_revenue'] * 0.20 if 'Loyal' in segment_stats.index else 0:,.2f}

**Growth Segments (Focus 30% of budget):**
- New Customers: Conversion to repeat target 50%
- Potential Loyalist: Upgrade to Loyal target 30%
- Promising: Increase purchase frequency target 25%

---

*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

with open(f'{output_dir}/segment_strategies.md', 'w') as f:
    f.write(strategies_md)
print(f"✓ Saved: segment_strategies.md")

# Comprehensive Segmentation Report
segmentation_report = f"""# RFM Customer Segmentation Analysis Report
## Olist E-commerce Dataset

**Analysis Date:** {analysis_date.strftime('%Y-%m-%d')}
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This RFM (Recency, Frequency, Monetary) analysis segments {len(rfm):,} customers from the Olist e-commerce platform based on their purchasing behavior. The analysis identifies high-value customers, at-risk segments, and growth opportunities.

### Key Metrics
- **Total Customers:** {len(rfm):,}
- **Total Revenue:** ${rfm['monetary'].sum():,.2f}
- **Average Customer Value:** ${rfm['monetary'].mean():,.2f}
- **Median Customer Value:** ${rfm['monetary'].median():,.2f}
- **Average Order Frequency:** {rfm['frequency'].mean():.2f} orders
- **Average Recency:** {rfm['recency'].mean():.1f} days

### VIP Customers (Top 5%)
- **Count:** {len(vip_customers):,} customers ({len(vip_customers)/len(rfm)*100:.1f}%)
- **Revenue:** ${vip_customers['monetary'].sum():,.2f} ({vip_customers['monetary'].sum()/rfm['monetary'].sum()*100:.1f}% of total)
- **Minimum Spend:** ${vip_threshold:,.2f}

---

## RFM Methodology

### Recency (R)
Days since last purchase, measured from {analysis_date.strftime('%Y-%m-%d')}
- **Score 5:** Most recent purchasers (0-{rfm[rfm['r_score']==5]['recency'].max():.0f} days)
- **Score 1:** Least recent purchasers ({rfm[rfm['r_score']==1]['recency'].min():.0f}+ days)

### Frequency (F)
Total number of orders placed
- **Score 5:** Most frequent buyers ({rfm[rfm['f_score']==5]['frequency'].min():.0f}+ orders)
- **Score 1:** Least frequent buyers ({rfm[rfm['f_score']==1]['frequency'].max():.0f} order)

### Monetary (M)
Total amount spent (including shipping)
- **Score 5:** Highest spenders (${rfm[rfm['m_score']==5]['monetary'].min():,.2f}+)
- **Score 1:** Lowest spenders (up to ${rfm[rfm['m_score']==1]['monetary'].max():,.2f})

---

## Customer Segmentation Results

### Segment Overview

{segment_stats.to_markdown()}

### Segment Definitions

1. **Champions:** Best customers with high R, F, M scores
2. **Loyal:** Frequent purchasers who buy regularly
3. **Potential Loyalist:** Recent customers showing loyalty potential
4. **New Customers:** Recent first-time or low-frequency buyers
5. **Promising:** Recent customers with moderate spending
6. **Need Attention:** Moderate scores, declining engagement
7. **At Risk:** Previously good customers with declining recency
8. **Can't Lose:** High-value customers at risk of churning
9. **Hibernating:** Low engagement, dormant customers
10. **Lost:** Very low scores across all dimensions

---

## Distribution Analysis

### Customer Distribution by Segment
```
{rfm['rfm_segment'].value_counts().sort_values(ascending=False).to_string()}
```

### Revenue Distribution by Segment
```
{segment_stats[['total_revenue', 'revenue_percentage']].sort_values('total_revenue', ascending=False).to_string()}
```

---

## Business Insights

### Critical Findings

1. **Revenue Concentration**
   - Top 5% of customers (VIP) contribute {vip_customers['monetary'].sum()/rfm['monetary'].sum()*100:.1f}% of total revenue
   - Champions segment drives significant value despite being {rfm[rfm['rfm_segment']=='Champions'].shape[0]/len(rfm)*100:.1f}% of customers

2. **At-Risk Revenue**
   - "Can't Lose" segment: {segment_stats.loc["Can't Lose", 'customer_count'] if "Can't Lose" in segment_stats.index else 0:,.0f} high-value customers at risk
   - Potential revenue loss if no intervention: ${segment_stats.loc["Can't Lose", 'total_revenue'] if "Can't Lose" in segment_stats.index else 0:,.2f}

3. **Growth Opportunities**
   - New Customers: {rfm[rfm['rfm_segment']=='New Customers'].shape[0]:,} customers ready for conversion campaigns
   - Potential Loyalists: {rfm[rfm['rfm_segment']=='Potential Loyalist'].shape[0]:,} customers showing loyalty potential

4. **Engagement Issues**
   - {rfm[rfm['rfm_segment'].isin(['At Risk', 'Hibernating', 'Lost'])].shape[0]:,} customers ({rfm[rfm['rfm_segment'].isin(['At Risk', 'Hibernating', 'Lost'])].shape[0]/len(rfm)*100:.1f}%) show low engagement
   - Average recency of {rfm['recency'].mean():.1f} days indicates room for re-engagement

---

## Recommendations

### Retention Strategy (Priority 1)
- **Target:** Champions, Loyal, Can't Lose
- **Action:** VIP programs, exclusive offers, personalized service
- **Goal:** Maintain 95%+ retention of top-tier customers

### Re-engagement Strategy (Priority 2)
- **Target:** At Risk, Need Attention
- **Action:** Win-back campaigns, satisfaction surveys, incentives
- **Goal:** Reactivate 30-40% of at-risk customers

### Growth Strategy (Priority 3)
- **Target:** New Customers, Potential Loyalist, Promising
- **Action:** Onboarding programs, loyalty incentives, cross-sell
- **Goal:** Convert 50%+ to repeat purchasers

### Optimization Strategy (Priority 4)
- **Target:** Hibernating, Lost
- **Action:** Low-cost reactivation, A/B testing, list cleanup
- **Goal:** Cost-efficient revival or graceful sunset

---

## Technical Details

### Data Sources
- Orders: {len(orders):,} total records ({len(orders_delivered):,} delivered)
- Order Items: {len(order_items):,} line items
- Customers: {len(customers):,} unique customers

### Analysis Parameters
- RFM Scoring: Quintile-based (1-5 scale)
- VIP Threshold: 95th percentile (${vip_threshold:,.2f})
- Segmentation: 10 distinct customer segments
- Time Window: From earliest to {analysis_date.strftime('%Y-%m-%d')}

### Data Quality
- Missing Values: Handled through filtering delivered orders
- Outliers: Retained for accurate high-value customer identification
- Recency Calculation: Based on most recent order date in dataset

---

## Appendix: Files Generated

1. **rfm_analysis.csv** - Complete RFM data for all {len(rfm):,} customers
2. **customer_segments.csv** - Segment statistics and metrics
3. **vip_customers.csv** - Top 5% high-value customers ({len(vip_customers):,} records)
4. **segment_strategies.md** - Detailed marketing strategies per segment
5. **rfm_summary.json** - Machine-readable analysis summary
6. **Visualizations:**
   - rfm_segments_distribution.png - Segment size distribution
   - monetary_distribution.png - Customer value distribution
   - rfm_3d_scatter.png - 3D RFM visualization
   - segment_revenue_contribution.png - Revenue by segment
   - rfm_segment_heatmap.png - RFM scores heatmap

---

*Analysis completed successfully. All outputs saved to: {output_dir}*
"""

with open(f'{output_dir}/segmentation_report.md', 'w') as f:
    f.write(segmentation_report)
print(f"✓ Saved: segmentation_report.md")

# Print final summary
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\n✓ All outputs saved to: {output_dir}")
print(f"\n📊 Files Generated:")
print(f"   • rfm_analysis.csv ({len(rfm):,} customers)")
print(f"   • customer_segments.csv ({len(segment_stats)} segments)")
print(f"   • vip_customers.csv ({len(vip_customers)} VIP customers)")
print(f"   • segment_strategies.md (Marketing playbook)")
print(f"   • segmentation_report.md (Complete analysis)")
print(f"   • rfm_summary.json (Metrics summary)")
print(f"\n📈 Visualizations:")
print(f"   • rfm_segments_distribution.png")
print(f"   • monetary_distribution.png")
print(f"   • rfm_3d_scatter.png")
print(f"   • segment_revenue_contribution.png")
print(f"   • rfm_segment_heatmap.png")

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)
print(f"\n1. REVENUE CONCENTRATION")
print(f"   • {len(vip_customers)} VIP customers ({len(vip_customers)/len(rfm)*100:.1f}%) generate ${vip_customers['monetary'].sum():,.2f}")
print(f"   • This represents {vip_customers['monetary'].sum()/rfm['monetary'].sum()*100:.1f}% of total revenue")

print(f"\n2. TOP SEGMENTS")
top_3_segments = segment_stats.nlargest(3, 'total_revenue')
for idx, (segment, row) in enumerate(top_3_segments.iterrows(), 1):
    print(f"   {idx}. {segment}: {int(row['customer_count']):,} customers, ${row['total_revenue']:,.2f} ({row['revenue_percentage']:.1f}%)")

print(f"\n3. AT-RISK CUSTOMERS")
at_risk_segments = ['At Risk', "Can't Lose", 'Hibernating']
at_risk_count = rfm[rfm['rfm_segment'].isin(at_risk_segments)].shape[0]
at_risk_revenue = segment_stats[segment_stats.index.isin(at_risk_segments)]['total_revenue'].sum()
print(f"   • {at_risk_count:,} customers at risk of churning")
print(f"   • ${at_risk_revenue:,.2f} in revenue requires retention efforts")

print(f"\n4. GROWTH OPPORTUNITIES")
growth_segments = ['New Customers', 'Potential Loyalist', 'Promising']
growth_count = rfm[rfm['rfm_segment'].isin(growth_segments)].shape[0]
print(f"   • {growth_count:,} customers ready for loyalty conversion")
print(f"   • Potential for significant LTV growth")

print("\n" + "=" * 80)
print("🎯 RFM ANALYSIS SUCCESSFULLY COMPLETED!")
print("=" * 80)
