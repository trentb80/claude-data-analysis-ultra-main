# Comprehensive Exploratory Data Analysis Report
## Customers Dataset

**Analysis Date**: 2026-02-06
**Dataset**: Customers.csv
**Analyst**: Claude Data Analysis Assistant

---

## Executive Summary

This report presents a comprehensive exploratory data analysis of the Customers dataset containing **2,000 records** across **11 variables**. The dataset captures customer demographics, income, spending behavior, professional background, and family characteristics.

### Key Findings at a Glance

1. **Data Quality**: The dataset is mostly complete with 35 missing values. 0 duplicate rows were found. Overall quality score: **92.45/100**.

2. **Customer Profile**: The average customer is **49 years old**, earns **$110,732/year**, has a spending score of **51/100**, and has **3.8 family members**.

3. **Income-Spending Relationship**: There is a very weak correlation (r=0.023) between annual income and spending score, suggesting that **income alone does not strongly predict spending behavior**.

4. **Gender Differences**: No statistically significant difference in income between genders (p=0.7564). No statistically significant difference in spending scores between genders (p=0.9667).

5. **Profession Impact**: No significant differences in income across professions (Kruskal-Wallis p=0.9341).

---

## 1. Data Overview

### 1.1 Dataset Structure

| Property | Value |
|----------|-------|
| Total Records | 2,000 |
| Total Columns | 11 |
| Numerical Columns | 5 |
| Categorical Columns | 2 |
| Memory Usage | 349.2 KB |

### 1.2 Column Description

| Column | Data Type | Non-Null Count | Unique Values |
|--------|-----------|----------------|---------------|
| CustomerID | int64 | 2000 | 2000 |
| Gender | object | 2000 | 2 |
| Age | int64 | 2000 | 100 |
| Annual Income ($) | int64 | 2000 | 1786 |
| Spending Score (1-100) | int64 | 2000 | 101 |
| Profession | object | 1965 | 9 |
| Work Experience | int64 | 2000 | 18 |
| Family Size | int64 | 2000 | 9 |

### 1.3 Data Quality Assessment

| Metric | Score |
|--------|-------|
| Overall Quality Score | 92.45/100 |
| Total Missing Values | 35 |
| Duplicate Rows | 0 |
| CustomerID Duplicates | 0 |
| Total Outliers (IQR) | 5 across 5 variables |

**Quality Issues Identified:**
- Spending Score has 2 values outside 1-100 range
- Age has 24 zero values
- Annual Income ($) has 2 zero values

---

## 2. Descriptive Statistics

### 2.1 Numerical Variables

| Statistic | Age | Annual Income ($) | Spending Score | Work Experience | Family Size |
|-----------|-----|-------------------|----------------|-----------------|-------------|
| Count | 2000 | 2000 | 2000 | 2000 | 2000 |
| Mean | 49.0 | 110,732 | 51.0 | 4.1 | 3.8 |
| Median | 48.0 | 110,045 | 50.0 | 3.0 | 4.0 |
| Std Dev | 28.4 | 45,740 | 27.9 | 3.9 | 2.0 |
| Min | 0 | 0 | 0 | 0 | 1 |
| 25th Pctl | 25 | 74,572 | 28 | 1 | 2 |
| 75th Pctl | 73 | 149,093 | 75 | 7 | 5 |
| Max | 99 | 189,974 | 100 | 17 | 9 |
| Skewness | 0.049 | -0.116 | 0.005 | 0.684 | 0.199 |
| Kurtosis | -1.169 | -0.843 | -1.101 | -0.467 | -1.163 |

### 2.2 Distribution Characteristics

- **Age**: approximately symmetric (skew=0.049), platykurtic (light-tailed) (kurtosis=-1.169)
- **Annual Income ($)**: approximately symmetric (skew=-0.116), mesokurtic (normal-like) (kurtosis=-0.843)
- **Spending Score (1-100)**: approximately symmetric (skew=0.005), platykurtic (light-tailed) (kurtosis=-1.101)
- **Work Experience**: right-skewed (skew=0.684), mesokurtic (normal-like) (kurtosis=-0.467)
- **Family Size**: approximately symmetric (skew=0.199), platykurtic (light-tailed) (kurtosis=-1.163)

### 2.3 Categorical Variables

#### Gender Distribution

| Gender | Count | Percentage |
|--------|-------|------------|
| Female | 1,186 | 59.3% |
| Male | 814 | 40.7% |

#### Profession Distribution

| Profession | Count | Percentage | Avg Income | Avg Spending Score |
|------------|-------|------------|------------|-------------------|
| Artist | 612 | 30.6% | $108,777 | 52.7 |
| Healthcare | 339 | 17.0% | $112,574 | 50.5 |
| Entertainment | 234 | 11.7% | $110,650 | 52.9 |
| Engineer | 179 | 8.9% | $111,161 | 49.0 |
| Doctor | 161 | 8.1% | $111,573 | 51.9 |
| Executive | 153 | 7.6% | $113,770 | 49.9 |
| Lawyer | 142 | 7.1% | $110,996 | 48.9 |
| Marketing | 85 | 4.2% | $107,994 | 48.7 |
| Homemaker | 60 | 3.0% | $108,759 | 46.4 |

---

## 3. Correlation Analysis

### 3.1 Pearson Correlation Matrix

| Variable | Age | Income | Spending | Work Exp | Family Size |
|----------|-----|--------|----------|----------|-------------|
| Age | 1.000 | 0.021 | -0.042 | -0.014 | 0.038 |
| Annual Income | 0.021 | 1.000 | 0.023 | 0.089 | 0.093 |
| Spending Score | -0.042 | 0.023 | 1.000 | -0.029 | 0.002 |
| Work Experience | -0.014 | 0.089 | -0.029 | 1.000 | 0.012 |
| Family Size | 0.038 | 0.093 | 0.002 | 0.012 | 1.000 |

### 3.2 Notable Correlations

- **Annual Income ($)** vs **Family Size**: r = 0.0930 (very weak positive)
- **Annual Income ($)** vs **Work Experience**: r = 0.0891 (very weak positive)

### 3.3 Key Statistical Tests

| Test | Variables | Statistic | p-value | Significant (alpha=0.05) |
|------|-----------|-----------|---------|--------------------------|
| Pearson Correlation | Income vs Spending | r = 0.0233 | 0.297657 | No |
| Mann-Whitney U | Income by Gender | U = 486639 | 0.756365 | No |
| Mann-Whitney U | Spending by Gender | U = 483232 | 0.966741 | No |
| Kruskal-Wallis | Income by Profession | H = 3.00 | 0.934118 | No |
| Pearson Correlation | Family Size vs Spending | r = 0.0022 | 0.920536 | No |
| Pearson Correlation | Work Exp vs Income | r = 0.0891 | 0.000066 | Yes |

---

## 4. Outlier Analysis (IQR Method)

| Variable | Outliers | % of Data | Lower Bound | Upper Bound |
|----------|----------|-----------|-------------|-------------|
| Age | 0 | 0.0% | -47 | 145 |
| Annual Income ($) | 0 | 0.0% | -37209 | 260874 |
| Spending Score (1-100) | 0 | 0.0% | -42 | 146 |
| Work Experience | 5 | 0.25% | -8 | 16 |
| Family Size | 0 | 0.0% | -2 | 10 |

---

## 5. Pattern Discovery & Key Insights

### 5.1 Age Distribution Patterns

The customer base spans ages 0 to 99 with a mean age of 49.0 years. The distribution is approximately symmetric (skew = 0.049).

**Age Group Breakdown:**

| Age Group | Count | Percentage |
|-----------|-------|------------|
| <20 | 380 | 19.0% |
| 20-29 | 211 | 10.5% |
| 30-39 | 241 | 12.0% |
| 40-49 | 195 | 9.8% |
| 50-59 | 202 | 10.1% |
| 60-69 | 210 | 10.5% |
| 70-79 | 167 | 8.3% |
| 80+ | 394 | 19.7% |

The largest age group is **80+** with 394 customers (19.7%).

### 5.2 Income vs Spending Score Relationship

The correlation between annual income and spending score is **r = 0.023** (p = 0.2977), indicating a very weak positive relationship. This means that income level is not a reliable predictor of spending behavior.

**Spending Score by Income Group:**

| Income Group | Count | Mean Spending | Median Spending |
|--------------|-------|---------------|-----------------|
| <20K | 54 | 49.5 | 47.5 |
| 20K-40K | 57 | 50.5 | 47.0 |
| 40K-60K | 166 | 51.7 | 52.5 |
| 60K-80K | 302 | 48.2 | 47.0 |
| 80K-100K | 303 | 50.4 | 49.0 |
| 100K+ | 1118 | 51.9 | 51.0 |

### 5.3 Gender-Based Differences

| Metric | Male | Female | Difference |
|--------|------|--------|------------|
| Count | 814 | 1186 | - |
| Mean Income | $110,991 | $110,554 | $438 |
| Mean Spending | 50.9 | 51.0 | 0.0 |
| Mean Age | 49.2 | 48.8 | 0.3 |

**Statistical Significance**: Income difference is not statistically significant (Mann-Whitney p=0.7564). Spending score difference is not statistically significant (Mann-Whitney p=0.9667).

### 5.4 Profession-Based Patterns

**Top 3 Professions by Average Income:**
1. **Executive**: $113,770 avg income, 49.9 avg spending score
2. **Healthcare**: $112,574 avg income, 50.5 avg spending score
3. **Doctor**: $111,573 avg income, 51.9 avg spending score

**Top 3 Professions by Average Spending Score:**
1. **Entertainment**: 52.9 avg spending score, $110,650 avg income
2. **Artist**: 52.7 avg spending score, $108,777 avg income
3. **Doctor**: 51.9 avg spending score, $111,573 avg income

### 5.5 Family Size Impact

The correlation between family size and spending score is **r = 0.0022** (p = 0.9205), indicating no meaningful relationship.

| Family Size | Count | Mean Spending | Mean Income |
|-------------|-------|---------------|-------------|
| 1 | 299 | 49.6 | $108,752 |
| 2 | 361 | 50.4 | $104,697 |
| 3 | 311 | 52.0 | $106,413 |
| 4 | 289 | 52.7 | $109,476 |
| 5 | 258 | 52.2 | $114,283 |
| 6 | 243 | 49.9 | $119,060 |
| 7 | 234 | 50.0 | $118,192 |
| 8 | 4 | 49.2 | $78,608 |
| 9 | 1 | 17.0 | $30,000 |

### 5.6 Work Experience vs Income

The correlation between work experience and annual income is **r = 0.0891** (p = 0.0001), indicating no meaningful relationship. This suggests that work experience alone does not predict income level in this dataset.

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
3. **Age-Group Campaigns**: The largest customer segment (80+) should receive tailored campaigns.
4. **Gender-Neutral Approach**: Since no significant gender differences exist in income or spending, gender-neutral marketing strategies may be most effective.

### For Further Analysis
1. **Customer Segmentation**: Apply clustering algorithms (K-means, DBSCAN) on income and spending score to identify distinct customer segments.
2. **Predictive Modeling**: Build regression models to predict spending score using demographic features.
3. **Feature Engineering**: Create interaction features (e.g., income-per-family-member) for improved predictive power.
4. **Time Series Analysis**: If temporal data becomes available, track how customer behavior changes over time.
5. **Deep Dive on Outliers**: Investigate the 5 identified outliers to determine if they represent special customer segments.

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
