# CAGE consequence chain vs FlowSignal reference harness — results (2026-10-06)
Pins: CAGE main 0c657b4c (consequence code tree-identical to b4bb9ef7); FlowSignal 471d8af (2026-08-31). PREREG written first. Probes: probe_cage_side.py (real Redis 6391, CAGE_ENV=development), probe_fs_side.py. Outputs: out_*.json.

## CAGE side (all predictions held)
| id | result | classification |
|---|---|---|
| controls | first EXECUTE; replay BLOCK ALREADY_CONSUMED; payload edit BLOCK ACTION_BINDING_MISMATCH | control-holds |
| S1 | `evaluate(token, payload)` takes no current authority version; token with ver="v1-REVOKED-UPSTREAM" EXECUTEs; `claims.ver` only enters the Redis binding hash | outside the docstring's "FlowSignal 6-step" lineage: FlowSignal's gateway blocks on `authority_state_version` != current; CAGE's carries `ver` and never checks currency |
| S2 | marker deleted -> second EXECUTE inside TTL | within-boundary if Redis is trusted; a store-integrity assumption, not stated at the gateway |
| S3 | fabricated `rec` minted by signer holder EXECUTEs | within-boundary (signer = trust root) but mint and verify share one signer; FlowSignal separates mint capability (`_GATEWAY_MINT_CAPABILITY`) from the receipt key |
| S4 | exp-1 and exp accepted; exp+1 TOKEN_INVALID | inclusive boundary; FlowSignal also `>` (same) |
| S5 | digest changes for any payload field; int 100 == float 100.0; 2**53+1 collides with 2**53 | broad binding (control); known RFC 8785 double behavior (earlier pass) |

## FlowSignal side
| id | result | classification |
|---|---|---|
| T1 | mandate absent from `AUTHORITATIVE_MANDATE_LIMITS` -> request's own `mandate_max_amount` is the limit (5e11 ALLOW); known mandate ignores presented limit (ESCALATE) | within declared boundary only if mandates are always pre-registered; receipt snapshot records presented==authoritative so the fallback is not distinguishable afterward |
| T2 | amount -50 ALLOW | unknown: no declared claim on amount sign |
| T3 | NaN, +inf ESCALATE (safe `<=`); **-inf ALLOW** (not predicted) | NaN control-holds; -inf = same class as T2 |
| T4 | clock and evidence time come from the request; backdating `requested_execution_time` turns a 30-day-late expired mandate into ALLOW; a screening timestamp in the future is clamped to age 0 and passes freshness (not predicted in detail) | within declared boundary (README: trusted evidence is an input); recorded because gateway `attempted_at` is also caller-supplied |
| T5 | float receipt vs int attempt -> ACTION_BINDING_MISMATCH | strict, fails closed (prediction was "unknown") |
| T6 | after authority advance -> AUTHORITY_STATE_STALE_REEVALUATION_REQUIRED | control-holds (the check CAGE lacks) |
| T7 | gateway issues a permit on each call for the same receipt (PERMITTED, PERMITTED); single-use lives in the downstream consumption store (not exercised here; their suite, 56 passed) | within declared design |
| T8 | decision edit without key -> AUTHORITY_RECEIPT_INTEGRITY_INVALID | control-holds |

## Misses against prediction
-inf ALLOW; future-dated evidence passes freshness; T5 resolved to mismatch. No CAGE-side misses.

## Reading
The lineage claim in CAGE's gateway docstring ("preserves FlowSignal's 6-step check sequence") does not hold for the currency step: S1 vs T6 is the one controlled contrast. The other contrasts are boundary-assumption differences (key separation, atomic store), not defects in either by their own declarations. FlowSignal's input-trust classes (T1/T2/T4) sit at its stated edge ("trusted evidence is an input"); CAGE's S2/S3 sit at an edge it states less explicitly. Not filed; held per user decision (S1 is the issue candidate once #405/#406 resolve). Not run: FlowSignal consumption store under restart/rollback; real FlowSignal service behind provider_01 (response authentication unverified beyond Bearer/transport per read, not tested).

## Correction (same day, after survey)
S1 compared against the PUBLIC harness; CAGE cites a non-public vendor file. CAGE's plan says the vendor's duplicated version check was "collapsed to a single check", but the plan's six steps, sketch and the shipped code contain none. Unknown what the vendor check compared.
