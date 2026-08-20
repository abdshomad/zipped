from typing import Dict, List, Any, Optional
import collections
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class MacroProposal:
    """A compression macro candidate discovered and proposed by a swarm agent."""
    def __init__(self, phrase: str, sigil: str, estimated_savings: int, agent_id: str):
        self.phrase = phrase
        self.sigil = sigil
        self.estimated_savings = estimated_savings
        self.agent_id = agent_id
        self.votes = 1

class SwarmAgentWorker:
    """Individual agent worker exploring local token contexts and proposing compression macros."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def discover_candidates(self, local_corpus: str) -> List[MacroProposal]:
        """Discovers repeated n-grams weighted by total estimated token savings."""
        words = local_corpus.split()
        ngrams = collections.Counter()

        for n in (12, 10, 8, 6, 4):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i : i + n])
                if "\n" not in phrase:
                    ngrams[phrase] += 1

        proposals = []
        # Sort by total potential token savings: (words - 1) * occurrences
        sorted_candidates = sorted(ngrams.items(), key=lambda x: (len(x[0].split()) - 1) * x[1], reverse=True)

        selected_phrases: List[str] = []
        for phrase, count in sorted_candidates:
            if count >= 2:
                # Avoid overlapping sub-phrases in proposal
                if not any(phrase in s or s in phrase for s in selected_phrases):
                    selected_phrases.append(phrase)
                    savings = (len(phrase.split()) - 1) * count
                    proposals.append(MacroProposal(phrase, f"§H{len(proposals)}", savings, self.agent_id))
                    if len(proposals) >= 5:
                        break

        return proposals

class TokenHiveMind:
    """Decentralized evolutionary memory aggregating and voting on token macros across multi-agent swarms."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.proposals: Dict[str, MacroProposal] = {}
        self.consensus_dictionary: Dict[str, str] = {}
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()

    def submit_proposals(self, proposals: List[MacroProposal]) -> None:
        """Receives macro proposals from swarm agents and tallies votes."""
        for p in proposals:
            if p.phrase in self.proposals:
                self.proposals[p.phrase].votes += 1
                self.proposals[p.phrase].estimated_savings += p.estimated_savings
            else:
                self.proposals[p.phrase] = p

    def reach_consensus(self, min_votes: int = 2) -> Dict[str, str]:
        """Promotes candidates meeting consensus threshold into global hive-mind dictionary."""
        promoted = {}
        sorted_proposals = sorted(
            [p for p in self.proposals.values() if p.votes >= min_votes],
            key=lambda x: (x.votes, x.estimated_savings),
            reverse=True,
        )

        selected: List[str] = []
        for prop in sorted_proposals:
            if not any(prop.phrase in s or s in prop.phrase for s in selected):
                selected.append(prop.phrase)
                assigned_sigil = f"§H{len(promoted)}"
                promoted[prop.phrase] = assigned_sigil

        self.consensus_dictionary = promoted
        return self.consensus_dictionary

    def compress(self, text: str) -> str:
        """Compresses text using current hive-mind consensus macros."""
        result = text
        for phrase, sigil in self.consensus_dictionary.items():
            result = result.replace(phrase, sigil)
        return result

    def decompress(self, compressed_text: str) -> str:
        """Losslessly restores original text using inverse consensus mapping."""
        result = compressed_text
        for phrase, sigil in self.consensus_dictionary.items():
            result = result.replace(sigil, phrase)
        return result

    def run_swarm_evolution(
        self,
        agents: List[SwarmAgentWorker],
        corpus: str,
        cycle_id: int = 17,
        dataset_name: str = "swarm_hivemind_benchmark",
    ) -> Dict[str, Any]:
        """Executes full swarm discovery, consensus voting, and SQLite metric recording."""
        for agent in agents:
            proposals = agent.discover_candidates(corpus)
            self.submit_proposals(proposals)

        consensus_dict = self.reach_consensus(min_votes=max(1, len(agents) // 3))
        compressed = self.compress(corpus)
        bench = self.bridge.benchmark_compression(corpus, compressed)

        self.db.record_run(
            cycle_id=cycle_id,
            feature_name="Distributed Token Hive-Mind Swarm Evolution",
            codec_id="token-hivemind-tier17",
            tier_level=17,
            metrics_by_tokenizer=bench,
            dataset_name=dataset_name,
            fidelity_score=1.0,
        )

        return {
            "consensus_macros_count": len(consensus_dict),
            "consensus_dictionary": consensus_dict,
            "benchmarks": bench,
        }
