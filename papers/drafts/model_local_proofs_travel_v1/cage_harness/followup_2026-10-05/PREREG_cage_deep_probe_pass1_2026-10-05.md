# CAGE deep probe, pass 1 — preregistration (2026-10-05, before any probe run)

Target: google/cybernetic-agent-governance-engine at main 7e07cba (post #397–#404; routing_seal.py unchanged since #396, state-commitment surface is new in #401).
Rule: predictions committed here before running; a control beside each attack; misses recorded plainly; no belief/motive claims; findings are about files at the pinned commit.

## Part A — state-commitment surface (src/gateway/governance/evidence/state_commitment.py, new in #401)

Property under test (the module's own docstring): the stateHash is a SHA-256 over the JCS bytes of a PII-sanitized, JSON-normalized snapshot, and the stored preimage reproduces it.

A1 Redaction collapse. Two raw snapshots differing only inside a value the sanitizer redacts (card number, SSN, labelled BIC, email) give the SAME stateHash. Prediction: equal (by design: scope string "agentstate-pii-sanitized/v1"; the #403 comment says so). Control: snapshots differing in a non-redacted field give different hashes.
A2 Type collapse via normalization. Decimal("100.00") vs "100.00"; datetime vs its ISO string; tuple vs list; an object with __str__ vs that string. Prediction: all four pairs hash equal (json_native documents Decimal→str, tuple→list, unknown→str). Control: int 100 vs string "100" differ.
A3 Sanitizer coverage (what reaches immutable storage). Variants of PII forms. Prediction: standard forms redacted (control); NOT redacted: fullwidth-digit card, zero-width-separated card, dot-separated card, space-separated IBAN, unlabelled BIC in free text (by design), card number split across two list items. Uncertain: lowercase IBAN, unicode-dash SSN.
A4 Sanitizer cost. Time of canonicalize_state on adversarial 64KB / 128KB / 256KB strings (repeated "swift " labels, long runs of digits/spaces, many "@", many separators). Prediction: linear (doubling input ≤ 3x time) for all families; non-trivial uncertainty on the labelled-BIC pattern (nested quantifier). Also: the size cap (256KB) is applied after sanitization, so a body of 10x the cap costs sanitization time before the 413 — prediction: yes, time grows with input past the cap.
A5 verify_state_commitment scope. (i) Without `linkage=`, a record minted for linkage L1 verifies for any step (prediction: True; linkage is optional). (ii) With the wrong linkage: False. (iii) callerIdentity altered in the record: True (not in _BINDING_FIELDS; the custodian, not this function, attests the record). (iv) state mutated with stateHash kept: False.
A6 BIC key cue. Value under a bic-like key is redacted; unlabelled under an ordinary key ("bank") is not; BIC inside a dict inside a list under a bic-like key: uncertain (prediction: the dict's own keys decide, so not redacted unless the inner key is bic-like).

## Part B — seal consume/revoke order (routing_seal.py, live Redis 7.0.15 on a local port)

B1 Revoke then consume: consume refused as revoked (prediction yes).
B2 Consume then revoke: revoke reports already-consumed / does not flip the seal to revoked (prediction yes).
B3 50 concurrent consumes of one verified seal: exactly 1 returns True (prediction yes).
B4 Concurrent revoke(x10) + consume(x10): exactly one writer of the nonce key wins; outcome consistent with state afterwards (prediction yes).
B5 Control: a seal without evidence index entry is refused; a verified, bound seal consumes once.

## Not in pass 1
Tri-state outcome replay Lua, STPA/FTRA, actuator_02/OpenShell, provider_02 HITL, provider_07 crypto (#399): pass 2.

## What would count as a finding vs a note
Finding: a property the module/docstring states fails on a constructed input, or an input class reaches immutable storage unredacted that the module claims to redact. Note: behaviour that matches the module's own stated trade-offs.

## Amendment 1 (before any Part B run; written after reading revoke_seal)
revoke_seal's docstring says revocation "never requires the seal to verify", sizes the nonce key's TTL from the unverified `exp`, and has no callers inside src/ (library API; no HTTP route found by grep).
B6 A forged JWT that carries a genuine seal's nonce (nonce is a claim inside the seal, readable by anyone who has seen it) and any exp passes seal_nonce(); revoke_seal(forged) therefore revokes the genuine seal. Prediction: True and the genuine seal is then refused as revoked.
B7 Same forgery with exp = now+1: the nonce key is written with TTL max(1+60,60)=61 s. Prediction: after the TTL lapses (test with a patched shorter floor is NOT allowed; use real wait or Redis EXPIRE-equivalent observation of the TTL value only), the key is gone and the genuine, still-valid seal consumes. I will observe the TTL via Redis TTL (prediction: 60–61) and confirm the consume-after-expiry by deleting the key at that point only if a wait of 61 s is run for real.
B8 HMAC-format seals: nonce = sha256(seal), so a forger cannot reach another seal's nonce. Prediction: B6 does not transfer to HMAC seals.
Classification: note, not a defect, unless a caller exposes revoke_seal; the question for the maintainers is whether the revocation path is meant to be authenticated by its caller.

## Amendment 2 (after Part A/B first runs; before the end-to-end run below)
Recorded misses so far (Part A, run before this amendment): A4 prediction "linear for all families" MISSED for the "swift " repeated-label family — super-linear (8192 → 0.72 s, 16384 → 2.78 s, 32768 → 11.4 s; ~4x per doubling = quadratic). Comparison against the pre-#403 sanitizer (4b116e0) and the regex alone: the cost is in the new `_BIC_LABELLED` pattern (nested quantifier over `[ \t/_-]*(?:swift|bic|...)`), 0.0008 s old vs 0.35 s new at 8 KB. A3 uncertain items resolved: lowercase IBAN and unicode-dash SSN are NOT redacted; space-separated SSN IS. B4/B8/B3/B1/B2/B5/B6/B7 per Part B (HMAC-mode seals minted in the same second with equal inputs are identical strings, so my HMAC-mode sequence reused one nonce across my own cases; JWT-mode is the valid run for B1–B4).
E1 End-to-end through the real POST /governance/state-commitments (httpx ASGI transport, trusted identity, recording sink, handler as in the repo's own test harness): a 16 KB body of "swift " repeats returns 200 after >1 s while a concurrent asyncio ticker (50 ms) shows a max gap >1 s (the sanitizer runs synchronously in the handler); a 16 KB plain body returns in <0.1 s with a max tick gap <0.2 s. Prediction: yes to both.
E2 32 KB "swift " body: ~4x the 16 KB time (prediction 4–6 s). 256 KB (the module's own cap) is extrapolated (~15 min), NOT run.
Scope of reading: authenticated workload identity is required (Linkerd allow-list); this is a reachability-from-an-authorized-producer finding, not an unauthenticated one. Whether other evidence-event fields carry caller text into `_append` (same sanitizer, same synchronous call) is not examined here.
