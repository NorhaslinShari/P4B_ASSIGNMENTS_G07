# Variant Triage Service (SECB3203 Assignment 1)

> Replace the text in this template. The README must let a stranger install, run and test the
> project with the exact commands below. All data are synthetic teaching data, not clinical data.

## Group

- Group ID: Group G07
- Members: NORHASLIN BINTI SHARI (A24CS0149), FATIN SYAKIRAH BINTI MOHAMAD HARDON (A24CS0073), BATRISYIA AMANI BINTI KHAIRUN HALED (A24CS0054)

## What this project does

<Three or four sentences: what a variant triage service is, what goes in, what comes out.>

## Set up

```
python -m venv .venv
<activate command for your system>
pip install -r requirements.txt
```

## Run
Run the program using:

python src/a1_triage.py data/variants.csv data/params.json results

The program generates the following files in the results/ directory:

- triage.csv - classified variant results
- report.txt - summary report containing statistics and decision counts

<Say which files appear in results/.>

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

<Link to docs/design.md and say in two sentences what it contains.>
The document describes the problem decomposition, classification rules, pseudocode, hand-traced examples, test plan, and work allocation among group members. It explains how variant data are processed and how classification decisions are produced based on configurable thresholds and priority genes.

## Limitations
1. Only depth, quality, gene priority, and impact are considered when making decisions; other genomic factors are not evaluated.
2. Missing or malformed input fields may cause errors if they are not handled before processing.

<At least two honest limitations, for example: rules use depth, quality and impact only; the data are synthetic.>

## Who did what

|     Member     | Main contributions                                    | Commits  |
|----------------|-------------------------------------------------------|----------|
| Fatin Syakirah | docs/design.md, GROUP_CONTRACT, AI_USE_LOG.md         | <number> |
| Batrisyia Amani| classify_variant(), triage(), rank_variants()         |          |
| Norhaslin      | decision_counts(), results_to_csv(), build_report(),  |          |
                 |  test_a1_triage.py, gene_summary(), impact_count()    |
                 |  README.md and code quality checks                    |


## AI use

Yes, we all use AI
