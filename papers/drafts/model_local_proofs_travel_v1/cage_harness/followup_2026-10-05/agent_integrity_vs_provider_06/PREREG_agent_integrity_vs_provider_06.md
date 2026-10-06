# PREREG — vendored agent-integrity (upstream) vs CAGE provider_06 adapter (2026-10-06)
Written BEFORE any probe in this folder was run. Pins: CAGE main 0c657b4c; upstream = the vendored tree `third_party/agent-integrity` (0.1.0-alpha.0, built from that copy with node 22). Nothing here touches the earlier pass 2a (that covered provider_07, not provider_06).
Declared boundary: the adapter README says it verifies receipts with Ed25519 JCS signatures, out-of-band JWKS, "Trust Anchor Invariant"; upstream states it is alpha, verifies consistency not truth, and defines receipt 2-alpha (signature over canonicalJson({protected, body}), receiptDigest over body incl. signature, issuer/audience/purpose/engine/policy/time/subject/replay checks in recheck).
Read before running (from source, not yet executed): upstream digest and signature payload differ from CAGE's; CAGE logs-but-ignores envelopeDigest mismatch; CAGE checks no issuer/audience/purpose/status/nonce/consumption; validate_fria does no receipt verification.

## Predictions
U0 A genuine upstream-created receipt (real createReceipt, real Ed25519 key placed in a JWKS) fails CAGE `verify_receipt_digest` and `verify_receipt_signature` and `_verify_receipt` (returns an error string). Because the formats differ. (Control: upstream recheck of the same receipt = PASS.)
Receipts built in CAGE's own scheme (test-key signed, JWKS-resolvable), then through `_verify_receipt`:
A1 envelopeDigest != evidence_hash -> accepted (None). Upstream class: receipt.subject_changed BLOCKED.
A2 validly signed receipt with verification.status "BLOCKED" -> `submit_evidence` returns a seal with seal_hash. Upstream: outcome carried.
A3 wrong issuer / audience / purpose -> accepted. Upstream: BLOCKED (wrong_issuer / wrong_audience / wrong_purpose).
A4 missing `expiresAt`, and malformed `expiresAt` -> accepted. Upstream: invalid_time BLOCKED.
A5 createdAt 1 year in future and lifetime 10 years -> accepted. Upstream: future_issued / lifetime_exceeded.
A6 same receipt submitted twice -> accepted twice (no consumption). Upstream: receipt.replayed on second.
A7 expiry boundary: at now == expiresAt CAGE accepts (strict `>`); upstream blocks (`>=`). Prediction: differ.
A8 non-canonical signature encoding (unpadded / base64url variant of the same 64 bytes) -> accepted with identical receiptDigest. Upstream: invalid_signature_encoding.
A9 `validate_fria` against a stubbed /verify returning {status: PASS} with a JWKS client configured and no receipt/signature -> admitted=True (the gate does not verify). Prediction: yes; this is a declared-design reading (README: "no wire change"), recorded as a boundary fact.
Controls: tampered body -> CAGE digest False; unknown kid -> error; genuine upstream tampered -> upstream blocks.

## Classification rule
Per item: control-holds / within-declared-boundary / outside-declared-boundary / unknown. A conformance claim ("registered in NORMATIVE_PROVIDERS conformance suite", "Phase 2 receipts") is tested against what the suite's receipts are (CAGE's own mock). No issue filed (user: hold).

## Amendment 1 (after run 1; before run 2)
Run 1 harness flaws, both mine: (a) A8's "digest identical across encodings" regenerated createdAt/expiresAt per variant, so digests differed for a reason unrelated to the property; it was recomputed in run 2 by re-encoding one signature's bytes in three ways under one body. (b) U0's `sig_value_charset_std_b64` field contained `or True` and measured nothing; replaced by a direct `+`/`/` presence test. Run 1 output kept as `out_provider_06_side_run1_flawed_A8.json`. All other cases are unchanged between runs. Also noted: upstream-side A1 control was produced by an envelope edit that made the live check fail (BLOCKED via `receipt.live_check_failed`), not via `receipt.subject_changed`; a weaker control than predicted, recorded as such.
