import pytest
from services.researcher.battle_royale import ShannonEntropyEstimator, BattleRoyaleMatchmaker, BattleRoyaleStrategy
from services.researcher.arena import TokenGenome
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_shannon_entropy_calculations():
    estimator = ShannonEntropyEstimator()
    repetitive = "AAAAAAAAAA"
    varied = "abcdefghijklmnopqrstuvwxyz 0123456789"

    h_rep = estimator.compute_entropy(repetitive)
    h_var = estimator.compute_entropy(varied)

    assert h_rep == 0.0
    assert h_var > 4.5

    redundancy = estimator.compute_theoretical_compression_limit(repetitive)
    assert redundancy == 1.0

def test_battle_royale_match_and_elo_update():
    matchmaker = BattleRoyaleMatchmaker()
    para = "In machine learning and artificial intelligence, natural language processing systems benchmark deep neural network token reduction models."
    corpus = "\n".join([para] * 20)

    strat_a = BattleRoyaleStrategy("dense_a", TokenGenome("g_a", {
        "natural language processing systems": "§0",
        "In machine learning and artificial intelligence": "§1",
        "deep neural network token reduction models": "§2",
    }))
    strat_b = BattleRoyaleStrategy("sparse_b", TokenGenome("g_b", {}))

    red_a, red_b = matchmaker.play_match(strat_a, strat_b, corpus)
    assert red_a > red_b
    assert strat_a.elo > 1200.0
    assert strat_b.elo < 1200.0
    assert strat_a.wins == 1
    assert strat_b.losses == 1

def test_battle_royale_tournament_execution():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    matchmaker = BattleRoyaleMatchmaker(db=db, bridge=bridge)

    para = "The system administrator initiates an export of the monthly billing report from the primary Postgres database server."
    corpus = "\n".join([para] * 30)

    strategies = [
        BattleRoyaleStrategy("elite_top", TokenGenome("g1", {
            "The system administrator initiates": "§0",
            "monthly billing report": "§1",
            "primary Postgres database server": "§2",
        })),
        BattleRoyaleStrategy("mid_tier", TokenGenome("g2", {
            "monthly billing report": "§1",
        })),
        BattleRoyaleStrategy("seed_base", TokenGenome("g3", {
            "primary Postgres database server": "§2",
        })),
        BattleRoyaleStrategy("baseline_null", TokenGenome("g4", {})),
    ]

    result = matchmaker.run_tournament(strategies, corpus, rounds=2, cycle_id=12)

    assert result["champion_id"] == "elite_top"
    assert result["champion_elo"] > 1200.0
    assert len(result["rankings"]) == 4

    # Verify SQLite logging
    latest = db.get_latest_metric("battle-royale-tier12", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 30.0
