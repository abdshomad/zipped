import pytest
from services.researcher.polyglot import PolyglotInterlinguaEngine
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_multilingual_to_canonical_zlang_convergence():
    engine = PolyglotInterlinguaEngine()

    spanish = "El autor que escribe el documento escrito en el repositorio"
    french = "L'auteur qui ecrit le document ecrit dans le depot"
    german = "Der Autor der schreibt das geschriebene Dokument im Repository"
    english = "The author who writes the written document in the repository"

    z_es = engine.compress(spanish)
    z_fr = engine.compress(french)
    z_de = engine.compress(german)
    z_en = engine.compress(english)

    # All languages must converge to identical canonical 1-token Semitic Z-Lang frame
    assert z_es == "§Z[+write *write @repo]"
    assert z_fr == "§Z[+write *write @repo]"
    assert z_de == "§Z[+write *write @repo]"
    assert z_en == "§Z[+write *write @repo]"

def test_polyglot_decompression_roundtrip():
    engine = PolyglotInterlinguaEngine()
    frame = "§Z[+write *write @repo]"
    restored = engine.decompress(frame)

    assert "author writes" in restored
    assert "written document" in restored
    assert "in repository" in restored

def test_multilingual_corpus_benchmarking():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    engine = PolyglotInterlinguaEngine(db=db, bridge=bridge)

    samples = {
        "es": "El autor que escribe el documento escrito en el repositorio y el servicio de registro guarda los registros de auditoria en la base de datos",
        "fr": "L'auteur qui ecrit le document ecrit dans le depot et le service de journalisation garde les journaux d'audit dans la base de donnees",
        "de": "Der Autor der schreibt das geschriebene Dokument im Repository und der Protokollierungsdienst speichert die Audit-Protokolle in der Datenbank",
        "en": "The author who writes the written document in the repository and the logging service stores the audit logs in the database storage",
    }

    res = engine.benchmark_multilingual_corpus(samples, cycle_id=14)
    bench = res["combined_benchmarks"]

    assert bench["o200k_base"]["reduction_percent"] > 40.0
    assert bench["cl100k_base"]["reduction_percent"] > 40.0

    # Verify SQLite record
    latest = db.get_latest_metric("polyglot-zlang-tier14", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
