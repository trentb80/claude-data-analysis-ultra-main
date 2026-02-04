# Slash Commands Implementation Guide

## Overview

This guide explains how slash commands are implemented in the Claude Data Analysis Assistant project. All 9 slash commands are already defined and ready to use.

## Current Implementation Status

### ✅ Fully Defined Commands (9/9)

1. **`/do-more`** - Automatic multi-skill analysis (⭐ Recommended)
2. **`/do-all`** - Complete interactive workflow with checkpoints
3. **`/analyze`** - General data analysis
4. **`/visualize`** - Data visualization
5. **`/quality`** - Data quality validation
6. **`/hypothesis`** - Research hypothesis generation
7. **`/generate`** - Code generation
8. **`/report`** - Report generation
9. **`/skills`** - Skills management

## Slash Command Architecture

### Directory Structure
```
.claude/
├── commands/               # Slash command definitions
│   ├── do-more.md         # Auto multi-skill analysis
│   ├── do-all.md          # Complete workflow
│   ├── analyze.md         # Data analysis
│   ├── visualize.md       # Visualizations
│   ├── quality.md         # Quality checks
│   ├── hypothesis.md      # Hypothesis generation
│   ├── generate.md        # Code generation
│   ├── report.md          # Report generation
│   └── skills.md          # Skills management
├── agents/                # Sub-agent configurations
├── skills/                # 12 specialized analysis skills
├── hooks/                 # Automation hooks
└── settings.json          # Claude Code configuration
```

## Command Definition Format

Each command is a Markdown file with YAML frontmatter:

```markdown
---
allowed-tools: Task, Read, Write, Bash, Grep, Glob, Edit, ...
description: Brief command description
argument-hint: [optional] [arguments]
skills: [optional skill references]
---

# Command Title

Command implementation details...

## Context
- Context variable 1: @path/to/resource
- Context variable 2: !`shell command`
- Argument reference: $1, $2, $3...

## Your Task
Detailed instructions for what the command should do...

## Expected Output
What files/reports should be generated...

## Example Usage
```bash
/command arg1 arg2
```
```

### YAML Frontmatter Fields

- **allowed-tools**: List of Claude Code tools the command can use
  - Common: `Task`, `Read`, `Write`, `Bash`, `Grep`, `Glob`, `Edit`
  - Advanced: `DeleteFile`, `RunCommand`, `StopCommand`, `CheckCommandStatus`, `TodoWrite`, `SearchCodebase`, `WebSearch`, `LS`

- **description**: One-line description (appears in command help)

- **argument-hint**: Optional hint for command arguments
  - Format: `[dataset] [analysis_type]`
  - Shown to user when they use the command

- **skills**: Optional reference to specific skills directory

### Context Variables

Commands can reference context using special syntax:

- **`@path/`** - Reference to a directory or file
  - Example: `@data_storage/` → `/home/user/project/data_storage/`
  - Example: `@data_storage/$1` → References first argument as file in data_storage

- **`!`command``** - Execute shell command and use output
  - Example: `!`pwd`` → Current working directory
  - Example: `!`date`` → Current date/time

- **`$N`** - Reference command arguments (N = 1, 2, 3...)
  - Example: `$1` → First argument
  - Example: `$2` → Second argument

## Command Delegation Pattern

Most commands delegate to specialized sub-agents using the Task tool:

```markdown
## Your Task

Use the [subagent-name] subagent to perform [task]:

### 1. Step One
- Detail 1
- Detail 2

### 2. Step Two
- Detail 1
- Detail 2

...
```

### Available Sub-Agents

1. **data-explorer** - Statistical analysis, pattern discovery
2. **visualization-specialist** - Chart creation, dashboards
3. **code-generator** - Analysis code generation
4. **report-writer** - Comprehensive reports
5. **quality-assurance** - Data validation, quality control
6. **hypothesis-generator** - Research hypothesis creation

## Command Details

### 1. `/do-more` - Automatic Multi-Skill Analysis

**Purpose**: Automatically observe data, match skills, execute analyses, generate reports

**Usage**:
```bash
/do-more
```

**Features**:
- ✅ Zero configuration required
- ✅ Auto-discovers data in `data_storage/`
- ✅ Matches 7+ relevant skills automatically
- ✅ Sequential execution
- ✅ Generates interactive HTML report
- ✅ Takes 2-5 minutes

**Output**:
```
do_more_analysis/
├── skill_execution/
│   ├── data-exploration-visualization/
│   ├── rfm-customer-segmentation/
│   ├── ltv-predictor/
│   ├── retention-analysis/
│   ├── funnel-analysis/
│   ├── growth-model-analyzer/
│   └── content-analysis/
└── integrated_results/
    └── Comprehensive_Analysis_Report.html
```

**Skill Matching Logic**:
- **E-commerce data** → RFM, LTV, Retention, Funnel, Growth, Recommender
- **User behavior** → User profiling, Retention, Funnel, Data exploration
- **Marketing data** → Attribution, Growth, A/B testing
- **Content data** → Content analysis, Recommender
- **General data** → Data exploration, Regression

### 2. `/do-all` - Complete Interactive Workflow

**Purpose**: Complete analysis workflow with human feedback checkpoints

**Usage**:
```bash
/do-all
```

**Features**:
- ✅ 6-stage comprehensive pipeline
- ✅ 3 human feedback checkpoints
- ✅ Custom code generation
- ✅ Multiple output formats
- ✅ Takes 10-30 minutes

**Workflow Stages**:
1. **Data Quality Assessment** → [Human Checkpoint: Confirm quality]
2. **Exploratory Data Analysis**
3. **Hypothesis Generation** → [Human Checkpoint: Approve hypotheses]
4. **Visualization** → [Human Checkpoint: Review visualizations]
5. **Code Generation**
6. **Report Generation**

**Output**:
```
complete_analysis/
├── data_quality_report/
├── exploratory_analysis/
├── hypothesis_reports/
├── visualizations/
├── generated_code/
├── final_report/
└── workflow_log/
```

### 3. `/analyze` - General Data Analysis

**Purpose**: Perform comprehensive data analysis using data-explorer sub-agent

**Usage**:
```bash
/analyze [dataset] [analysis_type]
```

**Arguments**:
- `dataset` - Dataset filename (in data_storage/)
- `analysis_type` - One of: exploratory, statistical, predictive, complete

**Example**:
```bash
/analyze sales_data.csv exploratory
/analyze customer_data.csv statistical
/analyze user_behavior.csv complete
```

**Output**: `analysis_reports/analysis_summary_[dataset].md`

### 4. `/visualize` - Data Visualization

**Purpose**: Create comprehensive visualizations using visualization-specialist

**Usage**:
```bash
/visualize [dataset] [chart_type]
```

**Arguments**:
- `dataset` - Dataset filename
- `chart_type` - One of: all, trends, distribution, correlation, comparison, custom

**Example**:
```bash
/visualize sales_data.csv all
/visualize user_behavior.csv trends
```

**Output**: `visualizations/dashboard_[dataset].html`

### 5. `/quality` - Data Quality Validation

**Purpose**: Perform data quality checks using quality-assurance sub-agent

**Usage**:
```bash
/quality [dataset] [action]
```

**Arguments**:
- `dataset` - Dataset filename
- `action` - One of: check, clean, validate, monitor, profile

**Example**:
```bash
/quality sales_data.csv check
/quality customer_data.csv validate
```

**Output**: `quality_reports/[dataset]_quality_check.json`

### 6. `/hypothesis` - Research Hypothesis Generation

**Purpose**: Generate research hypotheses using hypothesis-generator sub-agent

**Usage**:
```bash
/hypothesis [dataset] [domain]
```

**Arguments**:
- `dataset` - Dataset filename
- `domain` - Research domain (e-commerce, marketing, user_behavior, etc.)

**Example**:
```bash
/hypothesis sales_data.csv e-commerce
/hypothesis user_behavior.csv retention
```

**Output**: `hypothesis_reports/hypotheses_[dataset].md`

### 7. `/generate` - Code Generation

**Purpose**: Generate analysis code using code-generator sub-agent

**Usage**:
```bash
/generate [language] [analysis_type]
```

**Arguments**:
- `language` - python, r, sql, etc.
- `analysis_type` - Type of analysis code to generate

**Example**:
```bash
/generate python exploratory
/generate python machine-learning
```

**Output**: `generated_code/analysis_[type].py`

### 8. `/report` - Report Generation

**Purpose**: Generate comprehensive reports using report-writer sub-agent

**Usage**:
```bash
/report [dataset] [format]
```

**Arguments**:
- `dataset` - Dataset filename
- `format` - One of: html, pdf, markdown, docx

**Example**:
```bash
/report sales_data.csv html
/report customer_data.csv pdf
```

**Output**: `analysis_reports/report_[dataset].[format]`

### 9. `/skills` - Skills Management

**Purpose**: Manage and invoke specialized analysis skills

**Usage**:
```bash
/skills [action] [skill_name]
```

**Available Skills**:
- rfm-customer-segmentation
- ltv-predictor
- retention-analysis
- funnel-analysis
- user-profiling-analysis
- attribution-analysis-modeling
- growth-model-analyzer
- ab-testing-analyzer
- data-exploration-visualization
- regression-analysis-modeling
- content-analysis
- recommender-system

## How Commands Work

### Execution Flow

1. **User invokes command**: `/do-more`
2. **Claude Code parses command**: Loads `.claude/commands/do-more.md`
3. **Context resolution**: Resolves `@path`, `!`command``, `$N` variables
4. **Claude receives instructions**: Full command definition as context
5. **Claude executes**: Follows "Your Task" section
6. **Output generation**: Creates specified files/reports

### Behind the Scenes

When you type `/do-more`, Claude Code:

1. Finds `.claude/commands/do-more.md`
2. Parses YAML frontmatter for tools and permissions
3. Resolves context variables:
   - `@data_storage/` → `/home/user/project/data_storage/`
   - `!`pwd`` → `/home/user/project/`
4. Injects entire command definition into Claude's context
5. Claude follows the "Your Task" workflow
6. Claude uses allowed tools (Task, Read, Write, etc.)
7. Claude generates outputs as specified

## Testing Commands

### Test `/do-more` (Recommended First Test)

```bash
# 1. Ensure data is in data_storage/
ls data_storage/

# 2. Run command
/do-more

# 3. Wait for completion (2-5 minutes)

# 4. Check output
ls do_more_analysis/integrated_results/
open do_more_analysis/integrated_results/Comprehensive_Analysis_Report.html
```

### Test `/analyze`

```bash
# Analyze specific dataset
/analyze Orders.csv exploratory

# Check output
cat analysis_reports/analysis_summary_Orders.csv.md
```

### Test `/visualize`

```bash
# Create visualizations
/visualize Orders.csv all

# Check output
ls visualizations/
open visualizations/dashboard_Orders.csv.html
```

### Test `/quality`

```bash
# Check data quality
/quality Orders.csv check

# Check output
cat quality_reports/Orders.csv_quality_check.json
```

## Creating New Commands

### Step 1: Create Command File

Create `.claude/commands/my-command.md`:

```markdown
---
allowed-tools: Task, Read, Write, Bash, Grep, Glob
argument-hint: [arg1] [arg2]
description: My custom command description
---

# My Custom Command

Brief description of what this command does.

## Context
- Dataset: @data_storage/$1
- Output: ./my_command_output/
- Current directory: !`pwd`

## Your Task

1. Load dataset from `@data_storage/$1`
2. Perform custom analysis
3. Generate output report

## Expected Output

- `my_command_output/result.csv` - Analysis results
- `my_command_output/report.md` - Summary report

## Example Usage
```bash
/my-command dataset.csv
```
```

### Step 2: Test Command

```bash
/my-command test_data.csv
```

### Step 3: Iterate and Refine

- Add more detailed instructions in "Your Task"
- Specify exact output formats
- Add error handling guidelines
- Include validation checks

## Best Practices

### Command Design

1. **Clear Purpose**: Each command should do one thing well
2. **Consistent Naming**: Use verb-noun pattern (`analyze`, `visualize`, `generate`)
3. **Argument Flexibility**: Support both required and optional arguments
4. **Delegation**: Use sub-agents for complex tasks
5. **Output Standards**: Consistent output directory structure

### Documentation

1. **Comprehensive "Your Task"**: Detailed step-by-step workflow
2. **Context Variables**: Use `@`, `!``, `$` for dynamic paths
3. **Examples**: Include multiple usage examples
4. **Output Specification**: Explicitly list expected files
5. **Error Handling**: Include common error scenarios

### Integration

1. **Modular Design**: Commands should work independently
2. **Composability**: Commands can be chained together
3. **Consistent Outputs**: Standardized output formats
4. **Hooks Integration**: Work with validation hooks
5. **Skills Compatibility**: Integrate with skill system

## Troubleshooting

### Command Not Found

**Problem**: `/my-command` returns "Unknown command"

**Solution**:
1. Check file exists: `ls .claude/commands/my-command.md`
2. Check file permissions: `chmod 644 .claude/commands/my-command.md`
3. Restart Claude Code session

### Command Fails to Execute

**Problem**: Command starts but fails during execution

**Solution**:
1. Check allowed-tools include necessary tools
2. Verify context variables resolve correctly
3. Check output directories exist or can be created
4. Review Claude Code logs for error messages

### Wrong Output Generated

**Problem**: Command runs but output is incorrect

**Solution**:
1. Review "Your Task" section for clarity
2. Add more specific instructions
3. Include examples of expected output
4. Specify exact file formats and structures

### Permission Errors

**Problem**: Command can't access files or tools

**Solution**:
1. Check `.claude/settings.local.json` for permissions
2. Update allowed-tools in command YAML
3. Verify file paths are accessible

## Advanced Features

### Conditional Execution

Use context to conditionally execute parts:

```markdown
## Your Task

1. Check if `@data_storage/$1` exists
2. If exists, proceed with analysis
3. If not exists, search for alternative data files
4. ...
```

### Multi-Stage Workflows

Break complex workflows into stages:

```markdown
## Your Task

### Stage 1: Data Preparation
- Load data
- Clean data
- Validate quality

### Stage 2: Analysis
- Statistical analysis
- Pattern discovery

### Stage 3: Reporting
- Generate visualizations
- Create report
```

### Dynamic Skill Selection

Let commands intelligently select skills:

```markdown
## Your Task

1. Analyze data characteristics
2. Match appropriate skills from @skills/
3. Execute matched skills sequentially
4. Integrate results
```

## Integration with Skills

### Calling Skills from Commands

```markdown
## Your Task

1. Use the `/skills` command to invoke specific skill:
   - For customer data: `/skills run rfm-customer-segmentation`
   - For retention: `/skills run retention-analysis`
2. Process skill outputs
3. Integrate into command workflow
```

### Skills vs Commands

**Skills** (`.claude/skills/`):
- Specialized analysis modules
- Self-contained functionality
- Independent execution
- Python/R implementations

**Commands** (`.claude/commands/`):
- Orchestration and workflow
- User-facing interface
- Delegate to sub-agents and skills
- Markdown definitions

## Next Steps

1. **Test existing commands**: Try `/do-more` on sample data
2. **Explore command definitions**: Read through `.claude/commands/*.md`
3. **Customize commands**: Modify existing commands for your needs
4. **Create new commands**: Add custom commands for specific workflows
5. **Document workflows**: Create usage guides for your team

## Resources

- **Claude Code Documentation**: https://docs.anthropic.com/claude/code
- **Command Examples**: `.claude/commands/*.md`
- **Skills Documentation**: `.claude/skills/*/SKILL.md`
- **Project Guide**: `CLAUDE.md`

## Summary

All 9 slash commands are fully defined and ready to use:

✅ `/do-more` - Quick automated analysis (recommended)
✅ `/do-all` - Complete interactive workflow
✅ `/analyze` - General data analysis
✅ `/visualize` - Data visualizations
✅ `/quality` - Quality validation
✅ `/hypothesis` - Hypothesis generation
✅ `/generate` - Code generation
✅ `/report` - Report generation
✅ `/skills` - Skills management

**Start with**: `/do-more` for immediate results!
