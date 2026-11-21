import pytest 

from a1_triage import (
    CSV_COLUMNS,
    classify_variant,
    decision_counts,
    rank_variants,
    results_to_csv,
    triage,
)

PARAMS = {"min_depth": 10, "min_quality": 80, "priority_genes": ["BRCA1", "TP53"], "top_k": 3}

def row(variant="v1", gene="BRCA1", depth=40, quality=95, impact="high", pos=1000):
    return {"variant": variant, "gene": gene, "chrom": "17", "pos": str(pos), "depth": str(depth),
            "quality": str(quality), "impact": impact}

def test_normal_case_priority():
    assert classify_variant(row(), PARAMS)[0] == "prioritize"
    

def test_boundary_depth_below_threshold():
    decision, reason = classify_variant(row(depth=8), PARAMS)

    assert decision == "exclude"
    assert reason == "low depth"

def test_boundary_depth_at_threshold():
    decision, reason = classify_variant(row(depth=10), PARAMS)

    assert decision == "prioritize"

def test_boundary_depth_above_threshold():
    decision, reason = classify_variant(row(depth=11),PARAMS)

    assert decision == "prioritize"

def test_messy_text_input():
    assert classify_variant(row(gene="BRCA3", depth="40", quality="95"), PARAMS)[0] == "prioritize" 

def test_empty_list_rank_variants():
    assert rank_variants([], PARAMS["top_k"]) == []

def test_k_lsrger_than_data():
    variants = [
        {"variant": "v1", "score": 10},
        {"variant": "v2", "score": 20},
    ]
    result = rank_variants(variants, 10) # k is 10 (larger than data)
    assert len(result) == 2

def test_invalid_input_test():
    with pytest.raises(ValueError):
        classify_variant(row(depth="adbs"), PARAMS)
    

