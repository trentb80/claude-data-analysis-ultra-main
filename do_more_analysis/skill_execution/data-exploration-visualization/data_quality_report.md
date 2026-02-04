# Data Quality Assessment Report
**Generated**: 2026-02-04 18:37:58

## Executive Summary

This report provides a comprehensive assessment of data quality across all 8 datasets in the Olist e-commerce platform.

## Dataset Overview

| Dataset | Records | Fields | Size (MB) | Completeness |
|---------|---------|--------|-----------|--------------|
| Orders | 99,441 | 8 | 56.88 | 99.38% |
| Customers | 99,441 | 5 | 29.62 | 100.00% |
| Order_items | 112,650 | 7 | 39.43 | 100.00% |
| Payments | 103,886 | 5 | 17.81 | 100.00% |
| Reviews | 99,224 | 7 | 42.74 | 78.99% |
| Products | 32,951 | 9 | 6.79 | 99.17% |
| Sellers | 3,095 | 4 | 0.66 | 100.00% |
| Categories | 71 | 2 | 0.01 | 100.00% |

## Data Quality Metrics by Dataset

### ORDERS

**Overview:**
- Total Records: 99,441
- Total Fields: 8
- Completeness Score: 99.38%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 56.88 MB

**Missing Values:**

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| order_approved_at | 160 | 0.16% |
| order_delivered_carrier_date | 1,783 | 1.79% |
| order_delivered_customer_date | 2,965 | 2.98% |

### CUSTOMERS

**Overview:**
- Total Records: 99,441
- Total Fields: 5
- Completeness Score: 100.00%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 29.62 MB

**Missing Values:** None detected

### ORDER_ITEMS

**Overview:**
- Total Records: 112,650
- Total Fields: 7
- Completeness Score: 100.00%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 39.43 MB

**Missing Values:** None detected

### PAYMENTS

**Overview:**
- Total Records: 103,886
- Total Fields: 5
- Completeness Score: 100.00%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 17.81 MB

**Missing Values:** None detected

### REVIEWS

**Overview:**
- Total Records: 99,224
- Total Fields: 7
- Completeness Score: 78.99%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 42.74 MB

**Missing Values:**

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| review_comment_title | 87,656 | 88.34% |
| review_comment_message | 58,247 | 58.70% |

### PRODUCTS

**Overview:**
- Total Records: 32,951
- Total Fields: 9
- Completeness Score: 99.17%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 6.79 MB

**Missing Values:**

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| product_category_name | 610 | 1.85% |
| product_name_lenght | 610 | 1.85% |
| product_description_lenght | 610 | 1.85% |
| product_photos_qty | 610 | 1.85% |
| product_weight_g | 2 | 0.01% |
| product_length_cm | 2 | 0.01% |
| product_height_cm | 2 | 0.01% |
| product_width_cm | 2 | 0.01% |

### SELLERS

**Overview:**
- Total Records: 3,095
- Total Fields: 4
- Completeness Score: 100.00%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 0.66 MB

**Missing Values:** None detected

### CATEGORIES

**Overview:**
- Total Records: 71
- Total Fields: 2
- Completeness Score: 100.00%
- Duplicate Rows: 0 (0.00%)
- Memory Usage: 0.01 MB

**Missing Values:** None detected

## Quality Assessment Summary

**Key Findings:**

- Average Completeness Across All Datasets: 97.19%
- Total Duplicate Rows Across All Datasets: 0
- Datasets with Missing Values: 3/8

**Recommendations:**

- Implement data validation rules at the data entry point
- Establish regular data quality monitoring procedures
