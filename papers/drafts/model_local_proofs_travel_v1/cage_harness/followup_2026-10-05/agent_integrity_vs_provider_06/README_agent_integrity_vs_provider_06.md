# agent-integrity (vendored upstream) vs CAGE provider_06 — results (2026-10-06)
Pins: CAGE main 0c657b4c; upstream = `third_party/agent-integrity` 0.1.0-alpha.0 (copied, `npm ci`, built, node 22). PREREG (+ Amendment 1) written before the runs. Files: `probe_provider_06_side.py` -> `out_provider_06_side.json` (run 2; run 1 kept, A8 flawed); `ai06_gen.test.ts` (run inside the copied upstream with vitest) -> `upstream_gen_out.json` (genuine receipt, public key, upstream control results).

## Result table
| id | CAGE provider_06 | upstream (genuine code) | classification |
|---|---|---|---|
| U0 genuine upstream receipt | `verify_receipt_digest` False, `verify_receipt_signature` False, `submit_evidence` error "Receipt digest verification failed". Cause: upstream digest = sha256(JCS(body incl. signature)); CAGE's = sha256(JCS(body without signature)). Upstream signs JCS({protected:{algorithm,keyId}, body}) with standard padded base64 (88 chars); CAGE verifies a bare-body signature. Upstream signature verifies under the upstream definition (checked). | PASS | outside the README's wording ("upstream is vendored"); inside "SPIKE" label. The adapter cannot verify a receipt the vendored engine creates; its suite uses receipts built by CAGE's own mock/test helper |
| C controls | valid CAGE-scheme receipt sealed; tampered body, unknown kid refused | tampered receipt BLOCKED (mutated, invalid_signature) | control-holds |
| A1 envelopeDigest != evidence hash | accepted (code logs a warning; comment "Don't fail") | BLOCKED (subject check; my control tripped `live_check_failed` first - weak control) | outside: bound subject is not enforced |
| A2 validly signed receipt with status BLOCKED | `submit_evidence` returns a seal with `seal_hash` | outcome carried in verification | outside: receipt verdict never read |
| A3 wrong issuer / audience / purpose | accepted | BLOCKED (wrong_issuer / wrong_audience / wrong_purpose) | outside |
| A4 missing / malformed `expiresAt` | accepted (malformed -> warning only) | BLOCKED invalid_time | outside (fail-open on parse) |
| A5 createdAt +1y; lifetime 10y | accepted | BLOCKED future_issued; creation refuses >1h | outside |
| A6 replay | accepted twice | second BLOCKED receipt.replayed | outside (no consumption; README states single-use is upstream's, adapter calls it Phase 2) |
| A7 now == expiresAt | accepted; +1s refused | BLOCKED at ==; PASS 1ms before | boundary differs by one comparison |
| A8 signature encodings (url-nopad / std-pad / url-pad) | all three accepted; receiptDigest identical | invalid_signature_encoding | outside: signature string is malleable under an unchanged digest |
| A9 `validate_fria`, JWKS configured, stubbed `/verify` -> `{status: PASS}` unsigned | admitted=True | n/a | within declared design (README: no receipt on the gate path); recorded as boundary fact: the admit decision rests on transport/Bearer only |
| A10 no key manifest configured, forged `{receiptDigest: ...}` | sealed (code warns "verification will be skipped") | n/a | within declared; fail-open default when env unset |
Also read, not run: the vendored upstream contains no HTTP server (no `listen`/`createServer`; CLI + libraries only), so `/verify`, `/receipt`, `/health/*` have no implementation in the vendored tree beyond CAGE's own mock; the README points to "Agent Integrity PR #11" for the sidecar contract, not vendored here.

## Predictions vs observed
All A1-A10 and U0 predictions held. Harness flaws recorded (A8 digest check, tautological charset field; A1 upstream control weak). No misses against predictions otherwise.

## Reading
Same signature as the FlowSignal contrast, stronger because the upstream is in the tree and executable: the adapter's receipt verification is a CAGE-local scheme exercised only by CAGE-made receipts; a genuine receipt from the vendored engine fails at step 1, and receipts that pass CAGE's scheme skip the checks upstream treats as the point of a receipt (subject, audience, purpose, time window, verdict, single use). Declared boundary: SPIKE + mock, and `validate_fria` not verifying receipts is stated design. The README's "Trust Anchor Invariant" (key from outside the receipt) does hold (unknown kid refused). Not filed (held). Not run: adapter against a live upstream sidecar (none vendored); validate_fria input vs upstream envelope schema.
