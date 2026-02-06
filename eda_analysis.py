#!/usr/bin/env python3
"""
Comprehensive Exploratory Data Analysis - Customers Dataset
============================================================
Performs data assessment, statistical analysis, pattern discovery,
generates visualizations, and saves structured output files.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
from scipy import stats
from pathlib import Path

warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
DATA_PATH = '/home/user/claude-data-analysis-ultra-main/data_storage/Customers.csv'
VIZ_DIR = '/home/user/claude-data-analysis-ultra-main/visualizations'
REPORT_DIR = '/home/user/claude-data-analysis-ultra-main/analysis_reports'

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')
FIGSIZE = (12, 8)
DPI = 150

# ============================================================
# PHASE 1: DATA LOADING & ASSESSMENT
# ============================================================
print("=" * 70)
print("PHASE 1: DATA LOADING & ASSESSMENT")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print(f"\nDataset Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nColumn Names: {list(df.columns)}")
print(f"\nData Types:")
print(df.dtypes.to_string())

# Missing values
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
print(f"\nMissing Values:")
for col in df.columns:
    print(f"  {col}: {missing[col]} ({missing_pct[col]}%)")

total_missing = df.isnull().sum().sum()
print(f"\nTotal missing values: {total_missing}")

# Duplicates
full_duplicates = df.duplicated().sum()
id_duplicates = df['CustomerID'].duplicated().sum()
print(f"\nFull row duplicates: {full_duplicates}")
print(f"CustomerID duplicates: {id_duplicates}")

# Summary statistics
print(f"\nSummary Statistics (Numerical):")
desc = df.describe()
print(desc.to_string())

print(f"\nSummary Statistics (Categorical):")
for col in df.select_dtypes(include='object').columns:
    print(f"\n  {col}:")
    print(f"    Unique values: {df[col].nunique()}")
    print(f"    Top value: {df[col].mode().values[0]} (count: {df[col].value_counts().iloc[0]})")
    print(f"    Value counts:")
    for val, cnt in df[col].value_counts().items():
        print(f"      {val}: {cnt} ({cnt/len(df)*100:.1f}%)")

# Data quality issues
print(f"\nData Quality Issues:")
quality_issues = []

# Check for negative values in columns that should be positive
for col in ['Age', 'Annual Income ($)', 'Spending Score (1-100)', 'Work Experience', 'Family Size']:
    neg_count = (df[col] < 0).sum()
    if neg_count > 0:
        issue = f"{col} has {neg_count} negative values"
        quality_issues.append(issue)
        print(f"  WARNING: {issue}")

# Check spending score range
out_of_range = ((df['Spending Score (1-100)'] < 1) | (df['Spending Score (1-100)'] > 100)).sum()
if out_of_range > 0:
    issue = f"Spending Score has {out_of_range} values outside 1-100 range"
    quality_issues.append(issue)
    print(f"  WARNING: {issue}")

# Check for zero values
for col in ['Age', 'Annual Income ($)', 'Family Size']:
    zero_count = (df[col] == 0).sum()
    if zero_count > 0:
        issue = f"{col} has {zero_count} zero values"
        quality_issues.append(issue)
        print(f"  NOTE: {issue}")

if not quality_issues:
    print("  No critical quality issues detected.")

# ============================================================
# PHASE 2: STATISTICAL ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("PHASE 2: STATISTICAL ANALYSIS")
print("=" * 70)

numeric_cols = ['Age', 'Annual Income ($)', 'Spending Score (1-100)', 'Work Experience', 'Family Size']

# Detailed descriptive statistics
print("\nDetailed Descriptive Statistics:")
for col in numeric_cols:
    data = df[col].dropna()
    print(f"\n  {col}:")
    print(f"    Count:    {len(data)}")
    print(f"    Mean:     {data.mean():.2f}")
    print(f"    Median:   {data.median():.2f}")
    print(f"    Std Dev:  {data.std():.2f}")
    print(f"    Min:      {data.min()}")
    print(f"    Max:      {data.max()}")
    print(f"    Q1 (25%): {data.quantile(0.25):.2f}")
    print(f"    Q3 (75%): {data.quantile(0.75):.2f}")
    print(f"    IQR:      {data.quantile(0.75) - data.quantile(0.25):.2f}")
    print(f"    Skewness: {data.skew():.4f}")
    print(f"    Kurtosis: {data.kurtosis():.4f}")

    # Shapiro-Wilk normality test (on sample if large)
    sample = data.sample(min(500, len(data)), random_state=42)
    stat_sw, p_sw = stats.shapiro(sample)
    print(f"    Shapiro-Wilk p-value: {p_sw:.6f} ({'Normal' if p_sw > 0.05 else 'Not Normal'})")

# Frequency distribution for categorical columns
print("\nFrequency Distribution - Gender:")
gender_counts = df['Gender'].value_counts()
for g, c in gender_counts.items():
    print(f"  {g}: {c} ({c/len(df)*100:.1f}%)")

print("\nFrequency Distribution - Profession:")
prof_counts = df['Profession'].value_counts()
for p, c in prof_counts.items():
    print(f"  {p}: {c} ({c/len(df)*100:.1f}%)")

# Correlation matrix
print("\nCorrelation Matrix (Pearson):")
corr_matrix = df[numeric_cols].corr()
print(corr_matrix.round(4).to_string())

# Spearman correlation
print("\nCorrelation Matrix (Spearman):")
spearman_corr = df[numeric_cols].corr(method='spearman')
print(spearman_corr.round(4).to_string())

# Identify significant correlations
print("\nSignificant Correlations (|r| > 0.1):")
for i in range(len(numeric_cols)):
    for j in range(i+1, len(numeric_cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.1:
            print(f"  {numeric_cols[i]} vs {numeric_cols[j]}: r = {r:.4f}")

# Outlier detection using IQR method
print("\nOutlier Detection (IQR Method):")
outlier_counts = {}
outlier_details = {}
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    outlier_counts[col] = len(outliers)
    outlier_details[col] = {
        'count': int(len(outliers)),
        'percentage': round(len(outliers) / len(df) * 100, 2),
        'Q1': float(Q1),
        'Q3': float(Q3),
        'IQR': float(IQR),
        'lower_bound': float(lower),
        'upper_bound': float(upper)
    }
    print(f"  {col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")
    print(f"    Bounds: [{lower:.2f}, {upper:.2f}]")
    if len(outliers) > 0:
        print(f"    Outlier range: [{outliers[col].min()}, {outliers[col].max()}]")

# ============================================================
# PHASE 3: PATTERN DISCOVERY
# ============================================================
print("\n" + "=" * 70)
print("PHASE 3: PATTERN DISCOVERY")
print("=" * 70)

# Age distribution patterns
print("\nAge Distribution Patterns:")
age_bins = [0, 20, 30, 40, 50, 60, 70, 80, 100]
age_labels = ['<20', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
age_dist = df['Age_Group'].value_counts().sort_index()
for group, count in age_dist.items():
    print(f"  {group}: {count} ({count/len(df)*100:.1f}%)")
print(f"  Most common age group: {age_dist.idxmax()} ({age_dist.max()} customers)")

# Income vs Spending Score relationship
print("\nIncome vs Spending Score:")
r_pearson, p_pearson = stats.pearsonr(df['Annual Income ($)'], df['Spending Score (1-100)'])
r_spearman, p_spearman = stats.spearmanr(df['Annual Income ($)'], df['Spending Score (1-100)'])
print(f"  Pearson r: {r_pearson:.4f} (p-value: {p_pearson:.6f})")
print(f"  Spearman rho: {r_spearman:.4f} (p-value: {p_spearman:.6f})")

# Income segments
income_bins = [0, 20000, 40000, 60000, 80000, 100000, 200000]
income_labels = ['<20K', '20K-40K', '40K-60K', '60K-80K', '80K-100K', '100K+']
df['Income_Group'] = pd.cut(df['Annual Income ($)'], bins=income_bins, labels=income_labels, right=False)
print("\n  Spending Score by Income Group:")
for group in income_labels:
    subset = df[df['Income_Group'] == group]
    if len(subset) > 0:
        print(f"    {group}: n={len(subset)}, mean_spending={subset['Spending Score (1-100)'].mean():.1f}, median_spending={subset['Spending Score (1-100)'].median():.1f}")

# Gender-based differences
print("\nGender-Based Differences:")
for gender in df['Gender'].unique():
    subset = df[df['Gender'] == gender]
    print(f"\n  {gender} (n={len(subset)}):")
    print(f"    Mean Income: ${subset['Annual Income ($)'].mean():,.0f}")
    print(f"    Median Income: ${subset['Annual Income ($)'].median():,.0f}")
    print(f"    Mean Spending Score: {subset['Spending Score (1-100)'].mean():.1f}")
    print(f"    Median Spending Score: {subset['Spending Score (1-100)'].median():.1f}")
    print(f"    Mean Age: {subset['Age'].mean():.1f}")

# Mann-Whitney U test for gender differences
male_income = df[df['Gender'] == 'Male']['Annual Income ($)']
female_income = df[df['Gender'] == 'Female']['Annual Income ($)']
u_stat, u_pval = stats.mannwhitneyu(male_income, female_income, alternative='two-sided')
print(f"\n  Mann-Whitney U Test (Income by Gender): U={u_stat:.0f}, p={u_pval:.6f}")
print(f"  {'Significant' if u_pval < 0.05 else 'Not significant'} difference at alpha=0.05")

male_spending = df[df['Gender'] == 'Male']['Spending Score (1-100)']
female_spending = df[df['Gender'] == 'Female']['Spending Score (1-100)']
u_stat2, u_pval2 = stats.mannwhitneyu(male_spending, female_spending, alternative='two-sided')
print(f"\n  Mann-Whitney U Test (Spending by Gender): U={u_stat2:.0f}, p={u_pval2:.6f}")
print(f"  {'Significant' if u_pval2 < 0.05 else 'Not significant'} difference at alpha=0.05")

# Profession-based patterns
print("\nProfession-Based Patterns:")
prof_stats = df.groupby('Profession').agg({
    'Annual Income ($)': ['mean', 'median', 'std'],
    'Spending Score (1-100)': ['mean', 'median', 'std'],
    'Age': ['mean'],
    'CustomerID': 'count'
}).round(2)
prof_stats.columns = ['Income_Mean', 'Income_Median', 'Income_Std',
                       'Spending_Mean', 'Spending_Median', 'Spending_Std',
                       'Age_Mean', 'Count']
prof_stats = prof_stats.sort_values('Income_Mean', ascending=False)
print(prof_stats.to_string())

# Kruskal-Wallis test for profession differences in income
prof_groups_income = [group['Annual Income ($)'].values for name, group in df.groupby('Profession')]
h_stat, h_pval = stats.kruskal(*prof_groups_income)
print(f"\n  Kruskal-Wallis Test (Income by Profession): H={h_stat:.2f}, p={h_pval:.6f}")
print(f"  {'Significant' if h_pval < 0.05 else 'Not significant'} difference at alpha=0.05")

# Family size impact on spending
print("\nFamily Size Impact on Spending:")
family_stats = df.groupby('Family Size').agg({
    'Spending Score (1-100)': ['mean', 'median', 'count'],
    'Annual Income ($)': ['mean']
}).round(2)
family_stats.columns = ['Spending_Mean', 'Spending_Median', 'Count', 'Income_Mean']
print(family_stats.to_string())

r_family, p_family = stats.pearsonr(df['Family Size'].dropna(), df['Spending Score (1-100)'].dropna())
print(f"\n  Correlation (Family Size vs Spending): r={r_family:.4f}, p={p_family:.6f}")

# Work experience vs income
print("\nWork Experience vs Income:")
r_work, p_work = stats.pearsonr(df['Work Experience'].dropna(), df['Annual Income ($)'].dropna())
print(f"  Pearson r: {r_work:.4f} (p-value: {p_work:.6f})")

# Work experience bins
work_bins = [0, 2, 5, 10, 15, 20, 50]
work_labels = ['0-1yr', '2-4yr', '5-9yr', '10-14yr', '15-19yr', '20+yr']
df['Work_Group'] = pd.cut(df['Work Experience'], bins=work_bins, labels=work_labels, right=False)
work_stats = df.groupby('Work_Group').agg({
    'Annual Income ($)': ['mean', 'count'],
    'Spending Score (1-100)': ['mean']
}).round(2)
work_stats.columns = ['Income_Mean', 'Count', 'Spending_Mean']
print("\n  Income & Spending by Work Experience Group:")
print(work_stats.to_string())

# ============================================================
# PHASE 4: VISUALIZATIONS
# ============================================================
print("\n" + "=" * 70)
print("PHASE 4: GENERATING VISUALIZATIONS")
print("=" * 70)

# --- Plot 1: Age Distribution ---
print("\n  Creating: customers_age_distribution.png")
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)

# Histogram with KDE
axes[0].hist(df['Age'], bins=30, edgecolor='white', alpha=0.7, color='#4C72B0', density=True)
df['Age'].plot.kde(ax=axes[0], color='#C44E52', linewidth=2)
axes[0].set_xlabel('Age', fontsize=12)
axes[0].set_ylabel('Density', fontsize=12)
axes[0].set_title('Age Distribution (Histogram + KDE)', fontsize=14, fontweight='bold')
axes[0].axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=1.5, label=f'Mean: {df["Age"].mean():.1f}')
axes[0].axvline(df['Age'].median(), color='green', linestyle='--', linewidth=1.5, label=f'Median: {df["Age"].median():.1f}')
axes[0].legend(fontsize=10)

# Age group bar chart
age_counts = df['Age_Group'].value_counts().sort_index()
colors = sns.color_palette('husl', len(age_counts))
bars = axes[1].bar(range(len(age_counts)), age_counts.values, color=colors, edgecolor='white', linewidth=0.5)
axes[1].set_xticks(range(len(age_counts)))
axes[1].set_xticklabels(age_counts.index, fontsize=10)
axes[1].set_xlabel('Age Group', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].set_title('Customers by Age Group', fontsize=14, fontweight='bold')
for bar, val in zip(bars, age_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{VIZ_DIR}/customers_age_distribution.png', dpi=DPI, bbox_inches='tight')
plt.close()
print("    Done.")

# --- Plot 2: Income vs Spending Score ---
print("  Creating: customers_income_vs_spending.png")
fig, ax = plt.subplots(figsize=FIGSIZE)

gender_colors = {'Male': '#4C72B0', 'Female': '#DD8452'}
for gender, color in gender_colors.items():
    subset = df[df['Gender'] == gender]
    ax.scatter(subset['Annual Income ($)'], subset['Spending Score (1-100)'],
              c=color, alpha=0.5, s=40, label=gender, edgecolors='white', linewidth=0.3)

# Add trend line
z = np.polyfit(df['Annual Income ($)'], df['Spending Score (1-100)'], 1)
p = np.poly1d(z)
x_range = np.linspace(df['Annual Income ($)'].min(), df['Annual Income ($)'].max(), 100)
ax.plot(x_range, p(x_range), color='red', linewidth=2, linestyle='--', alpha=0.7,
        label=f'Trend (r={r_pearson:.3f})')

ax.set_xlabel('Annual Income ($)', fontsize=12)
ax.set_ylabel('Spending Score (1-100)', fontsize=12)
ax.set_title('Annual Income vs Spending Score by Gender', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)

# Add quadrant annotations
income_mid = df['Annual Income ($)'].median()
spending_mid = df['Spending Score (1-100)'].median()
ax.axhline(y=spending_mid, color='gray', linestyle=':', alpha=0.4)
ax.axvline(x=income_mid, color='gray', linestyle=':', alpha=0.4)

# Quadrant labels
ax.text(df['Annual Income ($)'].max() * 0.85, 95, 'High Income\nHigh Spending',
        fontsize=8, ha='center', alpha=0.6, style='italic')
ax.text(df['Annual Income ($)'].min() * 1.1 + 5000, 95, 'Low Income\nHigh Spending',
        fontsize=8, ha='center', alpha=0.6, style='italic')
ax.text(df['Annual Income ($)'].max() * 0.85, 5, 'High Income\nLow Spending',
        fontsize=8, ha='center', alpha=0.6, style='italic')
ax.text(df['Annual Income ($)'].min() * 1.1 + 5000, 5, 'Low Income\nLow Spending',
        fontsize=8, ha='center', alpha=0.6, style='italic')

plt.tight_layout()
plt.savefig(f'{VIZ_DIR}/customers_income_vs_spending.png', dpi=DPI, bbox_inches='tight')
plt.close()
print("    Done.")

# --- Plot 3: Correlation Heatmap ---
print("  Creating: customers_correlation_heatmap.png")
fig, ax = plt.subplots(figsize=(10, 8))

mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center='light', as_cmap=True)

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap=cmap, center=0,
            square=True, linewidths=1, linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'},
            ax=ax, vmin=-1, vmax=1, annot_kws={'size': 11, 'fontweight': 'bold'})

ax.set_title('Correlation Heatmap of Numerical Variables', fontsize=14, fontweight='bold', pad=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout()
plt.savefig(f'{VIZ_DIR}/customers_correlation_heatmap.png', dpi=DPI, bbox_inches='tight')
plt.close()
print("    Done.")

# --- Plot 4: Profession Analysis ---
print("  Creating: customers_profession_analysis.png")
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Profession count
prof_order = df['Profession'].value_counts().index
colors_prof = sns.color_palette('husl', len(prof_order))

sns.countplot(data=df, y='Profession', order=prof_order, ax=axes[0], palette=colors_prof)
axes[0].set_title('Profession Distribution', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Count', fontsize=11)
axes[0].set_ylabel('')
for i, v in enumerate(df['Profession'].value_counts()[prof_order].values):
    axes[0].text(v + 3, i, str(v), va='center', fontsize=9, fontweight='bold')

# Average income by profession
prof_income = df.groupby('Profession')['Annual Income ($)'].mean().sort_values(ascending=True)
bars = axes[1].barh(prof_income.index, prof_income.values, color=sns.color_palette('YlOrRd', len(prof_income)))
axes[1].set_title('Average Annual Income by Profession', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Average Annual Income ($)', fontsize=11)
axes[1].set_ylabel('')
for bar, val in zip(bars, prof_income.values):
    axes[1].text(val + 500, bar.get_y() + bar.get_height()/2, f'${val:,.0f}',
                va='center', fontsize=9, fontweight='bold')

# Average spending score by profession
prof_spending = df.groupby('Profession')['Spending Score (1-100)'].mean().sort_values(ascending=True)
bars2 = axes[2].barh(prof_spending.index, prof_spending.values, color=sns.color_palette('YlGnBu', len(prof_spending)))
axes[2].set_title('Average Spending Score by Profession', fontsize=13, fontweight='bold')
axes[2].set_xlabel('Average Spending Score', fontsize=11)
axes[2].set_ylabel('')
for bar, val in zip(bars2, prof_spending.values):
    axes[2].text(val + 0.3, bar.get_y() + bar.get_height()/2, f'{val:.1f}',
                va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{VIZ_DIR}/customers_profession_analysis.png', dpi=DPI, bbox_inches='tight')
plt.close()
print("    Done.")

# --- Plot 5: Gender Comparison ---
print("  Creating: customers_gender_comparison.png")
fig, axes = plt.subplots(2, 2, figsize=FIGSIZE)

# Income boxplot by gender
sns.boxplot(data=df, x='Gender', y='Annual Income ($)', ax=axes[0, 0],
            palette=gender_colors, width=0.5, fliersize=3)
axes[0, 0].set_title('Annual Income by Gender', fontsize=13, fontweight='bold')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('Annual Income ($)', fontsize=11)

# Spending boxplot by gender
sns.boxplot(data=df, x='Gender', y='Spending Score (1-100)', ax=axes[0, 1],
            palette=gender_colors, width=0.5, fliersize=3)
axes[0, 1].set_title('Spending Score by Gender', fontsize=13, fontweight='bold')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('Spending Score (1-100)', fontsize=11)

# Income violin plot by gender
sns.violinplot(data=df, x='Gender', y='Annual Income ($)', ax=axes[1, 0],
               palette=gender_colors, inner='quartile', cut=0)
axes[1, 0].set_title('Income Distribution by Gender (Violin)', fontsize=13, fontweight='bold')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('Annual Income ($)', fontsize=11)

# Spending violin plot by gender
sns.violinplot(data=df, x='Gender', y='Spending Score (1-100)', ax=axes[1, 1],
               palette=gender_colors, inner='quartile', cut=0)
axes[1, 1].set_title('Spending Score Distribution by Gender (Violin)', fontsize=13, fontweight='bold')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('Spending Score (1-100)', fontsize=11)

# Add mean markers
for ax_row in axes:
    for ax in ax_row:
        ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{VIZ_DIR}/customers_gender_comparison.png', dpi=DPI, bbox_inches='tight')
plt.close()
print("    Done.")

# ============================================================
# PHASE 5: SAVE OUTPUT FILES
# ============================================================
print("\n" + "=" * 70)
print("PHASE 5: SAVING OUTPUT FILES")
print("=" * 70)

# --- File 1: Statistical Summary CSV ---
print("\n  Saving: statistical_summary_exploratory.csv")
stat_summary = df[numeric_cols].describe().T
stat_summary['skewness'] = df[numeric_cols].skew()
stat_summary['kurtosis'] = df[numeric_cols].kurtosis()
stat_summary['missing'] = df[numeric_cols].isnull().sum()
stat_summary['missing_pct'] = (df[numeric_cols].isnull().sum() / len(df) * 100).round(2)
stat_summary['iqr'] = stat_summary['75%'] - stat_summary['25%']
stat_summary.to_csv(f'{REPORT_DIR}/statistical_summary_exploratory.csv')
print("    Done.")

# --- File 2: Data Quality JSON ---
print("  Saving: data_quality_exploratory.json")

completeness_scores = {}
for col in df.columns:
    completeness_scores[col] = round((1 - df[col].isnull().sum() / len(df)) * 100, 2)

quality_json = {
    "dataset_overview": {
        "file_name": "Customers.csv",
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "column_names": list(df.columns[:8]),  # original columns only
        "data_types": {col: str(df[col].dtype) for col in df.columns[:8]},
    },
    "missing_values": {
        "total_missing": int(total_missing),
        "by_column": {col: {"count": int(missing[col]), "percentage": float(missing_pct[col])}
                     for col in df.columns[:8]}
    },
    "duplicates": {
        "full_row_duplicates": int(full_duplicates),
        "customer_id_duplicates": int(id_duplicates)
    },
    "outliers_iqr": outlier_details,
    "completeness_scores": completeness_scores,
    "overall_quality_score": round(
        np.mean([
            100 - (total_missing / (df.shape[0] * df.shape[1]) * 100),  # completeness
            100 - (full_duplicates / df.shape[0] * 100),                 # uniqueness
            100 - (sum(outlier_counts.values()) / (len(df) * len(numeric_cols)) * 100),  # outlier ratio
            100 if not quality_issues else max(0, 100 - len(quality_issues) * 10)  # validity
        ]), 2
    ),
    "quality_issues": quality_issues if quality_issues else ["No critical quality issues detected"],
    "statistical_tests": {
        "income_spending_pearson_r": round(float(r_pearson), 4),
        "income_spending_pearson_p": round(float(p_pearson), 6),
        "gender_income_mannwhitney_p": round(float(u_pval), 6),
        "gender_spending_mannwhitney_p": round(float(u_pval2), 6),
        "profession_income_kruskal_p": round(float(h_pval), 6),
        "family_spending_pearson_r": round(float(r_family), 4),
        "work_income_pearson_r": round(float(r_work), 4)
    }
}

with open(f'{REPORT_DIR}/data_quality_exploratory.json', 'w') as f:
    json.dump(quality_json, f, indent=2)
print("    Done.")

# --- File 3: Comprehensive Markdown Report ---
print("  Saving: analysis_summary_exploratory.md")

# Compute additional metrics for the report
top_profession_income = prof_stats.sort_values('Income_Mean', ascending=False).head(3)
top_profession_spending = prof_stats.sort_values('Spending_Mean', ascending=False).head(3)

# Strong correlations for the report
strong_corrs = []
for i in range(len(numeric_cols)):
    for j in range(i+1, len(numeric_cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.05:
            strong_corrs.append((numeric_cols[i], numeric_cols[j], r))
strong_corrs.sort(key=lambda x: abs(x[2]), reverse=True)

report_md = f"""# Comprehensive Exploratory Data Analysis Report
## Customers Dataset

**Analysis Date**: 2026-02-06
**Dataset**: Customers.csv
**Analyst**: Claude Data Analysis Assistant

---

## Executive Summary

This report presents a comprehensive exploratory data analysis of the Customers dataset containing **{len(df):,} records** across **{df.shape[1]} variables**. The dataset captures customer demographics, income, spending behavior, professional background, and family characteristics.

### Key Findings at a Glance

1. **Data Quality**: The dataset is {'clean with no missing values' if total_missing == 0 else f'mostly complete with {total_missing} missing values'}. {full_duplicates} duplicate rows were found. Overall quality score: **{quality_json["overall_quality_score"]}/100**.

2. **Customer Profile**: The average customer is **{df['Age'].mean():.0f} years old**, earns **${df['Annual Income ($)'].mean():,.0f}/year**, has a spending score of **{df['Spending Score (1-100)'].mean():.0f}/100**, and has **{df['Family Size'].mean():.1f} family members**.

3. **Income-Spending Relationship**: There is a {'very weak' if abs(r_pearson) < 0.1 else 'weak' if abs(r_pearson) < 0.3 else 'moderate' if abs(r_pearson) < 0.5 else 'strong'} correlation (r={r_pearson:.3f}) between annual income and spending score, suggesting that **income alone does not strongly predict spending behavior**.

4. **Gender Differences**: {'No statistically significant difference' if u_pval > 0.05 else 'Statistically significant difference'} in income between genders (p={u_pval:.4f}). {'No statistically significant difference' if u_pval2 > 0.05 else 'Statistically significant difference'} in spending scores between genders (p={u_pval2:.4f}).

5. **Profession Impact**: {'Significant' if h_pval < 0.05 else 'No significant'} differences in income across professions (Kruskal-Wallis p={h_pval:.4f}).

---

## 1. Data Overview

### 1.1 Dataset Structure

| Property | Value |
|----------|-------|
| Total Records | {len(df):,} |
| Total Columns | {df.shape[1]} |
| Numerical Columns | {len(numeric_cols)} |
| Categorical Columns | {len(df.select_dtypes(include='object').columns)} |
| Memory Usage | {df.memory_usage(deep=True).sum() / 1024:.1f} KB |

### 1.2 Column Description

| Column | Data Type | Non-Null Count | Unique Values |
|--------|-----------|----------------|---------------|
| CustomerID | int64 | {df['CustomerID'].notna().sum()} | {df['CustomerID'].nunique()} |
| Gender | object | {df['Gender'].notna().sum()} | {df['Gender'].nunique()} |
| Age | int64 | {df['Age'].notna().sum()} | {df['Age'].nunique()} |
| Annual Income ($) | int64 | {df['Annual Income ($)'].notna().sum()} | {df['Annual Income ($)'].nunique()} |
| Spending Score (1-100) | int64 | {df['Spending Score (1-100)'].notna().sum()} | {df['Spending Score (1-100)'].nunique()} |
| Profession | object | {df['Profession'].notna().sum()} | {df['Profession'].nunique()} |
| Work Experience | int64 | {df['Work Experience'].notna().sum()} | {df['Work Experience'].nunique()} |
| Family Size | int64 | {df['Family Size'].notna().sum()} | {df['Family Size'].nunique()} |

### 1.3 Data Quality Assessment

| Metric | Score |
|--------|-------|
| Overall Quality Score | {quality_json["overall_quality_score"]}/100 |
| Total Missing Values | {total_missing} |
| Duplicate Rows | {full_duplicates} |
| CustomerID Duplicates | {id_duplicates} |
| Total Outliers (IQR) | {sum(outlier_counts.values())} across {len(numeric_cols)} variables |

**Quality Issues Identified:**
"""

if quality_issues:
    for issue in quality_issues:
        report_md += f"- {issue}\n"
else:
    report_md += "- No critical quality issues detected\n"

report_md += f"""
---

## 2. Descriptive Statistics

### 2.1 Numerical Variables

| Statistic | Age | Annual Income ($) | Spending Score | Work Experience | Family Size |
|-----------|-----|-------------------|----------------|-----------------|-------------|
| Count | {len(df)} | {len(df)} | {len(df)} | {len(df)} | {len(df)} |
| Mean | {df['Age'].mean():.1f} | {df['Annual Income ($)'].mean():,.0f} | {df['Spending Score (1-100)'].mean():.1f} | {df['Work Experience'].mean():.1f} | {df['Family Size'].mean():.1f} |
| Median | {df['Age'].median():.1f} | {df['Annual Income ($)'].median():,.0f} | {df['Spending Score (1-100)'].median():.1f} | {df['Work Experience'].median():.1f} | {df['Family Size'].median():.1f} |
| Std Dev | {df['Age'].std():.1f} | {df['Annual Income ($)'].std():,.0f} | {df['Spending Score (1-100)'].std():.1f} | {df['Work Experience'].std():.1f} | {df['Family Size'].std():.1f} |
| Min | {df['Age'].min()} | {df['Annual Income ($)'].min():,} | {df['Spending Score (1-100)'].min()} | {df['Work Experience'].min()} | {df['Family Size'].min()} |
| 25th Pctl | {df['Age'].quantile(0.25):.0f} | {df['Annual Income ($)'].quantile(0.25):,.0f} | {df['Spending Score (1-100)'].quantile(0.25):.0f} | {df['Work Experience'].quantile(0.25):.0f} | {df['Family Size'].quantile(0.25):.0f} |
| 75th Pctl | {df['Age'].quantile(0.75):.0f} | {df['Annual Income ($)'].quantile(0.75):,.0f} | {df['Spending Score (1-100)'].quantile(0.75):.0f} | {df['Work Experience'].quantile(0.75):.0f} | {df['Family Size'].quantile(0.75):.0f} |
| Max | {df['Age'].max()} | {df['Annual Income ($)'].max():,} | {df['Spending Score (1-100)'].max()} | {df['Work Experience'].max()} | {df['Family Size'].max()} |
| Skewness | {df['Age'].skew():.3f} | {df['Annual Income ($)'].skew():.3f} | {df['Spending Score (1-100)'].skew():.3f} | {df['Work Experience'].skew():.3f} | {df['Family Size'].skew():.3f} |
| Kurtosis | {df['Age'].kurtosis():.3f} | {df['Annual Income ($)'].kurtosis():.3f} | {df['Spending Score (1-100)'].kurtosis():.3f} | {df['Work Experience'].kurtosis():.3f} | {df['Family Size'].kurtosis():.3f} |

### 2.2 Distribution Characteristics

"""

for col in numeric_cols:
    skew = df[col].skew()
    kurt = df[col].kurtosis()
    skew_desc = "approximately symmetric" if abs(skew) < 0.5 else ("right-skewed" if skew > 0 else "left-skewed")
    kurt_desc = "mesokurtic (normal-like)" if abs(kurt) < 1 else ("leptokurtic (heavy-tailed)" if kurt > 0 else "platykurtic (light-tailed)")
    report_md += f"- **{col}**: {skew_desc} (skew={skew:.3f}), {kurt_desc} (kurtosis={kurt:.3f})\n"

report_md += f"""
### 2.3 Categorical Variables

#### Gender Distribution

| Gender | Count | Percentage |
|--------|-------|------------|
"""
for g in df['Gender'].value_counts().index:
    c = df['Gender'].value_counts()[g]
    report_md += f"| {g} | {c:,} | {c/len(df)*100:.1f}% |\n"

report_md += f"""
#### Profession Distribution

| Profession | Count | Percentage | Avg Income | Avg Spending Score |
|------------|-------|------------|------------|-------------------|
"""
for prof in prof_counts.index:
    c = prof_counts[prof]
    avg_inc = df[df['Profession'] == prof]['Annual Income ($)'].mean()
    avg_sp = df[df['Profession'] == prof]['Spending Score (1-100)'].mean()
    report_md += f"| {prof} | {c:,} | {c/len(df)*100:.1f}% | ${avg_inc:,.0f} | {avg_sp:.1f} |\n"

report_md += f"""
---

## 3. Correlation Analysis

### 3.1 Pearson Correlation Matrix

| Variable | Age | Income | Spending | Work Exp | Family Size |
|----------|-----|--------|----------|----------|-------------|
"""
for col1 in numeric_cols:
    row = f"| {col1.split('(')[0].strip()} |"
    for col2 in numeric_cols:
        r = corr_matrix.loc[col1, col2]
        row += f" {r:.3f} |"
    report_md += row + "\n"

report_md += f"""
### 3.2 Notable Correlations

"""
for c1, c2, r in strong_corrs[:10]:
    strength = "very weak" if abs(r) < 0.1 else "weak" if abs(r) < 0.3 else "moderate" if abs(r) < 0.5 else "strong"
    direction = "positive" if r > 0 else "negative"
    report_md += f"- **{c1}** vs **{c2}**: r = {r:.4f} ({strength} {direction})\n"

report_md += f"""
### 3.3 Key Statistical Tests

| Test | Variables | Statistic | p-value | Significant (alpha=0.05) |
|------|-----------|-----------|---------|--------------------------|
| Pearson Correlation | Income vs Spending | r = {r_pearson:.4f} | {p_pearson:.6f} | {'Yes' if p_pearson < 0.05 else 'No'} |
| Mann-Whitney U | Income by Gender | U = {u_stat:.0f} | {u_pval:.6f} | {'Yes' if u_pval < 0.05 else 'No'} |
| Mann-Whitney U | Spending by Gender | U = {u_stat2:.0f} | {u_pval2:.6f} | {'Yes' if u_pval2 < 0.05 else 'No'} |
| Kruskal-Wallis | Income by Profession | H = {h_stat:.2f} | {h_pval:.6f} | {'Yes' if h_pval < 0.05 else 'No'} |
| Pearson Correlation | Family Size vs Spending | r = {r_family:.4f} | {p_family:.6f} | {'Yes' if p_family < 0.05 else 'No'} |
| Pearson Correlation | Work Exp vs Income | r = {r_work:.4f} | {p_work:.6f} | {'Yes' if p_work < 0.05 else 'No'} |

---

## 4. Outlier Analysis (IQR Method)

| Variable | Outliers | % of Data | Lower Bound | Upper Bound |
|----------|----------|-----------|-------------|-------------|
"""
for col in numeric_cols:
    d = outlier_details[col]
    report_md += f"| {col} | {d['count']} | {d['percentage']}% | {d['lower_bound']:.0f} | {d['upper_bound']:.0f} |\n"

report_md += f"""
---

## 5. Pattern Discovery & Key Insights

### 5.1 Age Distribution Patterns

The customer base spans ages {df['Age'].min()} to {df['Age'].max()} with a mean age of {df['Age'].mean():.1f} years. The distribution is {('approximately symmetric' if abs(df['Age'].skew()) < 0.5 else 'right-skewed' if df['Age'].skew() > 0 else 'left-skewed')} (skew = {df['Age'].skew():.3f}).

**Age Group Breakdown:**

| Age Group | Count | Percentage |
|-----------|-------|------------|
"""
for group in age_dist.index:
    c = age_dist[group]
    report_md += f"| {group} | {c:,} | {c/len(df)*100:.1f}% |\n"

report_md += f"""
The largest age group is **{age_dist.idxmax()}** with {age_dist.max()} customers ({age_dist.max()/len(df)*100:.1f}%).

### 5.2 Income vs Spending Score Relationship

The correlation between annual income and spending score is **r = {r_pearson:.3f}** (p = {p_pearson:.4f}), indicating a {'very weak' if abs(r_pearson) < 0.1 else 'weak' if abs(r_pearson) < 0.3 else 'moderate' if abs(r_pearson) < 0.5 else 'strong'} {'positive' if r_pearson > 0 else 'negative'} relationship. This means that income level {'is not a reliable predictor of' if abs(r_pearson) < 0.3 else 'has some predictive power over'} spending behavior.

**Spending Score by Income Group:**

| Income Group | Count | Mean Spending | Median Spending |
|--------------|-------|---------------|-----------------|
"""
for group in income_labels:
    subset = df[df['Income_Group'] == group]
    if len(subset) > 0:
        report_md += f"| {group} | {len(subset)} | {subset['Spending Score (1-100)'].mean():.1f} | {subset['Spending Score (1-100)'].median():.1f} |\n"

report_md += f"""
### 5.3 Gender-Based Differences

| Metric | Male | Female | Difference |
|--------|------|--------|------------|
| Count | {len(df[df['Gender']=='Male'])} | {len(df[df['Gender']=='Female'])} | - |
| Mean Income | ${df[df['Gender']=='Male']['Annual Income ($)'].mean():,.0f} | ${df[df['Gender']=='Female']['Annual Income ($)'].mean():,.0f} | ${abs(df[df['Gender']=='Male']['Annual Income ($)'].mean() - df[df['Gender']=='Female']['Annual Income ($)'].mean()):,.0f} |
| Mean Spending | {df[df['Gender']=='Male']['Spending Score (1-100)'].mean():.1f} | {df[df['Gender']=='Female']['Spending Score (1-100)'].mean():.1f} | {abs(df[df['Gender']=='Male']['Spending Score (1-100)'].mean() - df[df['Gender']=='Female']['Spending Score (1-100)'].mean()):.1f} |
| Mean Age | {df[df['Gender']=='Male']['Age'].mean():.1f} | {df[df['Gender']=='Female']['Age'].mean():.1f} | {abs(df[df['Gender']=='Male']['Age'].mean() - df[df['Gender']=='Female']['Age'].mean()):.1f} |

**Statistical Significance**: Income difference is {'statistically significant' if u_pval < 0.05 else 'not statistically significant'} (Mann-Whitney p={u_pval:.4f}). Spending score difference is {'statistically significant' if u_pval2 < 0.05 else 'not statistically significant'} (Mann-Whitney p={u_pval2:.4f}).

### 5.4 Profession-Based Patterns

**Top 3 Professions by Average Income:**
"""
for idx, (prof, row) in enumerate(top_profession_income.iterrows(), 1):
    report_md += f"{idx}. **{prof}**: ${row['Income_Mean']:,.0f} avg income, {row['Spending_Mean']:.1f} avg spending score\n"

report_md += f"""
**Top 3 Professions by Average Spending Score:**
"""
for idx, (prof, row) in enumerate(top_profession_spending.iterrows(), 1):
    report_md += f"{idx}. **{prof}**: {row['Spending_Mean']:.1f} avg spending score, ${row['Income_Mean']:,.0f} avg income\n"

report_md += f"""
### 5.5 Family Size Impact

The correlation between family size and spending score is **r = {r_family:.4f}** (p = {p_family:.4f}), indicating {'no meaningful' if abs(r_family) < 0.1 else 'a weak' if abs(r_family) < 0.3 else 'a moderate'} relationship.

| Family Size | Count | Mean Spending | Mean Income |
|-------------|-------|---------------|-------------|
"""
for fam_size in sorted(df['Family Size'].dropna().unique()):
    subset = df[df['Family Size'] == fam_size]
    report_md += f"| {int(fam_size)} | {len(subset)} | {subset['Spending Score (1-100)'].mean():.1f} | ${subset['Annual Income ($)'].mean():,.0f} |\n"

report_md += f"""
### 5.6 Work Experience vs Income

The correlation between work experience and annual income is **r = {r_work:.4f}** (p = {p_work:.4f}), indicating {'no meaningful' if abs(r_work) < 0.1 else 'a weak' if abs(r_work) < 0.3 else 'a moderate'} relationship. This suggests that {'work experience alone does not predict income level' if abs(r_work) < 0.3 else 'more experienced workers tend to earn more'} in this dataset.

---

## 6. Visualizations Generated

The following publication-quality visualizations have been generated:

| File | Description |
|------|-------------|
| `customers_age_distribution.png` | Age distribution histogram with KDE and age group bar chart |
| `customers_income_vs_spending.png` | Scatter plot of income vs spending score, colored by gender, with trend line and quadrant annotations |
| `customers_correlation_heatmap.png` | Heatmap of Pearson correlations between all numerical variables |
| `customers_profession_analysis.png` | Three-panel analysis: profession distribution, average income, and average spending by profession |
| `customers_gender_comparison.png` | Four-panel gender comparison using boxplots and violin plots for income and spending |

All visualizations are saved in: `visualizations/`

---

## 7. Recommendations

### For Business Strategy
1. **Segment-Based Marketing**: Since income does not strongly predict spending, develop marketing strategies based on spending behavior segments rather than income levels alone.
2. **Profession Targeting**: Focus marketing efforts on high-spending professions to maximize ROI.
3. **Age-Group Campaigns**: The largest customer segment ({age_dist.idxmax()}) should receive tailored campaigns.
4. **Gender-Neutral Approach**: {'Since no significant gender differences exist in income or spending,' if (u_pval > 0.05 and u_pval2 > 0.05) else 'Given the observed gender differences,'} {'gender-neutral marketing strategies may be most effective.' if (u_pval > 0.05 and u_pval2 > 0.05) else 'consider gender-specific strategies.'}

### For Further Analysis
1. **Customer Segmentation**: Apply clustering algorithms (K-means, DBSCAN) on income and spending score to identify distinct customer segments.
2. **Predictive Modeling**: Build regression models to predict spending score using demographic features.
3. **Feature Engineering**: Create interaction features (e.g., income-per-family-member) for improved predictive power.
4. **Time Series Analysis**: If temporal data becomes available, track how customer behavior changes over time.
5. **Deep Dive on Outliers**: Investigate the {sum(outlier_counts.values())} identified outliers to determine if they represent special customer segments.

---

## 8. Methodology Notes

- **Statistical Tests**: Non-parametric tests (Mann-Whitney U, Kruskal-Wallis) were used for group comparisons as data distributions are not guaranteed to be normal.
- **Outlier Detection**: IQR method (1.5 x IQR below Q1 or above Q3) was applied to all numerical variables.
- **Correlation**: Both Pearson (linear) and Spearman (monotonic) correlations were computed.
- **Significance Level**: Alpha = 0.05 used for all hypothesis tests.

---

## Appendix: Output Files

| File | Location | Description |
|------|----------|-------------|
| `analysis_summary_exploratory.md` | `analysis_reports/` | This comprehensive report |
| `statistical_summary_exploratory.csv` | `analysis_reports/` | Full statistical summary table |
| `data_quality_exploratory.json` | `analysis_reports/` | Data quality metrics in JSON format |
| `customers_age_distribution.png` | `visualizations/` | Age distribution visualization |
| `customers_income_vs_spending.png` | `visualizations/` | Income vs spending scatter plot |
| `customers_correlation_heatmap.png` | `visualizations/` | Correlation heatmap |
| `customers_profession_analysis.png` | `visualizations/` | Profession analysis charts |
| `customers_gender_comparison.png` | `visualizations/` | Gender comparison charts |
"""

with open(f'{REPORT_DIR}/analysis_summary_exploratory.md', 'w') as f:
    f.write(report_md)
print("    Done.")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print(f"\nOutput Files Generated:")
print(f"  Reports:")
print(f"    - {REPORT_DIR}/analysis_summary_exploratory.md")
print(f"    - {REPORT_DIR}/statistical_summary_exploratory.csv")
print(f"    - {REPORT_DIR}/data_quality_exploratory.json")
print(f"  Visualizations:")
print(f"    - {VIZ_DIR}/customers_age_distribution.png")
print(f"    - {VIZ_DIR}/customers_income_vs_spending.png")
print(f"    - {VIZ_DIR}/customers_correlation_heatmap.png")
print(f"    - {VIZ_DIR}/customers_profession_analysis.png")
print(f"    - {VIZ_DIR}/customers_gender_comparison.png")
