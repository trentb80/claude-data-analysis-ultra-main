# RFM Customer Segmentation Analysis Report
## Olist E-commerce Dataset

**Analysis Date:** 2018-08-29
**Report Generated:** 2026-02-04 18:44:28

---

## Executive Summary

This RFM (Recency, Frequency, Monetary) analysis segments 96,478 customers from the Olist e-commerce platform based on their purchasing behavior. The analysis identifies high-value customers, at-risk segments, and growth opportunities.

### Key Metrics
- **Total Customers:** 96,478
- **Total Revenue:** $15,419,773.75
- **Average Customer Value:** $159.83
- **Median Customer Value:** $105.28
- **Average Order Frequency:** 1.00 orders
- **Average Recency:** 239.1 days

### VIP Customers (Top 5%)
- **Count:** 4,824 customers (5.0%)
- **Revenue:** $4,121,246.39 (26.7% of total)
- **Minimum Spend:** $446.23

---

## RFM Methodology

### Recency (R)
Days since last purchase, measured from 2018-08-29
- **Score 5:** Most recent purchasers (0-94 days)
- **Score 1:** Least recent purchasers (385+ days)

### Frequency (F)
Total number of orders placed
- **Score 5:** Most frequent buyers (1+ orders)
- **Score 1:** Least frequent buyers (1 order)

### Monetary (M)
Total amount spent (including shipping)
- **Score 5:** Highest spenders ($201.82+)
- **Score 1:** Lowest spenders (up to $54.37)

---

## Customer Segmentation Results

### Segment Overview

| rfm_segment        |   customer_count |   avg_recency |   avg_frequency |   avg_monetary |    total_revenue |   revenue_percentage |
|:-------------------|-----------------:|--------------:|----------------:|---------------:|-----------------:|---------------------:|
| Loyal              |            32225 |        268.63 |               1 |         133.33 |      4.29651e+06 |                27.86 |
| New Customers      |            15606 |         91.37 |               1 |         161.7  |      2.52353e+06 |                16.37 |
| Champions          |             6366 |         92.32 |               1 |         294.67 |      1.87586e+06 |                12.17 |
| Potential Loyalist |            11542 |        134.76 |               1 |         161.99 |      1.86967e+06 |                12.13 |
| Can't Lose         |             4409 |        423.14 |               1 |         299.01 |      1.31834e+06 |                 8.55 |
| Need Attention     |             6958 |        308.77 |               1 |         179.11 |      1.24623e+06 |                 8.08 |
| Promising          |             4541 |        222.98 |               1 |         214.07 | 972083           |                 6.3  |
| At Risk            |             4621 |        449.92 |               1 |         144.63 | 668321           |                 4.33 |
| Hibernating        |             7801 |        411.12 |               1 |          68.16 | 531681           |                 3.45 |
| Lost               |             2409 |        220.68 |               1 |          48.8  | 117552           |                 0.76 |

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
rfm_segment
Loyal                 32225
New Customers         15606
Potential Loyalist    11542
Hibernating            7801
Need Attention         6958
Champions              6366
At Risk                4621
Promising              4541
Can't Lose             4409
Lost                   2409
```

### Revenue Distribution by Segment
```
                    total_revenue  revenue_percentage
rfm_segment                                          
Loyal                  4296506.02               27.86
New Customers          2523529.72               16.37
Champions              1875855.53               12.17
Potential Loyalist     1869667.98               12.13
Can't Lose             1318344.01                8.55
Need Attention         1246233.57                8.08
Promising               972083.43                6.30
At Risk                 668320.74                4.33
Hibernating             531681.19                3.45
Lost                    117551.56                0.76
```

---

## Business Insights

### Critical Findings

1. **Revenue Concentration**
   - Top 5% of customers (VIP) contribute 26.7% of total revenue
   - Champions segment drives significant value despite being 6.6% of customers

2. **At-Risk Revenue**
   - "Can't Lose" segment: 4,409 high-value customers at risk
   - Potential revenue loss if no intervention: $1,318,344.01

3. **Growth Opportunities**
   - New Customers: 15,606 customers ready for conversion campaigns
   - Potential Loyalists: 11,542 customers showing loyalty potential

4. **Engagement Issues**
   - 14,831 customers (15.4%) show low engagement
   - Average recency of 239.1 days indicates room for re-engagement

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
- Orders: 99,441 total records (96,478 delivered)
- Order Items: 112,650 line items
- Customers: 99,441 unique customers

### Analysis Parameters
- RFM Scoring: Quintile-based (1-5 scale)
- VIP Threshold: 95th percentile ($446.23)
- Segmentation: 10 distinct customer segments
- Time Window: From earliest to 2018-08-29

### Data Quality
- Missing Values: Handled through filtering delivered orders
- Outliers: Retained for accurate high-value customer identification
- Recency Calculation: Based on most recent order date in dataset

---

## Appendix: Files Generated

1. **rfm_analysis.csv** - Complete RFM data for all 96,478 customers
2. **customer_segments.csv** - Segment statistics and metrics
3. **vip_customers.csv** - Top 5% high-value customers (4,824 records)
4. **segment_strategies.md** - Detailed marketing strategies per segment
5. **rfm_summary.json** - Machine-readable analysis summary
6. **Visualizations:**
   - rfm_segments_distribution.png - Segment size distribution
   - monetary_distribution.png - Customer value distribution
   - rfm_3d_scatter.png - 3D RFM visualization
   - segment_revenue_contribution.png - Revenue by segment
   - rfm_segment_heatmap.png - RFM scores heatmap

---

*Analysis completed successfully. All outputs saved to: /home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/rfm-customer-segmentation*
