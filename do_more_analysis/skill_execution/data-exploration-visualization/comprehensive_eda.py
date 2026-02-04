"""
Comprehensive Exploratory Data Analysis for Olist E-commerce Dataset
Author: Claude Data Analysis Assistant
Date: 2026-02-04
"""

import pandas as pd
import numpy as np
import json
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = Path('/home/user/claude-data-analysis-ultra-main/data_storage')
OUTPUT_PATH = Path('/home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/data-exploration-visualization')

print("=" * 80)
print("OLIST E-COMMERCE DATASET - COMPREHENSIVE EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# ============================================================================
# SECTION 1: DATA LOADING
# ============================================================================
print("\n[1/6] Loading all datasets...")

datasets = {}
file_info = {}

try:
    datasets['orders'] = pd.read_csv(DATA_PATH / 'Orders.csv')
    datasets['customers'] = pd.read_csv(DATA_PATH / 'Customers.csv')
    datasets['order_items'] = pd.read_csv(DATA_PATH / 'Order Items.csv')
    datasets['payments'] = pd.read_csv(DATA_PATH / 'Order Payments.csv')
    datasets['reviews'] = pd.read_csv(DATA_PATH / 'Reviews.csv')
    datasets['products'] = pd.read_csv(DATA_PATH / 'Products.csv')
    datasets['sellers'] = pd.read_csv(DATA_PATH / 'Sellers.csv')
    datasets['categories'] = pd.read_csv(DATA_PATH / 'Categories.csv')

    print("✓ Successfully loaded 8 datasets")

    for name, df in datasets.items():
        file_info[name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'size_mb': df.memory_usage(deep=True).sum() / (1024**2)
        }
        print(f"  - {name.capitalize()}: {file_info[name]['rows']:,} rows, {file_info[name]['columns']} columns, {file_info[name]['size_mb']:.2f} MB")

except Exception as e:
    print(f"✗ Error loading datasets: {e}")
    exit(1)

# ============================================================================
# SECTION 2: DATA QUALITY ASSESSMENT
# ============================================================================
print("\n[2/6] Assessing data quality...")

data_quality = {}

for name, df in datasets.items():
    quality_metrics = {
        'total_records': len(df),
        'total_fields': len(df.columns),
        'missing_values': {},
        'missing_percentage': {},
        'duplicate_rows': df.duplicated().sum(),
        'duplicate_percentage': (df.duplicated().sum() / len(df) * 100) if len(df) > 0 else 0,
        'data_types': df.dtypes.astype(str).to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024**2)
    }

    # Missing values analysis
    missing = df.isnull().sum()
    quality_metrics['missing_values'] = missing[missing > 0].to_dict()
    quality_metrics['missing_percentage'] = {
        col: (count / len(df) * 100)
        for col, count in quality_metrics['missing_values'].items()
    }

    # Completeness score (percentage of non-null values)
    quality_metrics['completeness_score'] = ((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100) if len(df) > 0 else 0

    data_quality[name] = quality_metrics

    print(f"\n  {name.upper()}:")
    print(f"    - Completeness: {quality_metrics['completeness_score']:.2f}%")
    print(f"    - Duplicates: {quality_metrics['duplicate_rows']:,} ({quality_metrics['duplicate_percentage']:.2f}%)")
    if quality_metrics['missing_values']:
        print(f"    - Missing values in {len(quality_metrics['missing_values'])} columns")

# ============================================================================
# SECTION 3: STATISTICAL SUMMARIES
# ============================================================================
print("\n[3/6] Generating statistical summaries...")

statistical_summaries = []

# Orders dataset statistics
if 'orders' in datasets and len(datasets['orders']) > 0:
    orders = datasets['orders'].copy()

    # Convert date columns
    date_cols = [col for col in orders.columns if 'date' in col.lower() or 'timestamp' in col.lower()]
    for col in date_cols:
        try:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')
        except:
            pass

    # Order status distribution
    if 'order_status' in orders.columns:
        status_dist = orders['order_status'].value_counts()
        for status, count in status_dist.items():
            statistical_summaries.append({
                'Dataset': 'Orders',
                'Metric': f'Status: {status}',
                'Value': count,
                'Percentage': f"{count/len(orders)*100:.2f}%"
            })

# Order Items dataset statistics
if 'order_items' in datasets and len(datasets['order_items']) > 0:
    items = datasets['order_items'].copy()

    numeric_cols = items.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        stats = items[col].describe()
        statistical_summaries.append({
            'Dataset': 'Order Items',
            'Metric': f'{col} - Mean',
            'Value': stats['mean'],
            'Percentage': ''
        })
        statistical_summaries.append({
            'Dataset': 'Order Items',
            'Metric': f'{col} - Median',
            'Value': stats['50%'],
            'Percentage': ''
        })
        statistical_summaries.append({
            'Dataset': 'Order Items',
            'Metric': f'{col} - Std Dev',
            'Value': stats['std'],
            'Percentage': ''
        })

# Payments dataset statistics
if 'payments' in datasets and len(datasets['payments']) > 0:
    payments = datasets['payments'].copy()

    if 'payment_type' in payments.columns:
        payment_dist = payments['payment_type'].value_counts()
        for payment_type, count in payment_dist.items():
            statistical_summaries.append({
                'Dataset': 'Payments',
                'Metric': f'Payment Type: {payment_type}',
                'Value': count,
                'Percentage': f"{count/len(payments)*100:.2f}%"
            })

# Reviews dataset statistics
if 'reviews' in datasets and len(datasets['reviews']) > 0:
    reviews = datasets['reviews'].copy()

    if 'review_score' in reviews.columns:
        score_dist = reviews['review_score'].value_counts().sort_index()
        for score, count in score_dist.items():
            statistical_summaries.append({
                'Dataset': 'Reviews',
                'Metric': f'Review Score: {score}',
                'Value': count,
                'Percentage': f"{count/len(reviews)*100:.2f}%"
            })

print(f"  ✓ Generated {len(statistical_summaries)} statistical metrics")

# ============================================================================
# SECTION 4: KEY BUSINESS METRICS CALCULATION
# ============================================================================
print("\n[4/6] Calculating key business metrics...")

business_metrics = {}

# Order metrics
if 'orders' in datasets:
    orders = datasets['orders'].copy()
    business_metrics['total_orders'] = len(orders)

    # Convert dates for time-based analysis
    date_cols = [col for col in orders.columns if 'purchase' in col.lower() and 'timestamp' in col.lower()]
    if date_cols:
        purchase_col = date_cols[0]
        orders[purchase_col] = pd.to_datetime(orders[purchase_col], errors='coerce')
        valid_dates = orders[purchase_col].dropna()

        if len(valid_dates) > 0:
            business_metrics['date_range_start'] = valid_dates.min().strftime('%Y-%m-%d')
            business_metrics['date_range_end'] = valid_dates.max().strftime('%Y-%m-%d')
            business_metrics['time_span_days'] = (valid_dates.max() - valid_dates.min()).days

# Customer metrics
if 'customers' in datasets:
    customers = datasets['customers'].copy()
    business_metrics['total_customers'] = len(customers)
    business_metrics['unique_customers'] = customers.iloc[:, 0].nunique() if len(customers.columns) > 0 else 0

# Order Items metrics
if 'order_items' in datasets:
    items = datasets['order_items'].copy()
    business_metrics['total_items_sold'] = len(items)

    # Price analysis
    price_col = [col for col in items.columns if 'price' in col.lower()]
    if price_col:
        price_col = price_col[0]
        business_metrics['average_item_price'] = float(items[price_col].mean()) if len(items) > 0 else 0
        business_metrics['median_item_price'] = float(items[price_col].median()) if len(items) > 0 else 0
        business_metrics['total_revenue'] = float(items[price_col].sum()) if len(items) > 0 else 0

    # Freight analysis
    freight_col = [col for col in items.columns if 'freight' in col.lower()]
    if freight_col:
        freight_col = freight_col[0]
        business_metrics['total_freight_cost'] = float(items[freight_col].sum()) if len(items) > 0 else 0
        business_metrics['average_freight_cost'] = float(items[freight_col].mean()) if len(items) > 0 else 0

# Payment metrics
if 'payments' in datasets:
    payments = datasets['payments'].copy()

    value_col = [col for col in payments.columns if 'value' in col.lower()]
    if value_col:
        value_col = value_col[0]
        business_metrics['total_payment_value'] = float(payments[value_col].sum()) if len(payments) > 0 else 0
        business_metrics['average_payment_value'] = float(payments[value_col].mean()) if len(payments) > 0 else 0

    installment_col = [col for col in payments.columns if 'installment' in col.lower()]
    if installment_col:
        installment_col = installment_col[0]
        business_metrics['average_installments'] = float(payments[installment_col].mean()) if len(payments) > 0 else 0

# Review metrics
if 'reviews' in datasets:
    reviews = datasets['reviews'].copy()
    business_metrics['total_reviews'] = len(reviews)

    score_col = [col for col in reviews.columns if 'score' in col.lower()]
    if score_col:
        score_col = score_col[0]
        business_metrics['average_review_score'] = float(reviews[score_col].mean()) if len(reviews) > 0 else 0
        business_metrics['median_review_score'] = float(reviews[score_col].median()) if len(reviews) > 0 else 0

# Product metrics
if 'products' in datasets:
    products = datasets['products'].copy()
    business_metrics['total_products'] = len(products)
    business_metrics['unique_products'] = products.iloc[:, 0].nunique() if len(products.columns) > 0 else 0

# Seller metrics
if 'sellers' in datasets:
    sellers = datasets['sellers'].copy()
    business_metrics['total_sellers'] = len(sellers)

# Category metrics
if 'categories' in datasets:
    categories = datasets['categories'].copy()
    business_metrics['total_categories'] = len(categories)

# Calculate derived metrics
if 'total_orders' in business_metrics and 'total_customers' in business_metrics and business_metrics['total_customers'] > 0:
    business_metrics['orders_per_customer'] = business_metrics['total_orders'] / business_metrics['total_customers']

if 'total_revenue' in business_metrics and 'total_orders' in business_metrics and business_metrics['total_orders'] > 0:
    business_metrics['average_order_value'] = business_metrics['total_revenue'] / business_metrics['total_orders']

if 'total_items_sold' in business_metrics and 'total_orders' in business_metrics and business_metrics['total_orders'] > 0:
    business_metrics['items_per_order'] = business_metrics['total_items_sold'] / business_metrics['total_orders']

print(f"  ✓ Calculated {len(business_metrics)} business metrics")

# ============================================================================
# SECTION 5: PATTERN AND CORRELATION ANALYSIS
# ============================================================================
print("\n[5/6] Analyzing patterns and correlations...")

patterns = {}

# Order Items correlation analysis
if 'order_items' in datasets:
    items = datasets['order_items'].copy()
    numeric_cols = items.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) >= 2:
        corr_matrix = items[numeric_cols].corr()

        # Find strong correlations (> 0.5 or < -0.5, excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': float(corr_val)
                    })

        patterns['order_items_correlations'] = strong_correlations
        print(f"  ✓ Found {len(strong_correlations)} strong correlations in Order Items")

# Review score patterns
if 'reviews' in datasets:
    reviews = datasets['reviews'].copy()

    if 'review_score' in reviews.columns:
        score_stats = {
            'distribution': reviews['review_score'].value_counts().sort_index().to_dict(),
            'mean': float(reviews['review_score'].mean()),
            'mode': int(reviews['review_score'].mode().iloc[0]) if len(reviews['review_score'].mode()) > 0 else None,
            'positive_rate': float((reviews['review_score'] >= 4).sum() / len(reviews) * 100) if len(reviews) > 0 else 0,
            'negative_rate': float((reviews['review_score'] <= 2).sum() / len(reviews) * 100) if len(reviews) > 0 else 0
        }
        patterns['review_score_patterns'] = score_stats
        print(f"  ✓ Analyzed review score patterns (Positive: {score_stats['positive_rate']:.1f}%, Negative: {score_stats['negative_rate']:.1f}%)")

# Payment type patterns
if 'payments' in datasets:
    payments = datasets['payments'].copy()

    if 'payment_type' in payments.columns:
        payment_patterns = {
            'distribution': payments['payment_type'].value_counts().to_dict(),
            'most_common': payments['payment_type'].mode().iloc[0] if len(payments['payment_type'].mode()) > 0 else None,
            'unique_types': int(payments['payment_type'].nunique())
        }
        patterns['payment_type_patterns'] = payment_patterns
        print(f"  ✓ Analyzed payment patterns ({payment_patterns['unique_types']} payment types)")

# Order status patterns
if 'orders' in datasets:
    orders = datasets['orders'].copy()

    if 'order_status' in orders.columns:
        status_patterns = {
            'distribution': orders['order_status'].value_counts().to_dict(),
            'delivery_rate': float((orders['order_status'] == 'delivered').sum() / len(orders) * 100) if len(orders) > 0 else 0,
            'cancellation_rate': float((orders['order_status'] == 'canceled').sum() / len(orders) * 100) if len(orders) > 0 else 0
        }
        patterns['order_status_patterns'] = status_patterns
        print(f"  ✓ Analyzed order status (Delivered: {status_patterns['delivery_rate']:.1f}%, Canceled: {status_patterns['cancellation_rate']:.1f}%)")

# ============================================================================
# SECTION 6: ANOMALY DETECTION
# ============================================================================
print("\n[6/6] Detecting anomalies...")

anomalies = {}

# Price anomalies in Order Items
if 'order_items' in datasets:
    items = datasets['order_items'].copy()
    price_col = [col for col in items.columns if 'price' in col.lower() and 'freight' not in col.lower()]

    if price_col:
        price_col = price_col[0]
        prices = items[price_col].dropna()

        if len(prices) > 0:
            Q1 = prices.quantile(0.25)
            Q3 = prices.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_low = (prices < lower_bound).sum()
            outliers_high = (prices > upper_bound).sum()

            anomalies['price_outliers'] = {
                'total_outliers': int(outliers_low + outliers_high),
                'low_outliers': int(outliers_low),
                'high_outliers': int(outliers_high),
                'outlier_percentage': float((outliers_low + outliers_high) / len(prices) * 100),
                'bounds': {
                    'lower': float(lower_bound),
                    'upper': float(upper_bound)
                }
            }
            print(f"  ✓ Price outliers: {anomalies['price_outliers']['total_outliers']:,} ({anomalies['price_outliers']['outlier_percentage']:.2f}%)")

# Payment value anomalies
if 'payments' in datasets:
    payments = datasets['payments'].copy()
    value_col = [col for col in payments.columns if 'value' in col.lower()]

    if value_col:
        value_col = value_col[0]
        values = payments[value_col].dropna()

        if len(values) > 0:
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1

            upper_bound = Q3 + 1.5 * IQR
            outliers_high = (values > upper_bound).sum()

            anomalies['payment_value_outliers'] = {
                'high_value_outliers': int(outliers_high),
                'outlier_percentage': float(outliers_high / len(values) * 100)
            }
            print(f"  ✓ High-value payment outliers: {anomalies['payment_value_outliers']['high_value_outliers']:,} ({anomalies['payment_value_outliers']['outlier_percentage']:.2f}%)")

# ============================================================================
# OUTPUT GENERATION
# ============================================================================
print("\n" + "=" * 80)
print("GENERATING OUTPUT FILES")
print("=" * 80)

# 1. Save exploration_summary.csv
summary_df = pd.DataFrame(statistical_summaries)
summary_output = OUTPUT_PATH / 'exploration_summary.csv'
summary_df.to_csv(summary_output, index=False)
print(f"\n✓ Saved: {summary_output}")

# 2. Save key_metrics.json
metrics_output = OUTPUT_PATH / 'key_metrics.json'
with open(metrics_output, 'w') as f:
    json.dump(business_metrics, f, indent=2)
print(f"✓ Saved: {metrics_output}")

# 3. Save data_quality_report.md
quality_report = f"""# Data Quality Assessment Report
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report provides a comprehensive assessment of data quality across all 8 datasets in the Olist e-commerce platform.

## Dataset Overview

| Dataset | Records | Fields | Size (MB) | Completeness |
|---------|---------|--------|-----------|--------------|
"""

for name, info in file_info.items():
    completeness = data_quality[name]['completeness_score']
    quality_report += f"| {name.capitalize()} | {info['rows']:,} | {info['columns']} | {info['size_mb']:.2f} | {completeness:.2f}% |\n"

quality_report += "\n## Data Quality Metrics by Dataset\n\n"

for name, metrics in data_quality.items():
    quality_report += f"### {name.upper()}\n\n"
    quality_report += f"**Overview:**\n"
    quality_report += f"- Total Records: {metrics['total_records']:,}\n"
    quality_report += f"- Total Fields: {metrics['total_fields']}\n"
    quality_report += f"- Completeness Score: {metrics['completeness_score']:.2f}%\n"
    quality_report += f"- Duplicate Rows: {metrics['duplicate_rows']:,} ({metrics['duplicate_percentage']:.2f}%)\n"
    quality_report += f"- Memory Usage: {metrics['memory_usage_mb']:.2f} MB\n\n"

    if metrics['missing_values']:
        quality_report += "**Missing Values:**\n\n"
        quality_report += "| Column | Missing Count | Missing % |\n"
        quality_report += "|--------|---------------|----------|\n"
        for col, count in metrics['missing_values'].items():
            pct = metrics['missing_percentage'][col]
            quality_report += f"| {col} | {count:,} | {pct:.2f}% |\n"
        quality_report += "\n"
    else:
        quality_report += "**Missing Values:** None detected\n\n"

quality_report += "## Quality Assessment Summary\n\n"
quality_report += "**Key Findings:**\n\n"

avg_completeness = np.mean([m['completeness_score'] for m in data_quality.values()])
quality_report += f"- Average Completeness Across All Datasets: {avg_completeness:.2f}%\n"

total_duplicates = sum([m['duplicate_rows'] for m in data_quality.values()])
quality_report += f"- Total Duplicate Rows Across All Datasets: {total_duplicates:,}\n"

datasets_with_missing = len([m for m in data_quality.values() if m['missing_values']])
quality_report += f"- Datasets with Missing Values: {datasets_with_missing}/{len(data_quality)}\n\n"

quality_report += "**Recommendations:**\n\n"
if avg_completeness < 95:
    quality_report += "- Investigate and address missing values in key columns\n"
if total_duplicates > 0:
    quality_report += "- Review duplicate records and determine if they should be removed\n"
quality_report += "- Implement data validation rules at the data entry point\n"
quality_report += "- Establish regular data quality monitoring procedures\n"

quality_output = OUTPUT_PATH / 'data_quality_report.md'
with open(quality_output, 'w') as f:
    f.write(quality_report)
print(f"✓ Saved: {quality_output}")

# 4. Save analysis_insights.md
insights_report = f"""# Olist E-commerce Data Analysis Insights
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report presents key insights from comprehensive exploratory data analysis of the Olist e-commerce platform, covering {business_metrics.get('total_orders', 'N/A'):,} orders, {business_metrics.get('total_customers', 'N/A'):,} customers, and {business_metrics.get('total_products', 'N/A'):,} products.

## Key Business Metrics

### Order Metrics
"""

if 'total_orders' in business_metrics:
    insights_report += f"- **Total Orders**: {business_metrics['total_orders']:,}\n"
if 'date_range_start' in business_metrics:
    insights_report += f"- **Date Range**: {business_metrics['date_range_start']} to {business_metrics['date_range_end']}\n"
    insights_report += f"- **Time Span**: {business_metrics['time_span_days']} days\n"
if 'average_order_value' in business_metrics:
    insights_report += f"- **Average Order Value**: ${business_metrics['average_order_value']:.2f}\n"
if 'items_per_order' in business_metrics:
    insights_report += f"- **Items per Order**: {business_metrics['items_per_order']:.2f}\n"

insights_report += "\n### Customer Metrics\n"
if 'total_customers' in business_metrics:
    insights_report += f"- **Total Customers**: {business_metrics['total_customers']:,}\n"
if 'orders_per_customer' in business_metrics:
    insights_report += f"- **Orders per Customer**: {business_metrics['orders_per_customer']:.2f}\n"

insights_report += "\n### Revenue Metrics\n"
if 'total_revenue' in business_metrics:
    insights_report += f"- **Total Revenue**: ${business_metrics['total_revenue']:,.2f}\n"
if 'average_item_price' in business_metrics:
    insights_report += f"- **Average Item Price**: ${business_metrics['average_item_price']:.2f}\n"
    insights_report += f"- **Median Item Price**: ${business_metrics['median_item_price']:.2f}\n"
if 'total_freight_cost' in business_metrics:
    insights_report += f"- **Total Freight Cost**: ${business_metrics['total_freight_cost']:,.2f}\n"
    insights_report += f"- **Average Freight Cost**: ${business_metrics['average_freight_cost']:.2f}\n"

insights_report += "\n### Payment Metrics\n"
if 'total_payment_value' in business_metrics:
    insights_report += f"- **Total Payment Value**: ${business_metrics['total_payment_value']:,.2f}\n"
    insights_report += f"- **Average Payment Value**: ${business_metrics['average_payment_value']:.2f}\n"
if 'average_installments' in business_metrics:
    insights_report += f"- **Average Installments**: {business_metrics['average_installments']:.2f}\n"

insights_report += "\n### Customer Satisfaction\n"
if 'average_review_score' in business_metrics:
    insights_report += f"- **Average Review Score**: {business_metrics['average_review_score']:.2f}/5.0\n"
    insights_report += f"- **Median Review Score**: {business_metrics['median_review_score']:.1f}/5.0\n"
if 'total_reviews' in business_metrics:
    insights_report += f"- **Total Reviews**: {business_metrics['total_reviews']:,}\n"

insights_report += "\n### Marketplace Metrics\n"
if 'total_products' in business_metrics:
    insights_report += f"- **Total Products**: {business_metrics['total_products']:,}\n"
if 'total_sellers' in business_metrics:
    insights_report += f"- **Total Sellers**: {business_metrics['total_sellers']:,}\n"
if 'total_categories' in business_metrics:
    insights_report += f"- **Total Categories**: {business_metrics['total_categories']:,}\n"

insights_report += "\n## Pattern Analysis\n\n"

# Review patterns
if 'review_score_patterns' in patterns:
    rsp = patterns['review_score_patterns']
    insights_report += "### Customer Satisfaction Patterns\n\n"
    insights_report += f"- **Positive Reviews (4-5 stars)**: {rsp['positive_rate']:.1f}%\n"
    insights_report += f"- **Negative Reviews (1-2 stars)**: {rsp['negative_rate']:.1f}%\n"
    insights_report += f"- **Most Common Score**: {rsp['mode']}\n"
    insights_report += f"- **Average Score**: {rsp['mean']:.2f}/5.0\n\n"

    if rsp['positive_rate'] > 70:
        insights_report += "**Insight**: High customer satisfaction rate indicates strong product quality and service delivery.\n\n"
    elif rsp['negative_rate'] > 20:
        insights_report += "**Insight**: Significant negative review rate suggests areas for improvement in product quality or delivery experience.\n\n"

# Order status patterns
if 'order_status_patterns' in patterns:
    osp = patterns['order_status_patterns']
    insights_report += "### Order Fulfillment Patterns\n\n"
    insights_report += f"- **Delivery Success Rate**: {osp['delivery_rate']:.1f}%\n"
    insights_report += f"- **Cancellation Rate**: {osp['cancellation_rate']:.1f}%\n"
    insights_report += "- **Order Status Distribution**:\n"
    for status, count in osp['distribution'].items():
        pct = count / sum(osp['distribution'].values()) * 100
        insights_report += f"  - {status}: {count:,} ({pct:.1f}%)\n"
    insights_report += "\n"

    if osp['delivery_rate'] > 90:
        insights_report += "**Insight**: Excellent delivery success rate demonstrates strong logistics capabilities.\n\n"
    if osp['cancellation_rate'] > 5:
        insights_report += "**Insight**: Cancellation rate suggests opportunity to improve order confirmation or inventory management.\n\n"

# Payment patterns
if 'payment_type_patterns' in patterns:
    ptp = patterns['payment_type_patterns']
    insights_report += "### Payment Behavior Patterns\n\n"
    insights_report += f"- **Most Popular Payment Method**: {ptp['most_common']}\n"
    insights_report += f"- **Payment Methods Available**: {ptp['unique_types']}\n"
    insights_report += "- **Payment Type Distribution**:\n"
    for payment_type, count in ptp['distribution'].items():
        pct = count / sum(ptp['distribution'].values()) * 100
        insights_report += f"  - {payment_type}: {count:,} ({pct:.1f}%)\n"
    insights_report += "\n"

# Correlations
if 'order_items_correlations' in patterns and patterns['order_items_correlations']:
    insights_report += "### Correlation Insights\n\n"
    insights_report += "**Strong Correlations Detected:**\n\n"
    for corr in patterns['order_items_correlations']:
        insights_report += f"- {corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f}\n"
    insights_report += "\n"

insights_report += "## Anomaly Detection\n\n"

if 'price_outliers' in anomalies:
    po = anomalies['price_outliers']
    insights_report += "### Price Anomalies\n\n"
    insights_report += f"- **Total Price Outliers**: {po['total_outliers']:,} ({po['outlier_percentage']:.2f}%)\n"
    insights_report += f"- **Below Normal Range**: {po['low_outliers']:,}\n"
    insights_report += f"- **Above Normal Range**: {po['high_outliers']:,}\n"
    insights_report += f"- **Expected Range**: ${po['bounds']['lower']:.2f} - ${po['bounds']['upper']:.2f}\n\n"

    if po['outlier_percentage'] > 5:
        insights_report += "**Insight**: Significant price outliers may indicate pricing errors or special promotional items.\n\n"

if 'payment_value_outliers' in anomalies:
    pvo = anomalies['payment_value_outliers']
    insights_report += "### Payment Value Anomalies\n\n"
    insights_report += f"- **High-Value Transactions**: {pvo['high_value_outliers']:,} ({pvo['outlier_percentage']:.2f}%)\n\n"

    if pvo['outlier_percentage'] > 1:
        insights_report += "**Insight**: High-value outliers represent premium customers or bulk orders worth special attention.\n\n"

insights_report += "## Strategic Recommendations\n\n"
insights_report += "### Customer Experience\n"
if 'review_score_patterns' in patterns and patterns['review_score_patterns']['negative_rate'] > 15:
    insights_report += "1. **Improve Product Quality**: Focus on reducing negative reviews by enhancing quality control\n"
if 'order_status_patterns' in patterns and patterns['order_status_patterns']['cancellation_rate'] > 3:
    insights_report += "2. **Reduce Cancellations**: Implement better inventory management and customer communication\n"
insights_report += "3. **Leverage Satisfied Customers**: Use high satisfaction rate for marketing and referral programs\n\n"

insights_report += "### Revenue Optimization\n"
if 'items_per_order' in business_metrics and business_metrics['items_per_order'] < 2:
    insights_report += "1. **Cross-Selling**: Increase items per order through product recommendations\n"
if 'orders_per_customer' in business_metrics and business_metrics['orders_per_customer'] < 1.5:
    insights_report += "2. **Customer Retention**: Develop loyalty programs to increase repeat purchases\n"
insights_report += "3. **Price Optimization**: Analyze price outliers to refine pricing strategy\n\n"

insights_report += "### Operational Efficiency\n"
insights_report += "1. **Freight Cost Management**: Optimize shipping costs while maintaining delivery quality\n"
if 'payment_type_patterns' in patterns:
    insights_report += "2. **Payment Options**: Ensure popular payment methods are well-supported and optimized\n"
insights_report += "3. **Data Quality**: Continue maintaining high data completeness for better analytics\n\n"

insights_report += "## Conclusion\n\n"
insights_report += "The Olist e-commerce platform demonstrates:\n"
if 'average_review_score' in business_metrics and business_metrics['average_review_score'] > 4:
    insights_report += "- Strong customer satisfaction with high review scores\n"
if 'order_status_patterns' in patterns and patterns['order_status_patterns']['delivery_rate'] > 90:
    insights_report += "- Excellent operational efficiency in order fulfillment\n"
insights_report += "- Opportunities for growth through customer retention and cross-selling\n"
insights_report += "- Solid data foundation for advanced analytics and machine learning applications\n"

insights_output = OUTPUT_PATH / 'analysis_insights.md'
with open(insights_output, 'w') as f:
    f.write(insights_report)
print(f"✓ Saved: {insights_output}")

# Summary of all outputs
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nOutput files generated in: {OUTPUT_PATH}")
print(f"\n1. exploration_summary.csv - {len(statistical_summaries)} statistical metrics")
print(f"2. key_metrics.json - {len(business_metrics)} business KPIs")
print(f"3. data_quality_report.md - Quality assessment for {len(data_quality)} datasets")
print(f"4. analysis_insights.md - Comprehensive business insights and recommendations")

print("\n" + "=" * 80)
print("KEY HIGHLIGHTS")
print("=" * 80)
if 'total_orders' in business_metrics:
    print(f"- Total Orders: {business_metrics['total_orders']:,}")
if 'total_customers' in business_metrics:
    print(f"- Total Customers: {business_metrics['total_customers']:,}")
if 'total_revenue' in business_metrics:
    print(f"- Total Revenue: ${business_metrics['total_revenue']:,.2f}")
if 'average_review_score' in business_metrics:
    print(f"- Average Review Score: {business_metrics['average_review_score']:.2f}/5.0")
if 'order_status_patterns' in patterns:
    print(f"- Delivery Success Rate: {patterns['order_status_patterns']['delivery_rate']:.1f}%")

print("\n✓ Exploratory Data Analysis completed successfully!")
