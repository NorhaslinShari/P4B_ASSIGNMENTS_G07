"""Assignment 1 - clinical variant triage service (synthetic teaching data only).

Reads variant calls, applies ordered triage rules with named thresholds, records a
reason for every decision and produces summaries, a ranked top-k list, a CSV text
and a short text report. Nothing here is clinical advice.
"""
import csv
import json
import sys
from pathlib import Path

DECISIONS = ("prioritize", "review", "exclude")
IMPACT_ORDER = ("high", "moderate", "low", "modifier")
PRIORITY_IMPACTS = frozenset({"high", "moderate"})
CSV_COLUMNS = [
    "variant", "gene", "chrom", "pos", "depth", "quality", "impact", "decision", "reason",
]
CLI_ARGUMENTS = 3


def load_variants(path) -> list[dict]:
    """Read variants.csv into a list of dicts. Every value stays text (Week 6 explains how)."""
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_params(path) -> dict:
    """Read the group parameters (data/params.json) into a dict."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def classify_variant(row: dict, params: dict) -> tuple[str, str]:
    """Return (decision, reason) for one variant row.

    Rules run in this order and the first rule that fires decides:
      1. depth < params["min_depth"]                      -> exclude (low depth)
      2. quality < params["min_quality"]                  -> exclude (low quality)
      3. priority gene and impact high or moderate        -> prioritize
      4. priority gene and impact low or modifier         -> review
      5. other gene and impact high or moderate           -> review
      6. other gene and impact low or modifier            -> exclude
    Gene symbols and impact labels are compared after strip() and case folding.
    depth, quality and pos may arrive as text.
    """
    min_depth = int(params.get("min_depth", 10))
    min_quality = int(params.get("min_quality", 80))
    depth = int(row["depth"])
    quality = int(row["quality"])
    gene = str(row.get("gene", row.get("gene_symbol", ""))).strip()
    impact = str(row.get("impact", "")).strip()

    if depth < min_depth:
        return "exclude", f"low depth {depth} threshold {min_depth}"

    if quality < min_quality:
        return "exclude", f"low quality {quality} threshold {min_quality}"

    raw_impacts = params.get("priority_impacts", ["high", "moderate"])
    priority_impacts = {i.lower() for i in raw_impacts}
     
    raw_panel_genes = params.get("panel_genes", params.get("priority_genes", None))
    panel_genes = {g.lower() for g in raw_panel_genes} if raw_panel_genes is not None else None

    if panel_genes is not None and gene.lower() in panel_genes:
        return "prioritize", f"panel_gene gene {gene}"
    elif impact.lower() in priority_impacts:
        return "prioritize", f"prioritize_impact impact {impact} gene {gene}"
    else:
        return "review", f"review_impact impact {impact} gene {gene}"


def triage(rows: list[dict], params: dict) -> list[dict]:
    """Classify every row. Returns NEW dicts (row fields plus decision and reason), same order.

    The input rows and params are never modified.
    """
    results = []
    for row in rows:
        decision, reason = classify_variant(row, params)
        new_row = row.copy()
        new_row["decision"] = decision
        new_row["reason"] = reason
        results.append(new_row)
    return results


def decision_counts(results: list[dict]) -> dict[str, int]:
    """Number of results per decision; keys are always prioritize, review, exclude (in order)."""
    count = { "prioritize": 0, "review": 0, "exclude": 0,} 
    for result in results:
        decision = result["decision"] #specific to decision in results = decision : prioritize
        count[decision] += 1 # add 1 to prioritize

    return count


def impact_counts(results: list[dict]) -> dict[str, int]:
    """Impact counts over variants that were NOT excluded.

    Keys are always high, moderate, low, modifier (in that order), zeros included.
    """
    count = { "high": 0, "moderate": 0, "low": 0, "modifier": 0}
    for result in results:
        if result["decision"] != "exclude":
            impact = result["impact"]
            count[impact] += 1 

    return count # same with decision_count

def gene_summary(results: list[dict]) -> dict[str, dict]:
    """Per-gene summary, genes in alphabetical order.

    Each value is {"total": n, "prioritize": a, "review": b, "exclude": c, "mean_depth": d}
    where mean_depth is the mean depth of ALL the gene's variants, rounded to 1 decimal.
    """
    # result untuk tiap gene
    if results == []:
        return {}
    
    summary = {}
    for result in results:
        gene = result["gene"]

        if gene not in summary: #initialize
            summary[gene] = {
                "total": 0, "prioritize": 0, "review": 0, 
                "exclude": 0, "sum_depth": 0
            }

        summary[gene]["total"] += 1 # if exist gene dlm summary then proceed count 
        summary[gene][result["decision"]] += 1
        summary[gene]["sum_depth"] += result["depth"]

    gene_summarize = {}

    for gene in sorted(summary): #sort kan gene
        total = summary[gene]["total"]  #already store value
        depth = summary[gene]["sum_depth"]

        gene_summarize[gene]= {"total": total, "prioritize": summary[gene]["prioritize"],
                                "review": summary[gene]["review"], "exclude": summary[gene]["exclude"],
                                "mean_depth":round(depth/total, 1)}
    return gene_summarize


def rank_variants(results: list[dict], k: int) -> list[dict]:
    """Top k variants that were not excluded, best first.

    Sort by: prioritize before review, then impact (high first), then higher quality,
    then higher depth, then smaller pos. Fewer than k are returned if fewer qualify.

    Raises:
        ValueError: if k is negative.
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    filtered_results = [r for r in results if r["decision"] != "exclude"]

    sorted_results = sorted(
        filtered_results,
        key=lambda r: (
            0 if r.get("decision") == "prioritize" else 1,   
            -int(r.get("quality", 0)),                
            -int(r.get("depth", 0)),                  
            int(r.get("pos", 0))                     
        )
    )

    return sorted_results[:k]


def results_to_csv(results: list[dict]) -> str:
    """CSV text: a header line (CSV_COLUMNS) and one line per result in the given order.

    Every line ends with a newline. Reason text contains no commas, so no quoting is needed.
    """
    header_line = [",".join(CSV_COLUMNS)]
    for result in results:
        row = ",".join(str(result[column]) for column in CSV_COLUMNS)
        header_line.append(row) # heaedr_line append new row (only list can append!)

    return "\n".join(header_line) + "\n" # add both end


def build_report(results: list[dict], params: dict) -> str:
    """Short text report; the line formats are fixed so the report can be checked.

    Lines: title, 'Thresholds: min_depth=D min_quality=Q', 'Priority genes: A, B, ...',
    'Variants: N', one 'decision: count' line per decision, a blank line,
    'Top K variants' and then 'rank. variant | gene | impact | decision' lines.
    """
    count = decision_counts(results)

    report = [
    "Variant triage report (synthetic teaching data)",
    f"Thresholds: min_depth={params['min_depth']} min_quality={params['min_quality']}",
    f"Priority genes: {', '.join(params['priority_genes'])}",
    f"Variants: {len(results)}",
    f"prioritize: {count['prioritize']}",
    f"review: {count['review']}",
    f"exclude: {count['exclude']}", "", # add blank line ikot mcm exp report
    f"Top {params['top_k']} variants", ]

    top = rank_variants(results, params["top_k"])
    for i, variant in enumerate(top, start=1):
        report.append(f"{i}. {variant['variant']} | {variant['gene']} | {variant['impact']} | {variant['decision']}" )

    return "\n".join(report) + "\n"

def main(argv: list[str] | None = None) -> int:
    """Command line: python src/a1_triage.py VARIANTS_CSV PARAMS_JSON OUT_DIR."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != CLI_ARGUMENTS:
        print("usage: python src/a1_triage.py data/variants.csv data/params.json results")
        return 2
    variants_path, params_path, out_dir = args
    rows = load_variants(variants_path)
    params = load_params(params_path)
    results = triage(rows, params)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "triage.csv").write_text(results_to_csv(results), encoding="utf-8")
    report = build_report(results, params)
    (out / "report.txt").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
