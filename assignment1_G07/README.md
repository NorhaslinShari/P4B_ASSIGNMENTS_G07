# Variant Triage Service (SECB3203 Assignment 1)

> Replace the text in this template. The README must let a stranger install, run and test the
> project with the exact commands below. All data are synthetic teaching data, not clinical data.

## Group

- Group ID: G07
- Members: NORHASLIN BINTI SHARI (A24CS0149), FATIN SYAKIRAH BINTI MOHAMAD HARDON (A24CS0073), BATRISYIA AMANI BINTI KHAIRUN HALED (A24CS0054)

## What this project does
This project is a rule-based variant triage service that classifies genetic variants as prioritize, review, or exclude. It reads variant data from a CSV file and parameters from a JSON file, applies predefined classification rules, and generates a CSV output and summary report.

## Set up
```
python -m venv .venv
<activate command for your system>
pip install -r requirements.txt
```

## Run
Command : python src/a1_triage.py data/variants.csv data/params.json results

Files in the results/ directory:

- triage.csv 
- report.txt 

## Test and lint

```
python -m pytest
ruff check src
```

## Our parameters

{
  "min_depth": 12,
  "min_quality": 70,
  "priority_genes": [
    "ATM",
    "PTEN",
    "EGFR",
    "APC",
    "BRCA2"
  ],
  "top_k": 6
}
They are read at run time and passed to the functions; they are not typed into the rules.

## Design
The document describes the problem decomposition, classification rules, pseudocode, hand-traced examples, test plan, and work allocation among group members. It explains how variant data are processed and how classification decisions are produced based on configurable thresholds and priority genes.

## Limitations
1. Only depth, quality, gene priority, and impact are considered when making decisions; other genomic factors are not evaluated.
2. Missing or malformed input fields may cause errors if they are not handled before processing.

## Who did what

|     Member     | Main contributions                                    | Commits  |
|----------------|-------------------------------------------------------|----------|
| Fatin Syakirah | docs/design.md, GROUP_CONTRACT, AI_USE_LOG.md         |    9     |
| Batrisyia Amani| classify_variant(), triage(), rank_variants()         |    7     |
| Norhaslin      | decision_counts(), results_to_csv(), build_report(),  |    32    |
|                |  test_a1_triage.py, gene_summary(), impact_count()    |          |
|                |  README.md and code quality checks                    |          |


## AI use
Yes, we all use AI
