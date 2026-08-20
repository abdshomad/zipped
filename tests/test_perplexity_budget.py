import pytest
from services.researcher.perplexity_budget import QueryAwareBudgetAllocator
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_query_aware_budget_entropy_and_salience():
    allocator = QueryAwareBudgetAllocator()

    text_informative = "Database connection pool timeout occurred on worker cluster node 4 due to socket exhaustion."
    text_boilerplate = "Please note that all operations are subject to routine terms and conditions."

    ent_info = allocator.calculate_entropy(text_informative)
    ent_boiler = allocator.calculate_entropy(text_boilerplate)

    assert ent_info > 3.0
    assert ent_boiler > 2.0

    query = "Why did worker cluster node 4 fail with socket exhaustion?"
    sal_info = allocator.calculate_query_salience(text_informative, query)
    sal_boiler = allocator.calculate_query_salience(text_boilerplate, query)

    assert sal_info > sal_boiler
    assert sal_info >= 0.5

def test_multi_document_rag_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    allocator = QueryAwareBudgetAllocator(db=db, bridge=bridge)

    query = "What is the root cause of the memory leak in auth_service?"

    doc_relevant = (
        "Investigation Report: The root cause of the memory leak in auth_service was identified as "
        "unclosed session handles within the JWT token validation cache loop."
    )

    doc_irrelevant_1 = (
        "Marketing Guidelines: All public documentation must use standard corporate typography "
        "and brand color palettes across all release notes and website banners."
    )
    doc_irrelevant_2 = (
        "Office Logistics: The cafeteria will undergo scheduled sanitation maintenance on Friday afternoon. "
        "Please ensure all personal kitchenware is removed prior to 3 PM."
    )
    doc_irrelevant_3 = (
        "Human Resources Policy: Annual self-evaluations must be submitted through the employee portal "
        "before the end of the current fiscal quarter."
    )

    # 10 documents with 1 relevant and 9 irrelevant
    documents = [doc_relevant] + [doc_irrelevant_1, doc_irrelevant_2, doc_irrelevant_3] * 3

    res = allocator.benchmark_rag_compression(
        documents=documents,
        query=query,
        cycle_id=25,
        dataset_name="10_doc_rag_benchmark",
    )

    assert res["total_docs"] == 10
    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 70.0
    assert bench["cl100k_base"]["reduction_percent"] > 70.0

    # Ensure critical answer evidence is strictly preserved in compressed output
    comp_out = res["compressed_output"]
    assert "unclosed session handles within the JWT token validation cache loop" in comp_out
    assert query in comp_out

    # Verify SQLite logging
    latest = db.get_latest_metric("query-perplexity-tier25", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 70.0
