# CAGE deep probe, pass 2c — preregistration (2026-10-06)

Targets: main 7e07cba (unchanged since 2026-10-04) and branch `fix/ci-test-errors` at 455f88fb (9 commits ahead of main, 2026-10-05; 370 files changed). Same rules as passes 1–2b.

## Part 0 — branch review, recorded as post-hoc (NOT preregistered)
Before this preregistration was written I (a) read the branch's commit list and diff stat, (b) classified the 109 changed `src/*.py` files by AST comparison (docstring-insensitive): 55 format/comment/docstring-only, 51 with some AST difference, and read the whitespace-insensitive diffs of the files tied to earlier findings (jcs_canonicalizer, consequence_gateway, consequence_token, stpa_validator, provider_07 adapter, routing_seal, actuator_02 adapter, governor/*, workload_identity, token_quota_proxy, mcp_tool_server, tool_guard, gatekeeper, kms_signer), and (c) re-ran every earlier probe script (pass 1, 2a, 2b) against the branch head. No predictions were committed for (a)–(c); my unrecorded expectation from the diffs was "unchanged". Result: no earlier finding's surface changed; see the README for details. This is exploratory.

## Part F — FTRA conditional clearance (`ftra/autonomy.py`, `governor/stages/ftra.py`, `ftra/graph_analyzer.py`)
Property stated in the code: `agent_confidence.reported_confidence` is "the agent's self-reported confidence, parsed one way everywhere ... so a value cannot clear one gate while failing another"; `conditional_clear_reason` is "closed by construction: anything it cannot establish keeps the human in the loop".
F1 `conditional_clear_reason(...)` called directly with `confidence=float("nan")`, a registered terminal, an envelope, magnitude within it: prediction: returns a clearing reason (NaN passes `confidence < floor`). Controls: confidence below the floor -> None; NaN magnitude -> None; unregistered -> None.
F2 Graph path: `PlanGraphAnalyzer(classifier with an envelope registry, magnitude_extractor).analyze(plan, confidence=nan)` for a one-step plan whose terminal is in its envelope: prediction: verdict CLEAR with the terminal in `auto_cleared_terminals`; confidence 0.0 for the same plan: not CLEAR; the boundary stage (`FtraStage.run`) with `params["confidence"] = nan` for the same action: `requires_hitl` and not auto-cleared (the parser maps NaN to 0.0). The graph path reads the evaluator's confidence through `confidence_extractor` (not `reported_confidence`).
F3 `safe_magnitude` with an extractor returning `10**400`: prediction: `OverflowError` escapes (the `float()` conversion is outside the `try`); through `FtraStage.run` the result is the fail-closed `FTRA_ERROR` (HARD, requires_hitl); through `PlanGraphAnalyzer.analyze` a fail-closed verdict.
F4 Magnitude as an int just above a ceiling of 2^53: ceiling `9007199254740992.0`, magnitude int `9007199254740993`: prediction: clears (float rounding). Control: `9007199254740994` does not.

## Part R — terminal registry integrity (`ftra/classifier.py`)
The loader's comment: the manifest digest "detects staleness or tampering of the authority block"; `registry_digest` covers the envelope "so a tampered ceiling fails the same check a tampered terminal does".
R1 With the envelope ceiling edited and `manifest_sha256` recomputed by the repository's own `rehash_registry`, the registry loads and the new ceiling is in force; edited without recomputing: `ValueError`. Prediction: both. (The digest is an unkeyed SHA-256 stored in the same file: integrity, not authenticity.)
R2 A registry with an envelope and no `manifest_sha256`: `ValueError`; without an envelope and without a digest: loads with a warning. Prediction: both.
R3 `expires_at` in the past with a recomputed digest: the classifier loads it and classifies as usual; `check_registry_staleness` reports it only when called. Prediction: loads.

## Part E — estate provider stub posture (`estate_provider.py`)
`StubEstateProvider` refuses unless `CAGE_ENV.lower()` is in {development, test, dev, ci}, default production. Prediction: refuses for unset, "", "production", "staging", "local", "testing", "continuous-integration", "dev " (trailing space); constructs for "dev", "DEV", "development", "test", "ci". Records the pattern next to the provider_07 guard (default "development", deny-list of production spellings): the estate guard is the allow-list shape.

## Not covered in pass 2c
HITL bundle path (provider_02), the provider_09 adapter itself (only the kernel estate provider read), FTRA node_factory/LLM-parse path beyond the confidence read, the branch's infra and CI changes (Terraform, Wolfi images, cloudbuild), KMS-backed behaviour.

## Finding vs note
As before: a stated invariant or in-repo convention failing on a constructed input is a finding; behaviour consistent with stated trade-offs or needing trusted write access is a note.

## Amendment 1 (after the runs)
Outcomes: every numbered prediction in Parts F, R and E matched on main 7e07cba, and the same script gave identical results at the branch head 455f88fb. No misses to record (the predictions were derived from reading the code; the run mostly confirms the reading). One flawed post-hoc check, corrected: after R1 I added `probe_2c_r1_inforce.py` to show the edited ceiling is in force; its first version wrapped `autonomous_envelope()` in a `try/except ValueError`, but that call does not raise (an unreadable registry returns state `unavailable` and no envelope), so it printed "loaded" for an edit that had failed the digest check. The script was fixed to report the classifier's actual state; its recorded output is the corrected run. Also unregistered: the branch-head re-runs of earlier scripts (Part 0); their HMAC-mode seal cases differ from the main-run outputs only because HMAC seals minted in the same second for equal inputs are the same string (a harness artifact noted in pass 1); JWT-mode cases are identical.
