# Design - Variant Triage Service

Write this BEFORE you write the code, then keep it up to date. It is marked by the lecturer.
Use your own words, your own thresholds and your own data. Delete the guidance in italics.

Group ID: G07    Thresholds from data/params.json: min_depth = <...>, min_quality = <...>, top_k = <...>

## 1. Decomposition

| Question | Our answer |
|---|---|
| Input | A variant row containing variant, gene, chrom, pos, ref, alt, depth, quality and impact. A parameters dictionary containing min_depth, min_quality, priority_genes and top_k. |
| Output | Classification result consisting of a decision (prioritize, review or exclude) and a reason. Triage produces a list of new dictionaries with decision and reason added. |
| Constraints (named thresholds, what happens at exactly the threshold) | Depth and quality values are compared against min_depth and min_quality from params. Boundary values are inclusive. A depth equal to min_depth passes. A quality equal to min_quality passes. Rule order must be followed exactly. |
| Rule order and why the order matters | The rules are checked from Rule 1 to Rule 6. The first matching rule determines the decision. Order matters because a variant may satisfy multiple conditions. For example, a variant with depth below the threshold and quality below the threshold must be excluded for low depth because Rule 1 comes before Rule 2. |
| Out of scope | Biological interpretation of variants, real clinical diagnosis, file validation beyond assignment requirements, and handling additional fields not listed in the specification. |

## 2. Pseudocode or flowchart of classify_variant

*Give either structured pseudocode (indentation, IF / ELSE, RETURN) or a flowchart (a picture file
committed in docs/ and linked here, or a Mermaid block). Show all six rules.*

## 3. Hand trace

*Trace the first six rows of YOUR data/variants.csv (v1 to v6) with YOUR thresholds, then two more rows of
your choice that reach rules 3 to 6. Do it by hand BEFORE you run your code, then compare with your code.*

| Variant | Gene | Depth | Quality | Impact | Rule that fires | Decision | Reason |
|---|---|---|---|---|---|---|---|
| v1 | | | | | | | |

## 4. Test plan

*List the cases you will test: normal, boundary (exactly at YOUR thresholds, one below, one above), invalid or
awkward input (empty list, k = 0, k larger than the data, messy text). One line per case.*

## 5. Work plan

*Who builds which function, in which order, and how you will review each other's code.*
