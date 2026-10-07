# PREREG — CAGE consequence chain vs FlowSignal reference harness (2026-10-06)
Written BEFORE any probe in this folder was run.
Pins: CAGE main 0c657b4c; FlowSignal 471d8af596044d61f86f774f70cd8c6ff2efc31c.
Scope: classify each result against the DECLARED boundary of the code under test
(FlowSignal: harness-scoped keys, in-process state, "trusted evidence" is an input;
CAGE: kernel signer, Redis single-use store). A flag is a lead, not a verdict.

## CAGE-side (ConsequenceGateway / token / store)
- S1 Authority state change after mint still yields EXECUTE within TTL (`ver` carried, never compared). Predict: YES.
- S2 Deleting the Redis consumption marker allows a second EXECUTE for the same token inside TTL. Predict: YES (expected storage property; declared-boundary question).
- S3 Holder of the kernel signer can mint an EXECUTE-grade token with a fabricated `rec`. Predict: YES (same-signer mint/verify).
- S4 Expiry boundary: token at now == exp accepted, now > exp rejected. Predict: boundary inclusive.
- S5 Digest covers full payload: changing any unrelated payload field changes the digest/binding. Predict: YES (broad binding).
Controls: a valid token EXECUTEs once; replay HOLD/BLOCK; tampered payload BLOCK.

## FlowSignal-side (validate_execution / evaluate_financial)
- T1 Mandate absent from AUTHORITATIVE_MANDATE_LIMITS: limit falls back to request `mandate_max_amount`. Predict: YES, passes with caller-chosen limit.
- T2 Negative amount passes `amount_within_limit`. Predict: YES.
- T3 NaN amount -> not ALLOW (control). Predict: safe.
- T4 Caller-supplied `requested_execution_time` / `screening_captured_at` accepted as clock/evidence. Predict: YES.
- T5 int vs float amount in binding hash. Predict: mismatch or normalized; unknown.
- T6 Control: authority_state_version bump after receipt -> AUTHORITY_STATE_STALE_REEVALUATION_REQUIRED. Predict: YES.
- T7 Control: permit single-use / replay denied. Predict: YES.

## Classification rule
Each result recorded as: control-holds / within-declared-boundary / outside-declared-boundary / unknown.
Misses against prediction are recorded as misses. No issues filed from this folder (user: hold).
