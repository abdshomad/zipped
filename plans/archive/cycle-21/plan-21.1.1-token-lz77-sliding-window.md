# Sub-Plan 21.1.1 — Token-LZ77 Sliding Window & Relative Pointer Codec

## Objective & Quantifiable Measure
- **Target:** Implement Token-LZ77 sliding-window compression (`services/researcher/token_lz77.py`) inspired by `ref/kuba-zip` and `ref/r-lib-zip`, scanning multi-turn agent histories and replacing recurring multi-token sequences with relative turn/token pointers `§(-turn:len)`.
- **Mechanism:** Relative back-reference resolution (`§(-2:5)` = go back 2 turns, take 5 tokens) that enables LLMs to reconstruct prior context losslessly while drastically shrinking prompt size.
- **Quantifiable Benchmark:** $\ge 80\%$ token reduction across 50-turn agent session histories with 100% exact roundtrip string restoration.

## Implementation Tasks
1. `21.1.1`: Create `TokenLZ77Codec` in `services/researcher/token_lz77.py`.
2. `21.1.2`: Implement relative turn-and-token offset encoding `§(-turn:len)` and bidirectional expander.
3. `21.1.3`: E2E 50-turn context sliding window benchmark in `tests/test_token_lz77.py` logging to `data/benchmarks.sqlite`.
