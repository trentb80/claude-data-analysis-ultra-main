# Slash Commands Testing Guide

## Your Setup

✅ **Commands**: 9 slash commands fully defined in `.claude/commands/`
✅ **Data**: Olist e-commerce dataset (8 files, 500K+ records) in `data_storage/`
✅ **Skills**: 12 specialized analysis skills in `.claude/skills/`
✅ **Ready**: Everything is configured and ready to use!

## Available Data

Your `data_storage/` directory contains:

| File | Records | Size | Description |
|------|---------|------|-------------|
| Orders.csv | 99,442 | 15MB | Order transactions |
| Customers.csv | 99,442 | 8.7MB | Customer information |
| Order Items.csv | ~200K | 15MB | Order line items |
| Order Payments.csv | ~100K | 5.6MB | Payment details |
| Reviews.csv | 104,720 | 14MB | Customer reviews |
| Products.csv | 32,952 | 2.3MB | Product catalog |
| Sellers.csv | 3,096 | 171KB | Seller information |
| Categories.csv | 71 | 2.5KB | Product categories |

This is **perfect data** for testing all commands!

## Recommended Testing Sequence

### Test 1: `/do-more` - Full Auto Analysis (⭐ Start Here!)

**Purpose**: Test the complete automatic analysis workflow

**Command**:
```bash
/do-more
```

**Expected Behavior**:
1. Scans all 8 files in `data_storage/`
2. Identifies e-commerce data type
3. Matches 7+ relevant skills:
   - data-exploration-visualization
   - rfm-customer-segmentation
   - ltv-predictor
   - retention-analysis
   - funnel-analysis
   - growth-model-analyzer
   - content-analysis (for reviews)
4. Executes each skill sequentially
5. Generates integrated HTML report

**Expected Output**:
```
do_more_analysis/
├── skill_execution/
│   ├── data-exploration-visualization/
│   │   ├── exploration_summary.csv
│   │   ├── correlation_matrix.png
│   │   └── distribution_plots.png
│   ├── rfm-customer-segmentation/
│   │   ├── customer_segments.csv
│   │   ├── vip_customers.csv
│   │   └── rfm_analysis.png
│   ├── ltv-predictor/
│   │   ├── ltv_predictions.csv
│   │   └── ltv_distribution.png
│   ├── retention-analysis/
│   │   ├── retention_rates.csv
│   │   └── cohort_heatmap.png
│   ├── funnel-analysis/
│   │   ├── conversion_funnel.csv
│   │   └── funnel_visualization.png
│   ├── growth-model-analyzer/
│   │   ├── growth_metrics.csv
│   │   └── growth_trends.png
│   └── content-analysis/
│       ├── sentiment_analysis.csv
│       └── review_wordcloud.png
└── integrated_results/
    ├── Comprehensive_Analysis_Report.html  # ⭐ Main output
    ├── Comprehensive_Analysis_Report.md
    └── integrated_summary.json
```

**Time**: 2-5 minutes

**Verification**:
```bash
# Check output directory created
ls -la do_more_analysis/

# View skill execution results
ls do_more_analysis/skill_execution/

# Open HTML report (main result)
open do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html
```

**What to Look For**:
- ✅ All 7+ skills executed successfully
- ✅ HTML report generated with visualizations
- ✅ Key insights and recommendations included
- ✅ VIP customer lists and segments created
- ✅ LTV predictions calculated
- ✅ Retention cohort analysis completed

---

### Test 2: `/analyze` - Basic Analysis

**Purpose**: Test single dataset analysis

**Command**:
```bash
/analyze Orders.csv exploratory
```

**Expected Behavior**:
1. Loads Orders.csv (99,442 records)
2. Performs exploratory data analysis
3. Generates statistical summaries
4. Identifies patterns and anomalies
5. Creates analysis report

**Expected Output**:
```
analysis_reports/
└── analysis_summary_Orders.csv.md
```

**Verification**:
```bash
# Check report created
ls -la analysis_reports/

# View report content
cat analysis_reports/analysis_summary_Orders.csv.md
```

**What to Look For**:
- ✅ Dataset shape and structure
- ✅ Missing value analysis
- ✅ Statistical summaries
- ✅ Key patterns identified
- ✅ Actionable insights

---

### Test 3: `/visualize` - Create Visualizations

**Purpose**: Test visualization generation

**Command**:
```bash
/visualize Orders.csv all
```

**Expected Behavior**:
1. Loads Orders.csv
2. Creates comprehensive dashboard
3. Generates multiple chart types
4. Produces interactive HTML

**Expected Output**:
```
visualizations/
├── dashboard_Orders.csv.html
├── summary_Orders.csv.png
└── charts_Orders.csv.py
```

**Verification**:
```bash
# Check visualizations created
ls -la visualizations/

# Open interactive dashboard
open visualizations/dashboard_Orders.csv.html
```

**What to Look For**:
- ✅ Interactive HTML dashboard
- ✅ Multiple chart types (trends, distributions, etc.)
- ✅ Clear labels and legends
- ✅ Responsive design

---

### Test 4: `/quality` - Data Quality Check

**Purpose**: Test data quality validation

**Command**:
```bash
/quality Orders.csv check
```

**Expected Behavior**:
1. Loads Orders.csv
2. Assesses data quality across 6 dimensions
3. Calculates quality scores
4. Identifies issues
5. Generates quality report

**Expected Output**:
```
quality_reports/
├── Orders.csv_quality_check.json
├── Orders.csv_data_profile.json
└── Orders.csv_validation_report.md
```

**Verification**:
```bash
# Check quality reports
ls -la quality_reports/

# View quality score
cat quality_reports/Orders.csv_quality_check.json | grep -A 5 "overall_score"
```

**What to Look For**:
- ✅ Overall quality score (0-100)
- ✅ Dimension-specific scores (completeness, accuracy, etc.)
- ✅ Issue counts and severity
- ✅ Recommendations for improvement

---

### Test 5: `/hypothesis` - Generate Hypotheses

**Purpose**: Test hypothesis generation

**Command**:
```bash
/hypothesis Orders.csv e-commerce
```

**Expected Behavior**:
1. Analyzes Orders.csv patterns
2. Generates testable hypotheses
3. Designs validation experiments
4. Creates research plan

**Expected Output**:
```
hypothesis_reports/
├── hypotheses_Orders.csv.md
├── experimental_design.md
└── validation_plan.md
```

**Verification**:
```bash
# Check hypothesis reports
ls -la hypothesis_reports/

# View hypotheses
cat hypothesis_reports/hypotheses_Orders.csv.md
```

**What to Look For**:
- ✅ 5-10 testable hypotheses
- ✅ Clear experimental designs
- ✅ Validation methodologies
- ✅ Expected outcomes

---

### Test 6: `/generate` - Code Generation

**Purpose**: Test analysis code generation

**Command**:
```bash
/generate python exploratory
```

**Expected Behavior**:
1. Generates exploratory analysis code
2. Creates data loading pipeline
3. Includes visualization code
4. Adds documentation

**Expected Output**:
```
generated_code/
├── analysis_exploratory.py
├── data_preprocessing.py
└── README.md
```

**Verification**:
```bash
# Check generated code
ls -la generated_code/

# View code
head -n 50 generated_code/analysis_exploratory.py
```

**What to Look For**:
- ✅ Clean, readable code
- ✅ Proper imports and setup
- ✅ Data loading functions
- ✅ Analysis functions
- ✅ Visualization code
- ✅ Documentation and comments

---

### Test 7: `/report` - Report Generation

**Purpose**: Test report generation

**Command**:
```bash
/report Orders.csv html
```

**Expected Behavior**:
1. Loads previous analysis results
2. Integrates findings
3. Creates comprehensive report
4. Generates HTML output

**Expected Output**:
```
analysis_reports/
└── report_Orders.csv.html
```

**Verification**:
```bash
# Check report
ls -la analysis_reports/report_Orders.csv.html

# Open report
open analysis_reports/report_Orders.csv.html
```

**What to Look For**:
- ✅ Executive summary
- ✅ Key findings
- ✅ Visualizations embedded
- ✅ Recommendations
- ✅ Professional formatting

---

### Test 8: `/do-all` - Complete Workflow

**Purpose**: Test complete interactive workflow

**Command**:
```bash
/do-all
```

**Expected Behavior**:
1. **Stage 1**: Data quality assessment
   - Shows quality score
   - **[Checkpoint]**: Asks for confirmation
2. **Stage 2**: Exploratory analysis
   - Performs comprehensive EDA
3. **Stage 3**: Hypothesis generation
   - Generates hypotheses
   - **[Checkpoint]**: Asks for approval
4. **Stage 4**: Visualization
   - Creates dashboards
   - **[Checkpoint]**: Asks for review
5. **Stage 5**: Code generation
   - Generates analysis code
6. **Stage 6**: Report generation
   - Creates final reports

**Expected Output**:
```
complete_analysis/
├── data_quality_report/
│   ├── quality_assessment.json
│   └── quality_improvement_recommendations.md
├── exploratory_analysis/
│   ├── statistical_summary.csv
│   └── pattern_analysis.md
├── hypothesis_reports/
│   ├── research_hypotheses.md
│   └── experimental_design.md
├── visualizations/
│   ├── interactive_dashboard.html
│   └── analysis_charts.png
├── generated_code/
│   ├── complete_analysis_pipeline.py
│   └── data_preprocessing.py
├── final_report/
│   ├── comprehensive_analysis_report.html
│   └── executive_summary.html
└── workflow_log/
    ├── analysis_progress.log
    └── execution_summary.md
```

**Time**: 10-30 minutes (with interactive checkpoints)

**Verification**:
```bash
# Check complete analysis directory
ls -la complete_analysis/

# View final report
open complete_analysis/final_report/comprehensive_analysis_report.html
```

**What to Look For**:
- ✅ All 6 stages completed
- ✅ Human feedback recorded
- ✅ Complete code generated
- ✅ Comprehensive documentation
- ✅ Multiple output formats

---

### Test 9: `/skills` - Skills Management

**Purpose**: Test skills invocation

**Command**:
```bash
/skills list
```

**Expected Behavior**:
Lists all 12 available skills

**Then test specific skill**:
```bash
/skills run rfm-customer-segmentation
```

**Expected Output**: RFM analysis results

---

## Detailed Test Checklist

### Pre-Test Checklist

- [ ] All command files exist in `.claude/commands/`
- [ ] Data files exist in `data_storage/`
- [ ] Output directories can be created (permissions)
- [ ] Python environment has required packages

**Verify**:
```bash
# Check commands
ls .claude/commands/*.md | wc -l  # Should be 9

# Check data
ls data_storage/*.csv | wc -l  # Should be 8

# Check permissions
mkdir -p test_output && rm -rf test_output  # Should succeed

# Check Python packages
python -c "import pandas, numpy, matplotlib, seaborn, sklearn"  # Should succeed
```

### During Testing

For each command test:

- [ ] Command recognized (no "Unknown command" error)
- [ ] Execution starts without immediate errors
- [ ] Progress is visible (logging/output)
- [ ] Expected files are created
- [ ] Output quality is good (no empty files)
- [ ] Execution completes successfully

### Post-Test Verification

- [ ] All output directories created
- [ ] HTML reports can be opened in browser
- [ ] CSV files are valid and non-empty
- [ ] PNG/image files are valid
- [ ] Markdown files are well-formatted
- [ ] JSON files are valid JSON

**Verify outputs**:
```bash
# Check all output directories
ls -la do_more_analysis/
ls -la complete_analysis/
ls -la analysis_reports/
ls -la visualizations/
ls -la quality_reports/
ls -la hypothesis_reports/
ls -la generated_code/

# Validate JSON files
for file in quality_reports/*.json; do
    python -m json.tool "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"
done

# Check HTML files can be opened
for file in visualizations/*.html; do
    [ -f "$file" ] && [ -s "$file" ] && echo "✓ $file" || echo "✗ $file"
done
```

## Common Issues and Solutions

### Issue: Command not found

**Symptoms**: `/do-more` returns "Unknown command"

**Solutions**:
```bash
# 1. Check command file exists
ls -la .claude/commands/do-more.md

# 2. Verify YAML frontmatter format
head -n 10 .claude/commands/do-more.md

# 3. Check file permissions
chmod 644 .claude/commands/*.md

# 4. Restart Claude Code session
```

### Issue: No data found

**Symptoms**: "Dataset not found" or "No files in data_storage"

**Solutions**:
```bash
# 1. Verify data exists
ls -la data_storage/

# 2. Check file permissions
chmod 644 data_storage/*.csv

# 3. Verify file names (case-sensitive!)
ls data_storage/ | grep -i orders
```

### Issue: Permission denied

**Symptoms**: "Permission denied" when creating output

**Solutions**:
```bash
# 1. Check directory permissions
ls -ld .

# 2. Create output directories manually
mkdir -p do_more_analysis analysis_reports visualizations quality_reports

# 3. Fix permissions
chmod 755 .
```

### Issue: Missing Python packages

**Symptoms**: "ModuleNotFoundError" or import errors

**Solutions**:
```bash
# Install core packages
pip install pandas numpy matplotlib seaborn scikit-learn scipy

# Install skill-specific packages
cd .claude/skills/rfm-customer-segmentation/
pip install -r requirements.txt
```

### Issue: Command runs but no output

**Symptoms**: Command completes but no files generated

**Solutions**:
```bash
# 1. Check for error messages in console
# 2. Verify output directory permissions
# 3. Check disk space
df -h .

# 4. Try with verbose logging
# (if available in Claude Code)
```

### Issue: HTML report won't open

**Symptoms**: HTML file exists but won't display

**Solutions**:
```bash
# 1. Check file size
ls -lh do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html

# 2. Validate HTML
head -n 20 do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html

# 3. Try different browser
# 4. Check for encoding issues
file do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html
```

## Performance Expectations

| Command | Dataset Size | Expected Time | Memory Usage |
|---------|-------------|---------------|--------------|
| `/do-more` | 100K records | 2-5 minutes | < 2GB |
| `/do-all` | 100K records | 10-30 minutes | < 2GB |
| `/analyze` | 100K records | 1-3 minutes | < 1GB |
| `/visualize` | 100K records | 1-2 minutes | < 1GB |
| `/quality` | 100K records | 1-2 minutes | < 1GB |
| `/hypothesis` | N/A | 2-4 minutes | < 500MB |
| `/generate` | N/A | 1-2 minutes | < 100MB |
| `/report` | N/A | 1-3 minutes | < 500MB |
| `/skills` | Varies | 2-10 minutes | < 2GB |

## Success Criteria

### Minimum Success (Basic Functionality)

- [ ] At least 1 command executes successfully
- [ ] Output files are generated
- [ ] No critical errors

### Good Success (Full Functionality)

- [ ] All 9 commands execute successfully
- [ ] Output quality is good
- [ ] Reports are readable and informative
- [ ] Visualizations render correctly

### Excellent Success (Production Ready)

- [ ] All commands execute without errors
- [ ] Output is comprehensive and insightful
- [ ] Reports are professional quality
- [ ] Visualizations are publication-ready
- [ ] Code is clean and documented
- [ ] Performance is acceptable

## Next Steps After Testing

Once testing is complete:

1. **Document Results**
   ```bash
   # Create test results summary
   echo "Test Results: $(date)" > test_results.txt
   echo "---" >> test_results.txt
   echo "✓ Commands tested: X/9" >> test_results.txt
   echo "✓ Issues found: Y" >> test_results.txt
   ```

2. **Review Outputs**
   - Open HTML reports in browser
   - Review analysis findings
   - Check visualizations
   - Validate code quality

3. **Customize Commands** (if needed)
   - Edit `.claude/commands/*.md` files
   - Add custom workflows
   - Adjust output formats

4. **Production Use**
   - Use `/do-more` for regular analysis
   - Build custom workflows
   - Integrate with your pipelines

## Quick Test Script

Save this as `test_commands.sh`:

```bash
#!/bin/bash

echo "Testing Claude Data Analysis Slash Commands"
echo "=========================================="
echo ""

# Test 1: Check setup
echo "Test 1: Checking setup..."
[ -d ".claude/commands" ] && echo "✓ Commands directory exists" || echo "✗ Commands directory missing"
[ -d "data_storage" ] && echo "✓ Data storage exists" || echo "✗ Data storage missing"
[ $(ls data_storage/*.csv 2>/dev/null | wc -l) -gt 0 ] && echo "✓ Data files found" || echo "✗ No data files"
echo ""

# Test 2: Verify commands
echo "Test 2: Verifying command files..."
for cmd in do-more do-all analyze visualize quality hypothesis generate report skills; do
    [ -f ".claude/commands/${cmd}.md" ] && echo "✓ ${cmd}" || echo "✗ ${cmd}"
done
echo ""

# Test 3: Check Python environment
echo "Test 3: Checking Python packages..."
python -c "import pandas" 2>/dev/null && echo "✓ pandas" || echo "✗ pandas"
python -c "import numpy" 2>/dev/null && echo "✓ numpy" || echo "✗ numpy"
python -c "import matplotlib" 2>/dev/null && echo "✓ matplotlib" || echo "✗ matplotlib"
python -c "import seaborn" 2>/dev/null && echo "✓ seaborn" || echo "✗ seaborn"
python -c "import sklearn" 2>/dev/null && echo "✓ scikit-learn" || echo "✗ scikit-learn"
echo ""

echo "Setup verification complete!"
echo ""
echo "Ready to test commands. Try:"
echo "  /do-more"
```

Run it:
```bash
chmod +x test_commands.sh
./test_commands.sh
```

## Summary

✅ **You have**: 9 fully-defined slash commands
✅ **You have**: Complete Olist e-commerce dataset
✅ **You can**: Start testing immediately

**Recommended first test**:
```bash
/do-more
```

This will give you immediate results and demonstrate the full system working!
