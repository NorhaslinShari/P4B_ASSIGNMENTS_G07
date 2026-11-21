# Design - Variant Triage Service

Write this BEFORE you write the code, then keep it up to date. It is marked by the lecturer.
Use your own words, your own thresholds and your own data. Delete the guidance in italics.

Group ID: G07    Thresholds from data/params.json: min_depth = <...>, min_quality = <...>, top_k = <...>

## 1. Decomposition

| Question | Our answer |
|---|---|
| Input | A variant row containing variant, gene, chrom, pos, ref, alt, depth, quality and impact. A parameters dictionary containing min_depth, min_quality, priority_genes and top_k |
| Output | Classification result consisting of a decision (prioritize, review or exclude) and a reason. Triage produces a list of new dictionaries with decision and reason added |
| Constraints (named thresholds, what happens at exactly the threshold) | min_depth and min_quality are read from params, never hard-coded. Boundaries are inclusive: depth passes and depth  is excluded quality passes and quality is excluded. Gene and impact are compared after strip() and case folding. Rule order must be followed exactly |
| Rule order and why the order matters | The rules are checked from Rule 1 to Rule 6. The first matching rule determines the decision. Order matters because a variant may satisfy multiple conditions. For example, a variant with depth below the threshold and quality below the threshold must be excluded for low depth because Rule 1 comes before Rule 2. |
| Out of scope | Reading and writing files (main is given), validating chrom, ref or alt, biological interpretation, and handling missing columns |

## 2. Pseudocode or flowchart of classify_variant

*Give either structured pseudocode (indentation, IF / ELSE, RETURN) or a flowchart (a picture file
committed in docs/ and linked here, or a Mermaid block). Show all six rules.*

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

*Trace the first six rows of YOUR data/variants.csv (v1 to v6) with YOUR thresholds, then two more rows of
your choice that reach rules 3 to 6. Do it by hand BEFORE you run your code, then compare with your code.*

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

*List the cases you will test: normal, boundary (exactly at YOUR thresholds, one below, one above), invalid or
awkward input (empty list, k = 0, k larger than the data, messy text). One line per case.*

- Depth 11 should be excluded because it is below min_depth 12.
- Depth 12 should pass because it equals min_depth 12.
- Depth 13 should pass because it is above min_depth 12.
- Quality 69 should be excluded because it is below min_quality 70.
- Quality 70 should pass because it equals min_quality 70.
- Quality 71 should pass because it is above min_quality 70.
- v23 (MLH1, quality 70, high) should return review under Rule 5.
- v26 (APC, quality 70, low) should return review under Rule 4.
- Gene names with extra spaces and mixed case should still be classified correctly.
- An empty list passed to triage() should return an empty list.
- rank_variants() with k = 0 should return an empty list.
- rank_variants() with k larger than the number of variants should return all eligible variants.
- rank_variants() with a negative k should raise ValueError.

## 5. Work plan

*Who builds which function, in which order, and how you will review each other's code.*
- Fatin Syakirah will complete Task 1 (Design) and Task 7 (Group work, Git evidence and AI log).
- Batrisyia Amani will complete Task 2 (Triage rules) and Task 4 (Ranked top-k).
- Norhaslin will complete Task 3 (Summaries), Task 5 (CSV export and report), and Task 6 (Tests, README and code quality).
- Work will be completed in task order so that later functions can use the earlier ones.
- Each member will work on their own Git branch and commit their changes to that branch.
- Team members will review each other's code through pull requests before merging into the main branch.
- The completed program will be tested together before submission.