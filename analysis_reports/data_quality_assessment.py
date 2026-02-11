"""
Data Quality Assessment Script
Target: /home/user/claude-data-analysis-ultra-main/data_storage/Customers.csv
Output: /home/user/claude-data-analysis-ultra-main/analysis_reports/data_quality_exploratory.json
"""

import pandas as pd
import numpy as np
import json
import os
from collections import OrderedDict

# ============================================================
# 1. Load the CSV file
# ============================================================
DATA_PATH = "/home/user/claude-data-analysis-ultra-main/data_storage/Customers.csv"
OUTPUT_PATH = "/home/user/claude-data-analysis-ultra-main/analysis_reports/data_quality_exploratory.json"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("DATA QUALITY ASSESSMENT REPORT")
print(f"Dataset: Customers.csv")
print(f"Records: {len(df)} rows, {len(df.columns)} columns")
print("=" * 70)

# ============================================================
# 2a. Missing Values Per Column
# ============================================================
print("\n--- MISSING VALUES ---")
missing_info = {}
for col in df.columns:
    missing_count = int(df[col].isnull().sum())
    missing_pct = round(missing_count / len(df) * 100, 2)
    missing_info[col] = {
        "missing_count": missing_count,
        "missing_percentage": missing_pct,
        "non_null_count": int(len(df) - missing_count)
    }
    print(f"  {col:30s}: {missing_count:5d} missing ({missing_pct:.2f}%)")

total_cells = len(df) * len(df.columns)
total_missing = int(df.isnull().sum().sum())
overall_completeness = round((1 - total_missing / total_cells) * 100, 2)
print(f"\n  Total cells: {total_cells}, Total missing: {total_missing}")
print(f"  Overall completeness: {overall_completeness}%")

# ============================================================
# 2b. Duplicate Rows
# ============================================================
print("\n--- DUPLICATE ROWS ---")
full_duplicates = int(df.duplicated().sum())
id_duplicates = int(df["CustomerID"].duplicated().sum())
print(f"  Full row duplicates: {full_duplicates}")
print(f"  Duplicate CustomerIDs: {id_duplicates}")

duplicate_info = {
    "full_row_duplicates": full_duplicates,
    "duplicate_customer_ids": id_duplicates,
    "unique_customer_ids": int(df["CustomerID"].nunique()),
    "total_rows": len(df)
}

# ============================================================
# 2c. Data Type Consistency
# ============================================================
print("\n--- DATA TYPE CONSISTENCY ---")

expected_types = {
    "CustomerID": {"expected": "integer", "actual": str(df["CustomerID"].dtype)},
    "Gender": {"expected": "string/categorical", "actual": str(df["Gender"].dtype)},
    "Age": {"expected": "integer/float", "actual": str(df["Age"].dtype)},
    "Annual Income ($)": {"expected": "integer/float", "actual": str(df["Annual Income ($)"].dtype)},
    "Spending Score (1-100)": {"expected": "integer/float", "actual": str(df["Spending Score (1-100)"].dtype)},
    "Profession": {"expected": "string/categorical", "actual": str(df["Profession"].dtype)},
    "Work Experience": {"expected": "integer/float", "actual": str(df["Work Experience"].dtype)},
    "Family Size": {"expected": "integer/float", "actual": str(df["Family Size"].dtype)}
}

dtype_issues = []
for col, info in expected_types.items():
    actual = info["actual"]
    expected = info["expected"]
    is_consistent = False
    if "integer" in expected and ("int" in actual or "float" in actual):
        is_consistent = True
    elif "float" in expected and ("float" in actual or "int" in actual):
        is_consistent = True
    elif "string" in expected and ("object" in actual or "str" in actual or "string" in actual.lower()):
        is_consistent = True
    info["is_consistent"] = is_consistent
    status = "OK" if is_consistent else "ISSUE"
    print(f"  {col:30s}: expected={expected:20s} actual={actual:10s} [{status}]")
    if not is_consistent:
        dtype_issues.append(col)

dtype_consistency_rate = round((len(expected_types) - len(dtype_issues)) / len(expected_types) * 100, 2)
print(f"\n  Data type consistency rate: {dtype_consistency_rate}%")
if dtype_issues:
    print(f"  Columns with type issues: {dtype_issues}")

# ============================================================
# 2d. Value Range Validation
# ============================================================
print("\n--- VALUE RANGE VALIDATION ---")

range_rules = {
    "CustomerID": {"min": 1, "max": None, "description": "Positive integer ID"},
    "Age": {"min": 0, "max": 130, "description": "Reasonable human age (0-130)"},
    "Annual Income ($)": {"min": 0, "max": None, "description": "Non-negative income"},
    "Spending Score (1-100)": {"min": 1, "max": 100, "description": "Score between 1 and 100"},
    "Work Experience": {"min": 0, "max": 70, "description": "Non-negative, reasonable years"},
    "Family Size": {"min": 1, "max": 20, "description": "Positive family size (1-20)"}
}

range_results = {}
total_valid_range = 0
total_checked_range = 0

for col, rules in range_rules.items():
    col_data = df[col].dropna()
    total_records = len(col_data)
    violations = []

    if rules["min"] is not None:
        below_min = col_data[col_data < rules["min"]]
        if len(below_min) > 0:
            violations.append({
                "type": "below_minimum",
                "threshold": rules["min"],
                "count": int(len(below_min)),
                "examples": below_min.head(5).tolist()
            })

    if rules["max"] is not None:
        above_max = col_data[col_data > rules["max"]]
        if len(above_max) > 0:
            violations.append({
                "type": "above_maximum",
                "threshold": rules["max"],
                "count": int(len(above_max)),
                "examples": above_max.head(5).tolist()
            })

    violation_count = sum(v["count"] for v in violations)
    valid_count = total_records - violation_count
    validity_rate = round(valid_count / total_records * 100, 2) if total_records > 0 else 100.0

    range_results[col] = {
        "rule_description": rules["description"],
        "total_checked": total_records,
        "valid_count": int(valid_count),
        "violation_count": int(violation_count),
        "validity_rate": validity_rate,
        "violations": violations,
        "statistics": {
            "min": float(col_data.min()) if len(col_data) > 0 else None,
            "max": float(col_data.max()) if len(col_data) > 0 else None,
            "mean": round(float(col_data.mean()), 2) if len(col_data) > 0 else None,
            "median": float(col_data.median()) if len(col_data) > 0 else None,
            "std": round(float(col_data.std()), 2) if len(col_data) > 0 else None
        }
    }

    total_valid_range += valid_count
    total_checked_range += total_records

    status = "PASS" if violation_count == 0 else "FAIL"
    print(f"  {col:30s}: {validity_rate:6.2f}% valid | "
          f"min={col_data.min()}, max={col_data.max()}, "
          f"violations={violation_count} [{status}]")

overall_validity = round(total_valid_range / total_checked_range * 100, 2) if total_checked_range > 0 else 100.0
print(f"\n  Overall value validity rate: {overall_validity}%")

# ============================================================
# 2e. Outlier Detection (IQR Method)
# ============================================================
print("\n--- OUTLIER DETECTION (IQR METHOD) ---")

numerical_cols = ["Age", "Annual Income ($)", "Spending Score (1-100)", "Work Experience", "Family Size"]
outlier_results = {}

for col in numerical_cols:
    col_data = df[col].dropna()
    Q1 = float(col_data.quantile(0.25))
    Q3 = float(col_data.quantile(0.75))
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = (col_data < lower_bound) | (col_data > upper_bound)
    outlier_count = int(outlier_mask.sum())
    outlier_pct = round(outlier_count / len(col_data) * 100, 2) if len(col_data) > 0 else 0.0

    outlier_values = col_data[outlier_mask].tolist()
    # Limit stored examples
    outlier_examples = sorted(outlier_values)[:10] if outlier_values else []

    outlier_results[col] = {
        "Q1": round(Q1, 2),
        "Q3": round(Q3, 2),
        "IQR": round(IQR, 2),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "outlier_count": outlier_count,
        "outlier_percentage": outlier_pct,
        "total_checked": int(len(col_data)),
        "outlier_examples": [float(x) for x in outlier_examples]
    }

    status = "CLEAN" if outlier_count == 0 else f"{outlier_count} OUTLIERS"
    print(f"  {col:30s}: Q1={Q1:.1f}, Q3={Q3:.1f}, IQR={IQR:.1f}, "
          f"bounds=[{lower_bound:.1f}, {upper_bound:.1f}] -> {status} ({outlier_pct}%)")

# ============================================================
# 2f. Unique Value Counts for Categorical Columns
# ============================================================
print("\n--- CATEGORICAL COLUMN ANALYSIS ---")

categorical_cols = ["Gender", "Profession"]
categorical_results = {}

for col in categorical_cols:
    col_data = df[col].dropna()
    value_counts = col_data.value_counts()
    unique_count = int(col_data.nunique())

    categorical_results[col] = {
        "unique_values": unique_count,
        "value_distribution": {str(k): int(v) for k, v in value_counts.items()},
        "most_common": str(value_counts.index[0]) if len(value_counts) > 0 else None,
        "least_common": str(value_counts.index[-1]) if len(value_counts) > 0 else None,
        "non_null_count": int(len(col_data)),
        "null_count": int(df[col].isnull().sum())
    }

    print(f"\n  {col} ({unique_count} unique values):")
    for val, count in value_counts.items():
        pct = round(count / len(col_data) * 100, 1)
        print(f"    {str(val):20s}: {count:5d} ({pct}%)")

# ============================================================
# 2g. Anomalous Pattern Detection
# ============================================================
print("\n--- ANOMALOUS PATTERN DETECTION ---")

anomalies = []

# Check for negative values where unexpected
for col in ["Age", "Annual Income ($)", "Spending Score (1-100)", "Work Experience", "Family Size"]:
    col_data = df[col].dropna()
    neg_count = int((col_data < 0).sum())
    if neg_count > 0:
        anomalies.append({
            "type": "negative_values",
            "column": col,
            "count": neg_count,
            "description": f"{col} contains {neg_count} negative values"
        })
        print(f"  WARNING: {col} has {neg_count} negative values")

# Check for zero values where unexpected
for col in ["Age", "Family Size"]:
    col_data = df[col].dropna()
    zero_count = int((col_data == 0).sum())
    if zero_count > 0:
        anomalies.append({
            "type": "zero_values",
            "column": col,
            "count": zero_count,
            "description": f"{col} contains {zero_count} zero values which may be invalid"
        })
        print(f"  WARNING: {col} has {zero_count} zero values (potentially invalid)")

# Check for very high ages
age_data = df["Age"].dropna()
extreme_ages = age_data[age_data > 100]
if len(extreme_ages) > 0:
    anomalies.append({
        "type": "extreme_age",
        "column": "Age",
        "count": int(len(extreme_ages)),
        "description": f"Found {len(extreme_ages)} records with age > 100"
    })
    print(f"  WARNING: {len(extreme_ages)} records with age > 100")

# Check for inconsistency between age and work experience
if "Age" in df.columns and "Work Experience" in df.columns:
    valid_both = df.dropna(subset=["Age", "Work Experience"])
    impossible_exp = valid_both[valid_both["Work Experience"] > (valid_both["Age"] - 14)]
    if len(impossible_exp) > 0:
        anomalies.append({
            "type": "age_experience_inconsistency",
            "columns": ["Age", "Work Experience"],
            "count": int(len(impossible_exp)),
            "description": f"{len(impossible_exp)} records where work experience exceeds (age - 14)"
        })
        print(f"  WARNING: {len(impossible_exp)} records where work experience > (age - 14)")

# Check for unusual income values (e.g., income = 0)
income_data = df["Annual Income ($)"].dropna()
zero_income = int((income_data == 0).sum())
if zero_income > 0:
    anomalies.append({
        "type": "zero_income",
        "column": "Annual Income ($)",
        "count": zero_income,
        "description": f"{zero_income} records with zero income"
    })
    print(f"  WARNING: {zero_income} records with zero annual income")

# Check Gender values for unexpected entries
gender_vals = df["Gender"].dropna().unique()
expected_genders = {"Male", "Female"}
unexpected_genders = set(str(g) for g in gender_vals) - expected_genders
if unexpected_genders:
    anomalies.append({
        "type": "unexpected_gender_values",
        "column": "Gender",
        "values": list(unexpected_genders),
        "description": f"Unexpected gender values: {unexpected_genders}"
    })
    print(f"  WARNING: Unexpected gender values: {unexpected_genders}")

# Check Spending Score boundaries precisely
ss_data = df["Spending Score (1-100)"].dropna()
below_1 = int((ss_data < 1).sum())
above_100 = int((ss_data > 100).sum())
if below_1 > 0 or above_100 > 0:
    anomalies.append({
        "type": "spending_score_out_of_range",
        "column": "Spending Score (1-100)",
        "below_1": below_1,
        "above_100": above_100,
        "description": f"Spending score: {below_1} below 1, {above_100} above 100"
    })
    print(f"  WARNING: Spending Score out of range: {below_1} below 1, {above_100} above 100")

if not anomalies:
    print("  No major anomalous patterns detected.")
else:
    print(f"\n  Total anomalies detected: {len(anomalies)}")

# ============================================================
# 3. Calculate Data Quality Score (0-100)
# ============================================================
print("\n" + "=" * 70)
print("DATA QUALITY SCORE CALCULATION")
print("=" * 70)

# --- Completeness Score (weight: 30%) ---
completeness_score = overall_completeness
print(f"\n  [1] Completeness Score: {completeness_score:.2f}/100")
print(f"      (Based on % of non-null values across all cells)")

# --- Uniqueness Score (weight: 20%) ---
unique_ids = df["CustomerID"].nunique()
total_ids = len(df)
uniqueness_score = round((unique_ids / total_ids) * 100, 2)
print(f"\n  [2] Uniqueness Score: {uniqueness_score:.2f}/100")
print(f"      (Based on % unique CustomerIDs: {unique_ids}/{total_ids})")

# --- Validity Score (weight: 30%) ---
validity_score = overall_validity
print(f"\n  [3] Validity Score: {validity_score:.2f}/100")
print(f"      (Based on % values within expected ranges)")

# --- Consistency Score (weight: 20%) ---
consistency_score = dtype_consistency_rate
# Penalize for anomalies found
anomaly_penalty = min(len(anomalies) * 2, 20)  # Max 20 point penalty
consistency_score = max(0, consistency_score - anomaly_penalty)
print(f"\n  [4] Consistency Score: {consistency_score:.2f}/100")
print(f"      (Based on data type adherence: {dtype_consistency_rate}%, anomaly penalty: -{anomaly_penalty})")

# --- Weighted Overall Score ---
weights = {
    "completeness": 0.30,
    "uniqueness": 0.20,
    "validity": 0.30,
    "consistency": 0.20
}

overall_quality_score = round(
    completeness_score * weights["completeness"] +
    uniqueness_score * weights["uniqueness"] +
    validity_score * weights["validity"] +
    consistency_score * weights["consistency"],
    2
)

print(f"\n  OVERALL DATA QUALITY SCORE: {overall_quality_score:.2f}/100")
print(f"  Weights: Completeness={weights['completeness']:.0%}, "
      f"Uniqueness={weights['uniqueness']:.0%}, "
      f"Validity={weights['validity']:.0%}, "
      f"Consistency={weights['consistency']:.0%}")

# Quality grade
if overall_quality_score >= 95:
    grade = "EXCELLENT"
elif overall_quality_score >= 85:
    grade = "GOOD"
elif overall_quality_score >= 70:
    grade = "ACCEPTABLE"
elif overall_quality_score >= 50:
    grade = "NEEDS IMPROVEMENT"
else:
    grade = "POOR"

print(f"  Quality Grade: {grade}")

# ============================================================
# 4. Assemble and Save JSON Report
# ============================================================

quality_report = OrderedDict({
    "report_metadata": {
        "report_title": "Data Quality Assessment Report",
        "dataset": "Customers.csv",
        "dataset_path": DATA_PATH,
        "total_records": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "generated_by": "data_quality_assessment.py"
    },
    "missing_values": {
        "per_column": missing_info,
        "total_missing_cells": total_missing,
        "total_cells": total_cells,
        "overall_completeness_pct": overall_completeness
    },
    "duplicates": duplicate_info,
    "data_type_consistency": {
        "column_types": expected_types,
        "consistency_rate": dtype_consistency_rate,
        "columns_with_issues": dtype_issues
    },
    "value_range_validation": {
        "rules_applied": {k: v["description"] for k, v in range_rules.items()},
        "per_column_results": range_results,
        "overall_validity_rate": overall_validity
    },
    "outlier_detection": {
        "method": "IQR (1.5x interquartile range)",
        "per_column_results": outlier_results
    },
    "categorical_analysis": categorical_results,
    "anomalous_patterns": {
        "total_anomalies_found": len(anomalies),
        "details": anomalies
    },
    "quality_scores": {
        "completeness_score": completeness_score,
        "uniqueness_score": uniqueness_score,
        "validity_score": validity_score,
        "consistency_score": consistency_score,
        "weights": weights,
        "overall_quality_score": overall_quality_score,
        "quality_grade": grade
    },
    "recommendations": []
})

# Generate recommendations based on findings
recommendations = []

if overall_completeness < 100:
    cols_with_missing = [c for c, info in missing_info.items() if info["missing_count"] > 0]
    recommendations.append({
        "priority": "HIGH" if overall_completeness < 90 else "MEDIUM",
        "category": "Completeness",
        "issue": f"Missing values detected in {len(cols_with_missing)} column(s): {cols_with_missing}",
        "suggestion": "Investigate root cause of missing data. Consider imputation strategies "
                      "(mean/median for numerical, mode for categorical) or validate if missing values are intentional."
    })

if full_duplicates > 0:
    recommendations.append({
        "priority": "HIGH",
        "category": "Uniqueness",
        "issue": f"{full_duplicates} fully duplicate rows detected",
        "suggestion": "Remove exact duplicate rows. Investigate data pipeline for duplication source."
    })

if id_duplicates > 0:
    recommendations.append({
        "priority": "CRITICAL",
        "category": "Uniqueness",
        "issue": f"{id_duplicates} duplicate CustomerIDs found",
        "suggestion": "CustomerID should be a unique identifier. Investigate and resolve duplicates."
    })

for col, result in outlier_results.items():
    if result["outlier_count"] > 0:
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Outliers",
            "issue": f"{result['outlier_count']} outliers detected in '{col}' "
                     f"({result['outlier_percentage']}% of values)",
            "suggestion": f"Review outliers in '{col}' (values outside [{result['lower_bound']}, "
                         f"{result['upper_bound']}]). Determine if they are valid extreme values or errors."
        })

for anomaly in anomalies:
    recommendations.append({
        "priority": "HIGH",
        "category": "Anomaly",
        "issue": anomaly["description"],
        "suggestion": "Investigate and validate these records against source data."
    })

quality_report["recommendations"] = recommendations

# Save JSON
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(quality_report, f, indent=2, ensure_ascii=False, default=str)

print(f"\n{'=' * 70}")
print(f"Quality report saved to: {OUTPUT_PATH}")
print(f"{'=' * 70}")

# Print summary of recommendations
if recommendations:
    print(f"\n--- RECOMMENDATIONS ({len(recommendations)} items) ---")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  [{rec['priority']}] {rec['category']}")
        print(f"    Issue: {rec['issue']}")
        print(f"    Action: {rec['suggestion']}")
