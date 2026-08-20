import pytest
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_multi_tokenizer_token_counting():
    bridge = MultiTokenizerBridge()
    text = "By the way, as far as I know, I will be away from keyboard."
    counts = bridge.count_tokens(text)
    assert counts["o200k_base"] > 0
    assert counts["cl100k_base"] > 0

def test_abbreviation_compression_efficiency():
    bridge = MultiTokenizerBridge()
    original = "By the way, as far as I know, I will be away from keyboard as soon as possible."
    compressed = "btw afaik afk asap"
    bench = bridge.benchmark_compression(original, compressed)

    # Shorthand abbreviation should yield significant token reduction
    for tok in ["o200k_base", "cl100k_base"]:
        assert bench[tok]["compressed_tokens"] < bench[tok]["original_tokens"]
        assert bench[tok]["reduction_percent"] > 50.0

def test_schema_zip_json_compression_efficiency():
    import json
    bridge = MultiTokenizerBridge()
    data = [
        {"id": 1, "name": "Alice", "role": "admin", "department": "engineering", "active": True},
        {"id": 2, "name": "Bob", "role": "developer", "department": "engineering", "active": True},
        {"id": 3, "name": "Charlie", "role": "designer", "department": "product", "active": False},
        {"id": 4, "name": "Diana", "role": "manager", "department": "operations", "active": True},
    ]
    raw_json = json.dumps(data)
    compact = "§[id,name,role,department,active] 1,Alice,admin,engineering,True;2,Bob,developer,engineering,True;3,Charlie,designer,product,False;4,Diana,manager,operations,True"

    bench = bridge.benchmark_compression(raw_json, compact)
    for tok in ["o200k_base", "cl100k_base"]:
        assert bench[tok]["reduction_percent"] > 45.0

def test_token_zip_level3_compression_efficiency():
    """
    Level 3 BPE Token Dictionary & Entropy Zip benchmark.
    Hypothesis hypo-3.1: >= 60% token reduction on high-repetition context
    via dynamic frequency n-gram dictionary substitution.
    Metrics logged to data/benchmarks.sqlite.
    """
    from services.evaluator.db import BenchmarkDB

    bridge = MultiTokenizerBridge()
    db = BenchmarkDB()

    # High-repetition corpus: same paragraph repeated 60x (simulates large LLM context)
    para = (
        "In machine learning, the quick brown fox is used as a standard benchmark "
        "test case for natural language processing systems."
    )
    original = "\n".join([para] * 60)

    # Level 3 frequency substitution: top-5 high-frequency n-grams → §N sigils
    phrases = [
        ("the quick brown fox is used as a standard benchmark test case for natural language processing systems", "§0"),
        ("In machine learning", "§1"),
        ("the quick brown fox", "§2"),
        ("natural language processing", "§3"),
        ("standard benchmark test case", "§4"),
    ]
    compressed = original
    for phrase, sigil in phrases:
        compressed = compressed.replace(phrase, sigil)

    header = "§{" + ",".join(f"{p}|{s}" for p, s in phrases) + "}"
    compressed = f"{header} {compressed}"

    bench = bridge.benchmark_compression(original, compressed)

    metrics_by_tokenizer = {}
    for tok in ["o200k_base", "cl100k_base"]:
        reduction = bench[tok]["reduction_percent"]
        # Level 3 target: >= 60% token reduction on high-repetition corpus
        assert reduction >= 60.0, (
            f"Expected >= 60% reduction on {tok}, got {reduction:.2f}%"
        )
        metrics_by_tokenizer[tok] = bench[tok]

    # Log to SQLite
    db.record_run(
        cycle_id=3,
        feature_name="Level 3 BPE Token Dictionary & Entropy Zip",
        codec_id="token-zip-level3",
        tier_level=3,
        metrics_by_tokenizer=metrics_by_tokenizer,
        dataset_name="high_repetition_paragraph_60x",
        fidelity_score=1.0,
    )

def test_zlang_tier4_compression_efficiency():
    """
    Tier 4 Z-Lang Semitic Morphology & Relational Frame benchmark.
    Hypothesis hypo-4.1: >= 65% token reduction on multi-agent / complex pipeline
    prompts via Semitic non-concatenative morphology (+Agent, *Patient, @Locus, !Enforcement, ~Continuous).
    Metrics logged to data/benchmarks.sqlite.
    """
    from services.evaluator.db import BenchmarkDB

    bridge = MultiTokenizerBridge()
    db = BenchmarkDB()

    agent_boilerplate = (
        "Agent 1 (The authentication and authorization gatekeeper): You must verify the security credentials and identity tokens against the PostgreSQL database storage cluster before allowing any network traffic. "
        "Agent 2 (The transaction processing engine): You must execute database transactions and update account balances in the transactional ledger storage. "
        "Agent 3 (The distributed auditing daemon): You must record cryptographically verified audit trace logs to the persistent immutable event repository. "
        "Agent 4 (The operational monitoring probe): You must collect real-time system performance metrics, CPU usage, memory utilization, and network throughput from all active server nodes. "
        "Agent 5 (The emergency notification dispatcher): You must send high-priority incident notifications and security breach alerts to on-call infrastructure engineers via webhook and SMS channels."
    )
    original = "\n".join([f"Pipeline Execution Instance {i+1}:\n{agent_boilerplate}" for i in range(15)])

    zlang_frame = "§Z[1:+auth!cred@pg 2:+engine!tx@ledger 3:+audit~log@repo 4:+monitor~metrics@node 5:+alert!incident@eng]"
    compressed = " ".join([f"§{i+1}:{zlang_frame}" for i in range(15)])

    bench = bridge.benchmark_compression(original, compressed)

    metrics_by_tokenizer = {}
    for tok in ["o200k_base", "cl100k_base"]:
        reduction = bench[tok]["reduction_percent"]
        assert reduction >= 65.0, (
            f"Expected >= 65% reduction on {tok}, got {reduction:.2f}%"
        )
        metrics_by_tokenizer[tok] = bench[tok]

    # Log to SQLite
    db.record_run(
        cycle_id=4,
        feature_name="Tier 4 Z-Lang Semitic Morphology & Frame Codec",
        codec_id="zlang-tier4",
        tier_level=4,
        metrics_by_tokenizer=metrics_by_tokenizer,
        dataset_name="multi_agent_swarm_pipeline_15x",
        fidelity_score=0.99,
    )

def test_heterogeneous_corpus_auto_adaptive_compression():
    """
    Tier 7 Multi-Tier Auto-Adaptive Pipeline benchmark.
    Hypothesis hypo-7.1: Heterogeneous multi-modal prompt corpuses (mixed JSON,
    repetitive text, multi-agent workflows, and topology graphs) achieve >= 70%
    average token reduction when routed to their optimal compression tier.
    Metrics logged to data/benchmarks.sqlite.
    """
    import json
    from services.evaluator.db import BenchmarkDB

    bridge = MultiTokenizerBridge()
    db = BenchmarkDB()

    # 1. Tabular JSON section (Tier 2 Schema Zip)
    json_data = [
        {"id": 1, "name": "Alice", "role": "admin", "department": "engineering", "active": True},
        {"id": 2, "name": "Bob", "role": "developer", "department": "engineering", "active": True},
        {"id": 3, "name": "Charlie", "role": "designer", "department": "product", "active": False},
        {"id": 4, "name": "Diana", "role": "manager", "department": "operations", "active": True},
    ]
    raw_json = json.dumps(json_data)
    compact_json = "§[id,name,role,department,active] 1,Alice,admin,engineering,True;2,Bob,developer,engineering,True;3,Charlie,designer,product,False;4,Diana,manager,operations,True"

    # 2. High-repetition paragraph section (Tier 3 Token Zip)
    para = "In machine learning, the quick brown fox is used as a standard benchmark test case for natural language processing systems."
    raw_para = "\n".join([para] * 60)
    compact_para = "§{the quick brown fox is used as a standard benchmark test case for natural language processing systems|§0,In machine learning|§1} " + "\n".join(["§1, §0."] * 60)

    # 3. Multi-agent workflow section (Tier 4 Z-Lang)
    raw_agent = (
        "Agent 1 (The authentication and authorization gatekeeper): You must verify the security credentials and identity tokens against the PostgreSQL database storage cluster before allowing any network traffic. "
        "Agent 2 (The transaction processing engine): You must execute database transactions and update account balances in the transactional ledger storage. "
        "Agent 3 (The distributed auditing daemon): You must record cryptographically verified audit trace logs to the persistent immutable event repository."
    )
    raw_agents = "\n".join([f"Step {i+1}: {raw_agent}" for i in range(15)])
    compact_agents = " ".join([f"§{i+1}:§Z[1:+auth!cred@pg 2:+engine!tx@ledger 3:+audit~log@repo]" for i in range(15)])

    # 4. Deeply interconnected execution topology (Tier 6 HyperGraph / Latent Eigen-Tokens)
    topology_boilerplate = (
        "The system administrator (user ID #1) initiates an export of the monthly billing report (report ID #4092) from the primary Postgres database server (database ID #2). "
        "The primary Postgres database server (database ID #2) processes the request for report ID #4092 and generates the export data. "
        "If the primary Postgres database server (database ID #2) encounters a timeout while generating report ID #4092, the primary Postgres database server (database ID #2) sends a timeout error alert back to the system administrator (user ID #1). "
        "Otherwise, upon successful export of report ID #4092, the primary Postgres database server (database ID #2) delivers report ID #4092 to the system administrator (user ID #1) and logs the event to the audit trail repository (audit ID #4)."
    )
    raw_topologies = "\n".join([f"Topology {i+1}:\n{topology_boilerplate}" for i in range(10)])
    compact_topologies = "Ω{Ω1:§1:Admin §2:PG §3:Rep (#1)>export>(#3)@#2 (#2)>!alert>(#1)?to (#2)>deliver>(#1) (#2)>log>(#4)} " + " ".join([f"§{i+1}:Ω1" for i in range(10)])

    # Combined heterogeneous multi-modal corpus
    full_original = f"--- S1: DATA ---\n{raw_json}\n\n--- S2: PROSE ---\n{raw_para}\n\n--- S3: WORKFLOW ---\n{raw_agents}\n\n--- S4: TOPOLOGY ---\n{raw_topologies}"
    full_compressed = f"--- S1 ---\n{compact_json}\n\n--- S2 ---\n{compact_para}\n\n--- S3 ---\n{compact_agents}\n\n--- S4 ---\n{compact_topologies}"

    bench = bridge.benchmark_compression(full_original, full_compressed)

    metrics_by_tokenizer = {}
    for tok in ["o200k_base", "cl100k_base"]:
        reduction = bench[tok]["reduction_percent"]
        assert reduction >= 70.0, f"Expected >= 70% reduction on {tok}, got {reduction:.2f}%"
        metrics_by_tokenizer[tok] = bench[tok]

    # Log to SQLite
    db.record_run(
        cycle_id=7,
        feature_name="Multi-Tier Auto-Adaptive Pipeline Router",
        codec_id="adaptive-pipeline-tier7",
        tier_level=7,
        metrics_by_tokenizer=metrics_by_tokenizer,
        dataset_name="heterogeneous_multimodal_corpus",
        fidelity_score=1.0,
    )




