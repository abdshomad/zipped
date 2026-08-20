from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import string
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class ContinuousLearningEngine:
    """In-context autonomous learning engine mining repeating dialogue patterns to dynamically mint persistent codecs."""

    AVAILABLE_SIGILS = [f"§{c}" for c in string.digits + string.ascii_letters + "!@#$%^&*+-~"]

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None, min_frequency: int = 2):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()
        self.min_frequency = min_frequency
        self.phrase_counter: Counter = Counter()
        self.learned_rules: Dict[str, str] = {}
        self.reverse_rules: Dict[str, str] = {}

    def _extract_ngrams(self, text: str, min_words: int = 3, max_words: int = 15) -> List[str]:
        words = text.strip().split()
        ngrams = []
        for n in range(min(max_words, len(words)), min_words - 1, -1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i : i + n])
                if len(phrase) > 10:
                    ngrams.append(phrase)
        return ngrams

    def observe(self, turn_text: str) -> None:
        """Observes a turn, updates recurring phrase frequencies, and dynamically mints new 1-token sigils."""
        ngrams = self._extract_ngrams(turn_text)
        for ng in ngrams:
            self.phrase_counter[ng] += 1

        # Re-evaluate top candidates sorted by word length and frequency
        top_candidates = sorted(
            [p for p, count in self.phrase_counter.items() if count >= self.min_frequency],
            key=lambda x: (len(x.split()), self.phrase_counter[x]),
            reverse=True,
        )

        for phrase in top_candidates:
            if phrase not in self.learned_rules and len(self.learned_rules) < len(self.AVAILABLE_SIGILS):
                sigil = self.AVAILABLE_SIGILS[len(self.learned_rules)]
                self.learned_rules[phrase] = sigil
                self.reverse_rules[sigil] = phrase

    def compress(self, text: str) -> str:
        """Compresses text using the current active learned dictionary."""
        res = text
        for phrase, sigil in sorted(self.learned_rules.items(), key=lambda x: len(x[0]), reverse=True):
            res = res.replace(phrase, sigil)
        return res

    def decompress(self, text: str) -> str:
        """Losslessly recovers original text from learned sigils."""
        res = text
        for sigil, phrase in self.reverse_rules.items():
            res = res.replace(sigil, phrase)
        return res

    def benchmark_continuous_stream(
        self,
        turns: List[str],
        cycle_id: int = 29,
        dataset_name: str = "continuous_agent_dialogue_stream",
    ) -> Dict[str, Any]:
        """Runs progressive streaming benchmark across turns, mining patterns and logging to BenchmarkDB."""
        for turn in turns:
            self.observe(turn)

        raw_all = "\n\n".join(turns)
        comp_all = self.compress(raw_all)
        restored = self.decompress(comp_all)
        assert restored == raw_all, "Lossless invariant violated!"

        bench = self.bridge.benchmark_compression(raw_all, comp_all)

        self.db.record_run(
            cycle_id=cycle_id,
            feature_name="Continuous In-Context Autonomous Learning Engine & Perpetual Codec Registry",
            codec_id="continuous-learning-tier29",
            tier_level=29,
            metrics_by_tokenizer=bench,
            dataset_name=dataset_name,
            fidelity_score=1.0,
        )

        return {
            "total_turns": len(turns),
            "learned_rules_count": len(self.learned_rules),
            "benchmarks": bench,
        }
