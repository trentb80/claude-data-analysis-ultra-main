"""
Data Visualization Script for Olist E-commerce EDA
Generates comprehensive visualizations for business insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configuration
DATA_PATH = Path('/home/user/claude-data-analysis-ultra-main/data_storage')
OUTPUT_PATH = Path('/home/user/claude-data-analysis-ultra-main/do_more_analysis/skill_execution/data-exploration-visualization')

print("Generating visualizations for Olist E-commerce dataset...")

# Load datasets
orders = pd.read_csv(DATA_PATH / 'Orders.csv')
order_items = pd.read_csv(DATA_PATH / 'Order Items.csv')
payments = pd.read_csv(DATA_PATH / 'Order Payments.csv')
reviews = pd.read_csv(DATA_PATH / 'Reviews.csv')

# ============================================================================
# VISUALIZATION 1: Order Status Distribution
# ============================================================================
print("\n[1/5] Creating order status distribution chart...")

if 'order_status' in orders.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    status_counts = orders['order_status'].value_counts()

    colors = sns.color_palette("husl", len(status_counts))
    bars = ax.bar(range(len(status_counts)), status_counts.values, color=colors)

    ax.set_xlabel('Order Status', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Orders', fontsize=12, fontweight='bold')
    ax.set_title('Order Status Distribution - Olist E-commerce Platform', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(status_counts)))
    ax.set_xticklabels(status_counts.index, rotation=45, ha='right')

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, status_counts.values)):
        height = bar.get_height()
        percentage = (value / len(orders)) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / '01_order_status_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: 01_order_status_distribution.png")

# ============================================================================
# VISUALIZATION 2: Review Score Distribution
# ============================================================================
print("[2/5] Creating review score distribution chart...")

if 'review_score' in reviews.columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Bar chart
    score_counts = reviews['review_score'].value_counts().sort_index()
    colors_gradient = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(score_counts)))

    bars = ax1.bar(score_counts.index, score_counts.values, color=colors_gradient, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Review Score (1-5)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    ax1.set_title('Customer Review Score Distribution', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(score_counts.index)
    ax1.grid(axis='y', alpha=0.3)

    for bar, value in zip(bars, score_counts.values):
        height = bar.get_height()
        percentage = (value / len(reviews)) * 100
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Pie chart
    positive = (reviews['review_score'] >= 4).sum()
    neutral = (reviews['review_score'] == 3).sum()
    negative = (reviews['review_score'] <= 2).sum()

    categories = ['Positive\n(4-5 stars)', 'Neutral\n(3 stars)', 'Negative\n(1-2 stars)']
    values = [positive, neutral, negative]
    colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']

    wedges, texts, autotexts = ax2.pie(values, labels=categories, autopct='%1.1f%%',
                                         colors=colors_pie, startangle=90,
                                         textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Customer Sentiment Overview', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / '02_review_score_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: 02_review_score_distribution.png")

# ============================================================================
# VISUALIZATION 3: Payment Type Distribution
# ============================================================================
print("[3/5] Creating payment type distribution chart...")

if 'payment_type' in payments.columns:
    fig, ax = plt.subplots(figsize=(12, 7))

    payment_counts = payments['payment_type'].value_counts()
    colors = sns.color_palette("Set2", len(payment_counts))

    wedges, texts, autotexts = ax.pie(payment_counts.values,
                                        labels=payment_counts.index,
                                        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(payment_counts.values)):,})',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        explode=[0.05 if i == 0 else 0 for i in range(len(payment_counts))])

    ax.set_title('Payment Method Distribution - Olist Platform', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / '03_payment_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: 03_payment_type_distribution.png")

# ============================================================================
# VISUALIZATION 4: Price Distribution Analysis
# ============================================================================
print("[4/5] Creating price distribution analysis...")

price_col = [col for col in order_items.columns if 'price' in col.lower() and 'freight' not in col.lower()]
if price_col:
    price_col = price_col[0]
    prices = order_items[price_col].dropna()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Histogram
    ax1.hist(prices, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Price (R$)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax1.set_title('Item Price Distribution', fontsize=14, fontweight='bold', pad=20)
    ax1.axvline(prices.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: R${prices.mean():.2f}')
    ax1.axvline(prices.median(), color='green', linestyle='--', linewidth=2, label=f'Median: R${prices.median():.2f}')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Box plot
    ax2.boxplot(prices, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', edgecolor='black'),
                medianprops=dict(color='red', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.5),
                capprops=dict(color='black', linewidth=1.5))
    ax2.set_ylabel('Price (R$)', fontsize=12, fontweight='bold')
    ax2.set_title('Price Distribution - Box Plot', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(alpha=0.3)

    # Add statistics text
    stats_text = f'Mean: R${prices.mean():.2f}\nMedian: R${prices.median():.2f}\nStd: R${prices.std():.2f}\nMin: R${prices.min():.2f}\nMax: R${prices.max():.2f}'
    ax2.text(1.3, prices.median(), stats_text, fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / '04_price_distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: 04_price_distribution_analysis.png")

# ============================================================================
# VISUALIZATION 5: Key Business Metrics Dashboard
# ============================================================================
print("[5/5] Creating business metrics dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Calculate metrics
total_orders = len(orders)
total_customers = len(orders['customer_id'].unique()) if 'customer_id' in orders.columns else 0
total_revenue = order_items[price_col].sum() if price_col else 0
avg_review_score = reviews['review_score'].mean() if 'review_score' in reviews.columns else 0
delivery_rate = (orders['order_status'] == 'delivered').sum() / len(orders) * 100 if 'order_status' in orders.columns else 0

# KPI Cards (top row)
kpis = [
    ('Total Orders', f'{total_orders:,}', '#3498db'),
    ('Total Customers', f'{total_customers:,}', '#2ecc71'),
    ('Total Revenue', f'R${total_revenue:,.0f}', '#f39c12')
]

for idx, (title, value, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, idx])
    ax.text(0.5, 0.7, value, ha='center', va='center', fontsize=32, fontweight='bold', color=color)
    ax.text(0.5, 0.3, title, ha='center', va='center', fontsize=16, fontweight='bold', color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0.05, 0.1), 0.9, 0.8, fill=False, edgecolor=color, linewidth=3))

# Review Score Trend (middle left)
ax_review = fig.add_subplot(gs[1, :2])
if 'review_score' in reviews.columns:
    score_dist = reviews['review_score'].value_counts().sort_index()
    bars = ax_review.bar(score_dist.index, score_dist.values, color=plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(score_dist))))
    ax_review.set_xlabel('Rating', fontsize=11, fontweight='bold')
    ax_review.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax_review.set_title('Customer Satisfaction Distribution', fontsize=12, fontweight='bold')
    ax_review.grid(axis='y', alpha=0.3)
    ax_review.set_xticks(score_dist.index)

# Satisfaction Gauge (middle right)
ax_gauge = fig.add_subplot(gs[1, 2])
satisfaction_pct = avg_review_score / 5 * 100
colors_gauge = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
color_idx = int(avg_review_score - 1) if avg_review_score >= 1 else 0
gauge_color = colors_gauge[min(color_idx, 4)]

ax_gauge.text(0.5, 0.6, f'{avg_review_score:.2f}', ha='center', va='center', fontsize=40, fontweight='bold', color=gauge_color)
ax_gauge.text(0.5, 0.35, 'Avg Rating', ha='center', va='center', fontsize=14, fontweight='bold', color='gray')
ax_gauge.text(0.5, 0.2, f'{satisfaction_pct:.1f}% Satisfaction', ha='center', va='center', fontsize=11, color='gray')
ax_gauge.set_xlim(0, 1)
ax_gauge.set_ylim(0, 1)
ax_gauge.axis('off')
ax_gauge.add_patch(plt.Circle((0.5, 0.6), 0.35, fill=False, edgecolor=gauge_color, linewidth=4))

# Order Status (bottom left)
ax_status = fig.add_subplot(gs[2, :2])
if 'order_status' in orders.columns:
    status_counts = orders['order_status'].value_counts().head(6)
    bars = ax_status.barh(range(len(status_counts)), status_counts.values, color=sns.color_palette("husl", len(status_counts)))
    ax_status.set_yticks(range(len(status_counts)))
    ax_status.set_yticklabels(status_counts.index)
    ax_status.set_xlabel('Number of Orders', fontsize=11, fontweight='bold')
    ax_status.set_title('Order Status Breakdown', fontsize=12, fontweight='bold')
    ax_status.grid(axis='x', alpha=0.3)

    for i, (bar, value) in enumerate(zip(bars, status_counts.values)):
        ax_status.text(value, i, f' {value:,}', va='center', fontsize=9, fontweight='bold')

# Delivery Performance (bottom right)
ax_delivery = fig.add_subplot(gs[2, 2])
delivered = (orders['order_status'] == 'delivered').sum() if 'order_status' in orders.columns else 0
other = total_orders - delivered

wedges, texts, autotexts = ax_delivery.pie([delivered, other],
                                             labels=['Delivered', 'Other'],
                                             autopct='%1.1f%%',
                                             colors=['#2ecc71', '#95a5a6'],
                                             startangle=90,
                                             textprops={'fontsize': 10, 'fontweight': 'bold'})
ax_delivery.set_title('Delivery Success Rate', fontsize=12, fontweight='bold')

# Main title
fig.suptitle('Olist E-commerce Platform - Business Metrics Dashboard', fontsize=18, fontweight='bold', y=0.98)

plt.savefig(OUTPUT_PATH / '05_business_metrics_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 05_business_metrics_dashboard.png")

print("\n✓ All visualizations generated successfully!")
print(f"\nVisualization files saved in: {OUTPUT_PATH}")
print("\nGenerated Charts:")
print("  1. 01_order_status_distribution.png - Order fulfillment status")
print("  2. 02_review_score_distribution.png - Customer satisfaction metrics")
print("  3. 03_payment_type_distribution.png - Payment method preferences")
print("  4. 04_price_distribution_analysis.png - Product pricing analysis")
print("  5. 05_business_metrics_dashboard.png - Comprehensive KPI dashboard")
