# Design - Variant Triage Service

Group ID: G07    
Thresholds from data/params.json: min_depth = 12, min_quality = 70, top_k = 6

## 1. Decomposition

| Question | Our answer |
|---|---|
| Input | A variant row containing variant, gene, chrom, pos, ref, alt, depth, quality and impact. A parameters dictionary containing min_depth, min_quality, priority_genes and top_k |
| Output | Classification result consisting of a decision (prioritize, review or exclude) and a reason. Triage produces a list of new dictionaries with decision and reason added |
| Constraints (named thresholds, what happens at exactly the threshold) | min_depth and min_quality are read from params, never hard-coded. Boundaries are inclusive: depth passes and depth  is excluded quality passes and quality is excluded. Gene and impact are compared after strip() and case folding. Rule order must be followed exactly |
| Rule order and why the order matters | The rules are checked from Rule 1 to Rule 6. The first matching rule determines the decision. Order matters because a variant may satisfy multiple conditions. For example, a variant with depth below the threshold and quality below the threshold must be excluded for low depth because Rule 1 comes before Rule 2. |
| Out of scope | Reading and writing files (main is given), validating chrom, ref or alt, biological interpretation, and handling missing columns |

## 2. Pseudocode or flowchart of classify_variant

FUNCTION classify_variant(row, params)

    depth = depth value
    quality = quality value
    gene = normalized gene name
    impact = normalized impact

    IF depth < min_depth    #rule 1
        RETURN exclude

    IF quality < min_quality    #rule 2
        RETURN exclude

    IF gene is a priority gene AND impact is high or moderate   #rule 3
        RETURN prioritize

    IF gene is a priority gene AND impact is low or modifier    #rule 4
        RETURN review

    IF gene is NOT a priority gene AND impact is high or moderate   #rule 5
        RETURN review

    RETURN exclude  #rule 6

END FUNCTION

## 3. Hand trace

| Variant | Gene | Depth | Quality | Impact | Rule that fires | Decision | Reason |
|---|---|---|---|---|---|---|---|
| v1 | RB1 | 9 | 90 | moderate | Rule 1 | exclude | depth 9 below min_depth 12 |
| v2 | BRCA2 | 10 | 90 | high | Rule 1 | exclude | depth 10 below min_depth 12 |
| v3 | MLH1 | 11 | 90 | moderate | Rule 1 | exclude | depth 11 below min_depth 12 |
| v4 | TP53 | 30 | 79 | low | Rule 6 | exclude | non-priority gene TP53 with low impact |
| v5 | ATM | 30 | 80 | modifier | Rule 4 | review | priority gene ATM with modifier impact |
| v6 | TP53 | 30 | 81 | high | Rule 5 | review | non-priority gene TP53 with high impact |
| v11 | PTEN | 28 | 67 | high | Rule 2 | exclude | quality 67 below min_quality 70 |
| v22 | APC | 28 | 90 | high | Rule 3 | prioritize | priority gene APC with high impact |

## 4. Test plan

- Normal case: A priority gene with high impact should return prioritize.
- Boundary case: Depth 11 should be excluded because it is below min_depth 12.
- Boundary case: Depth 12 should pass because it equals min_depth 12.
- Boundary case: Depth 13 should pass because it is above min_depth 12.
- Awkward input: Gene names with extra spaces and mixed case should still be classified correctly.
- Awkward input: An empty list passed to rank_variants() should return an empty list.
- Awkward input: rank_variants() with k larger than the number of variants should return all available variants.
- Invalid input: A non-numeric depth value should raise an exception when converted to an integer.

## 5. Work plan

- Fatin Syakirah will complete Task 1 (Design) and Task 7 (Group work, Git evidence and AI log).
- Batrisyia Amani will complete Task 2 (Triage rules) and Task 4 (Ranked top-k).
- Norhaslin will complete Task 3 (Summaries), Task 5 (CSV export and report), and Task 6 (Tests, README and code quality).
- Work will be completed in task order so that later functions can use the earlier ones.
- Each member will work on their own Git branch and commit their changes to that branch.
- Team members will review each other's code through pull requests before merging into the main branch.
- The completed program will be tested together before submission.