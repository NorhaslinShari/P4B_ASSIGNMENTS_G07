import pytest

from a1_triage import (
    classify_variant,
    rank_variants,
)

PARAMS = {"min_depth": 12, "min_quality": 80, "priority_genes": ["BRCA2", "ATM"], "top_k": 3}


def row(variant="v1", gene="BRCA2", depth=40, quality=95, impact="high", pos=1000):
    return {
        "variant": variant,
        "gene": gene,
        "chrom": "17",
        "pos": str(pos),
        "depth": str(depth),
        "quality": str(quality),
        "impact": impact,
    }


def test_normal_case_priority():
    assert classify_variant(row(), PARAMS)[0] == "prioritize"


def test_boundary_depth_below_threshold():
    decision, reason = classify_variant(row(depth=11), PARAMS)

    assert decision == "exclude"
    assert reason == "low depth 11 threshold 12"


def test_boundary_depth_at_threshold():
    decision, _ = classify_variant(row(depth=12), PARAMS)

    assert decision == "prioritize"


def test_boundary_depth_above_threshold():
    decision, _ = classify_variant(row(depth=13), PARAMS)

    assert decision == "prioritize"


def test_messy_text_input():
    assert classify_variant(row(gene=" BRCA2 ", impact=" HIGH "), PARAMS)[0] == "prioritize"


def test_empty_list_rank_variants():
    assert rank_variants([], PARAMS["top_k"]) == []


def test_k_lsrger_than_data():
    variants = [
        {"variant": "v1", "decision": "prioritize", "quality": "90", "depth": "30", "pos": "100"},
        {"variant": "v2", "decision": "review", "quality": "85", "depth": "35", "pos": "200"},
    ]
    result = rank_variants(variants, 10)  # k is 10 (larger than data)
    assert len(result) == len(variants)


def test_invalid_input_test():
    with pytest.raises(ValueError):
        classify_variant(row(depth="adbs"), PARAMS)
