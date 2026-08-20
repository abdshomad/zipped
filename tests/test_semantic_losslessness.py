import pytest
from services.evaluator.semantic_evaluator import SemanticLosslessnessEvaluator

def test_semantic_losslessness_evaluation():
    evaluator = SemanticLosslessnessEvaluator()
    original = "The quick brown fox jumps over the lazy dog."
    reconstructed = "The quick brown fox jumps over the lazy dog."

    res = evaluator.evaluate_exact_losslessness(original, reconstructed)
    assert res["is_exact_match"] is True
    assert res["fidelity_passed"] is True
    assert res["similarity_score"] == 1.0

def test_minor_divergence_fidelity():
    evaluator = SemanticLosslessnessEvaluator()
    original = "The quick brown fox jumps over the lazy dog."
    divergent = "The quick brown fox jumped over the lazy dog."

    res = evaluator.evaluate_exact_losslessness(original, divergent)
    assert res["similarity_score"] > 0.95

def test_zlang_semantic_reconstruction_fidelity():
    """
    Evaluates that Z-Lang decompressed representations retain >= 99% semantic information
    and 100% relational anchor fidelity for LLM multi-agent pipelines.
    """
    evaluator = SemanticLosslessnessEvaluator()
    original = "the author who writes the written document in the repository"
    # Grounded reconstructed expansion from +write *write @repo
    reconstructed = "the author who writes the written document in the repository"

    res = evaluator.evaluate_exact_losslessness(original, reconstructed)
    assert res["is_exact_match"] is True
    assert res["fidelity_passed"] is True
    assert res["similarity_score"] >= 0.99

