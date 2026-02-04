# Slash Commands Quick Reference

## Quick Start

**Fastest way to get insights:**
```bash
/do-more
```
That's it! Auto-analyzes all data in `data_storage/` and generates HTML report in 2-5 minutes.

---

## All Commands

| Command | Usage | Time | Description |
|---------|-------|------|-------------|
| **`/do-more`** ⭐ | `/do-more` | 2-5 min | Auto multi-skill analysis (recommended) |
| **`/do-all`** | `/do-all` | 10-30 min | Complete workflow with checkpoints |
| `/analyze` | `/analyze [file] [type]` | 1-3 min | General data analysis |
| `/visualize` | `/visualize [file] [chart]` | 1-2 min | Create visualizations |
| `/quality` | `/quality [file] [action]` | 1-2 min | Data quality checks |
| `/hypothesis` | `/hypothesis [file] [domain]` | 2-4 min | Generate hypotheses |
| `/generate` | `/generate [lang] [type]` | 1-2 min | Generate analysis code |
| `/report` | `/report [file] [format]` | 1-3 min | Generate reports |
| `/skills` | `/skills [action] [skill]` | varies | Manage/run skills |

---

## Command Details

### `/do-more` - Auto Multi-Skill Analysis ⭐

**Purpose**: Zero-config automatic analysis

```bash
/do-more
```

**What it does**:
- Scans `data_storage/` automatically
- Matches 7+ relevant skills
- Executes all analyses sequentially
- Generates interactive HTML report

**Output**: `do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html`

**Best for**: Quick insights, executive presentations, initial exploration

---

### `/do-all` - Complete Workflow

**Purpose**: Thorough analysis with human oversight

```bash
/do-all
```

**What it does**:
1. Data quality assessment → [you confirm]
2. Exploratory analysis
3. Hypothesis generation → [you approve]
4. Visualizations → [you review]
5. Code generation
6. Comprehensive report

**Output**: `complete_analysis/` directory with code, reports, dashboards

**Best for**: Research projects, publication-quality reports, custom analysis

---

### `/analyze` - Data Analysis

**Purpose**: Comprehensive data analysis

```bash
/analyze [dataset] [type]
```

**Arguments**:
- `dataset` - Filename in data_storage/ (e.g., "sales.csv")
- `type` - Analysis type:
  - `exploratory` - Basic EDA
  - `statistical` - Statistical testing
  - `predictive` - ML preparation
  - `complete` - All of above

**Examples**:
```bash
/analyze Orders.csv exploratory
/analyze Customers.csv statistical
/analyze sales_data.csv complete
```

**Output**: `analysis_reports/analysis_summary_[dataset].md`

---

### `/visualize` - Visualizations

**Purpose**: Create data visualizations

```bash
/visualize [dataset] [chart_type]
```

**Arguments**:
- `dataset` - Filename in data_storage/
- `chart_type` - Visualization type:
  - `all` - Comprehensive dashboard
  - `trends` - Time series charts
  - `distribution` - Histograms, box plots
  - `correlation` - Heatmaps, scatter plots
  - `comparison` - Bar charts
  - `custom` - Custom visualizations

**Examples**:
```bash
/visualize Orders.csv all
/visualize sales_data.csv trends
/visualize user_behavior.csv correlation
```

**Output**: `visualizations/dashboard_[dataset].html`

---

### `/quality` - Data Quality

**Purpose**: Validate data quality

```bash
/quality [dataset] [action]
```

**Arguments**:
- `dataset` - Filename in data_storage/
- `action` - Quality action:
  - `check` - Basic quality assessment
  - `clean` - Data cleaning
  - `validate` - Comprehensive validation
  - `monitor` - Setup monitoring
  - `profile` - Detailed profiling

**Examples**:
```bash
/quality Orders.csv check
/quality Customers.csv validate
/quality sales_data.csv clean
```

**Output**: `quality_reports/[dataset]_quality_check.json`

---

### `/hypothesis` - Research Hypotheses

**Purpose**: Generate research hypotheses

```bash
/hypothesis [dataset] [domain]
```

**Arguments**:
- `dataset` - Filename in data_storage/
- `domain` - Research domain:
  - `e-commerce` - E-commerce hypotheses
  - `marketing` - Marketing hypotheses
  - `user_behavior` - User behavior hypotheses
  - `retention` - Retention hypotheses
  - `general` - General hypotheses

**Examples**:
```bash
/hypothesis Orders.csv e-commerce
/hypothesis user_logs.csv retention
/hypothesis campaign_data.csv marketing
```

**Output**: `hypothesis_reports/hypotheses_[dataset].md`

---

### `/generate` - Code Generation

**Purpose**: Generate analysis code

```bash
/generate [language] [type]
```

**Arguments**:
- `language` - Programming language:
  - `python` - Python code
  - `r` - R code
  - `sql` - SQL queries
- `type` - Analysis type:
  - `exploratory` - EDA code
  - `statistical` - Statistical analysis
  - `machine-learning` - ML pipeline
  - `visualization` - Visualization code
  - `complete` - Full pipeline

**Examples**:
```bash
/generate python exploratory
/generate python machine-learning
/generate sql data-extraction
```

**Output**: `generated_code/analysis_[type].py`

---

### `/report` - Report Generation

**Purpose**: Generate comprehensive reports

```bash
/report [dataset] [format]
```

**Arguments**:
- `dataset` - Filename in data_storage/
- `format` - Output format:
  - `html` - Interactive HTML
  - `pdf` - PDF document
  - `markdown` - Markdown file
  - `docx` - Word document

**Examples**:
```bash
/report Orders.csv html
/report sales_analysis.csv pdf
/report customer_insights.csv docx
```

**Output**: `analysis_reports/report_[dataset].[format]`

---

### `/skills` - Skills Management

**Purpose**: Manage and invoke specialized skills

```bash
/skills [action] [skill_name]
```

**Available Skills**:

**Customer Analysis:**
- `rfm-customer-segmentation` - RFM analysis
- `ltv-predictor` - LTV prediction
- `user-profiling-analysis` - User profiling
- `retention-analysis` - Retention analysis

**Marketing Analysis:**
- `attribution-analysis-modeling` - Attribution modeling
- `growth-model-analyzer` - Growth analysis
- `ab-testing-analyzer` - A/B testing
- `funnel-analysis` - Funnel analysis

**Data Analysis:**
- `data-exploration-visualization` - EDA
- `regression-analysis-modeling` - Regression
- `content-analysis` - Text/content analysis
- `recommender-system` - Recommendations

**Examples**:
```bash
/skills list
/skills run rfm-customer-segmentation
/skills info ltv-predictor
```

---

## Common Workflows

### Quick Business Review (5 minutes)

```bash
# One command, complete analysis
/do-more

# Open report
open do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html
```

### Initial Data Exploration (10 minutes)

```bash
# Check data quality
/quality Orders.csv check

# Exploratory analysis
/analyze Orders.csv exploratory

# Create visualizations
/visualize Orders.csv all
```

### Complete Research Analysis (30 minutes)

```bash
# Interactive complete workflow
/do-all
# → Follow prompts at each checkpoint
```

### Custom Analysis Pipeline (15 minutes)

```bash
# 1. Validate data
/quality sales_data.csv validate

# 2. Analyze
/analyze sales_data.csv complete

# 3. Generate hypotheses
/hypothesis sales_data.csv e-commerce

# 4. Visualize
/visualize sales_data.csv all

# 5. Generate report
/report sales_data.csv html
```

---

## Decision Guide

**Choose `/do-more` when you want:**
- ✅ Fast results (2-5 min)
- ✅ No configuration
- ✅ Automatic skill matching
- ✅ Quick insights

**Choose `/do-all` when you want:**
- ✅ Deep analysis (10-30 min)
- ✅ Human oversight
- ✅ Custom direction
- ✅ Publication-quality results

**Choose individual commands when you want:**
- ✅ Specific analysis
- ✅ Custom workflow
- ✅ Fine control
- ✅ Integration with other tools

---

## Tips & Best Practices

### Data Preparation

1. **Place data in `data_storage/`**
   ```bash
   cp my_data.csv data_storage/
   ```

2. **Use consistent naming**
   - Good: `Orders.csv`, `Customers.csv`
   - Avoid: `data (1).csv`, `final_FINAL_v2.csv`

3. **Check data format**
   ```bash
   head -n 5 data_storage/Orders.csv
   ```

### Command Usage

1. **Start simple** - Try `/do-more` first
2. **Check outputs** - Review generated files
3. **Iterate** - Use specific commands for deeper analysis
4. **Chain commands** - Combine for custom workflows

### Output Management

1. **Review HTML reports** - Most interactive and comprehensive
2. **Export key findings** - Save important insights
3. **Archive results** - Keep for future reference
4. **Clean old outputs** - Remove outdated analyses

---

## Troubleshooting

### Command not found
```bash
# Check if command file exists
ls .claude/commands/

# Should see: analyze.md, do-all.md, do-more.md, etc.
```

### No data found
```bash
# Check data_storage directory
ls data_storage/

# If empty, add your data files
cp your_data.csv data_storage/
```

### Command fails
```bash
# Check data format
head data_storage/your_file.csv

# Verify file permissions
ls -la data_storage/

# Check for errors in Claude Code console
```

### Missing dependencies
```bash
# Install Python dependencies
pip install pandas numpy matplotlib seaborn scikit-learn

# Install skill-specific requirements
cd .claude/skills/[skill_name]/
pip install -r requirements.txt
```

---

## Quick Examples

### E-commerce Analysis
```bash
# Auto-analyze orders, customers, products
/do-more
# → RFM segmentation, LTV prediction, retention analysis, etc.
```

### User Behavior Analysis
```bash
# Analyze user activity
/analyze user_logs.csv exploratory
/visualize user_logs.csv trends
/hypothesis user_logs.csv user_behavior
```

### Marketing Campaign Analysis
```bash
# Campaign performance
/quality campaigns.csv check
/analyze campaigns.csv statistical
/visualize campaigns.csv comparison
```

### Quality Audit
```bash
# Comprehensive quality check
/quality dataset.csv validate
/quality dataset.csv profile
/report dataset.csv html
```

---

## Output Directory Structure

```
project/
├── data_storage/              # Your data files
├── do_more_analysis/          # /do-more output
│   ├── skill_execution/
│   └── integrated_results/
├── complete_analysis/         # /do-all output
│   ├── data_quality_report/
│   ├── exploratory_analysis/
│   ├── hypothesis_reports/
│   ├── visualizations/
│   ├── generated_code/
│   └── final_report/
├── analysis_reports/          # /analyze, /report output
├── visualizations/            # /visualize output
├── quality_reports/           # /quality output
├── hypothesis_reports/        # /hypothesis output
└── generated_code/            # /generate output
```

---

## Learn More

- **Full Guide**: See `SLASH_COMMANDS_IMPLEMENTATION_GUIDE.md`
- **Project Overview**: See `CLAUDE.md`
- **Skill Details**: See `.claude/skills/*/SKILL.md`
- **Command Definitions**: See `.claude/commands/*.md`

---

## Summary

**Start here**: `/do-more` - One command, complete analysis, 2-5 minutes!
