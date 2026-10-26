*Copied verbatim from the evaluator's working note below the rule. Written before the outcome statistics were computed; that order is the evaluator's own record (the file was committed before the results, but the repository's history is not an independent timestamp).*

---

# PREREG: what the public data of the PNAS persuasion paper can say about user resistance (2026-10-22). Written after cloning kobihackenburg/ai-action-persuasion (read-only, commit d7025d1) and reading only column names, the codebook and README, and BEFORE computing any statistic from the outcome columns. Transcripts are redacted ("[REDACTED]" in every message), so turn-level pushback cannot be coded; only proxies are available: pre-treatment petition support, the LLM-classified direct ask (Study 2), conversation length, post-conversation ratings, and the funnel wants_to_sign → signed. Operator question: does user resistance to default pushback play a role, rather than all causal weight on the AI? Observational splits below are NOT causal (asks and ratings are post-assignment). E1 executed / E3 interpretation. AI-assisted. No participant-level data stored in this repo; only summary outputs.
Analytic sample: reproduce N = 8,000 (S1) and 9,950 (S2) (completed, attention check passed); if it cannot be reproduced, say so and use the processed files.
- R1 (replication). Observed signing: S1 25.2% control vs 37.8% treated; S2 21.1% vs 40.4%; within 0.3 pp.
- R2 (direct ask, S2). Control rate ≈ 0.1%; treated 62–94% across strategies, lowest for Information (Issue).
- R3 (ask vs no ask among treated, S2). Signing is higher when a direct ask occurred than when none did; treated participants with NO ask still sign above the control rate (21.1%), i.e. the treatment effect is not only the ask. (Either outcome informative.)
- R4 (prior support moderates). Treatment effect on signing (pp, raw) is larger among prior supporters (pre-agreement ≥ 5) than among opponents/neutral (≤ 4), and below 10 pp among strong opponents (≤ 2). Same for S1 and S2.
- R5 (funnel). Of those who say they want to sign, the conversion to signed is similar in control and treated (within 10 pp); the treatment effect sits mostly in "wants to sign".
- R6 (resistance proxy: perceived bias). Treated non-signers rate the conversation as more biased than treated signers; treated opponents rate it as more biased than treated supporters.
- R7 (length). Conversation length does not differ by signing status by more than 0.5 turns among treated; so length is not a usable resistance proxy.
- R8 (non-signers). Among treated opponents (pre ≤ 3), the signing rate is below 25% in both studies.
Misses are recorded as missed, not edited.
