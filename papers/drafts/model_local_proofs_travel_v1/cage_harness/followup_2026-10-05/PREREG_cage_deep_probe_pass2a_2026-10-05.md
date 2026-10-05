# CAGE deep probe, pass 2a — preregistration (2026-10-05, before any pass-2a run)

Target: google/cybernetic-agent-governance-engine at main 7e07cba (unchanged since pass 1). Same rules as pass 1: predictions first; controls beside attacks; misses recorded; no belief/motive claims. Pass 2a covers the consequence gateway chain, the vendored JCS canonicalizer it hashes with, and the provider_07 adapter (#399). Pass 2b (STPA/FTRA, actuator_02/OpenShell, provider_02 HITL, provider_09) is not started.

## Part C — vendored JCS (src/gateway/governance/vendor/jcs, via jcs_canonicalize_plan), used for every consequence digest
Property under test: RFC 8785 says what a verifier in another language would compute; two payloads a verifier must treat as different should not canonicalize equal, and values RFC 8785 cannot represent should be refused, not coerced.
C1 NaN / Infinity: prediction: raises (control: finite float canonicalizes).
C2 ints above 2^53: 9007199254740993 vs 9007199254740992: prediction: distinct digests (exact Python ints; RFC 8785 would serialize both as the same IEEE double, so a cross-language verifier disagrees). Record as note.
C3 float 1.0 vs int 1: prediction: equal (RFC: both "1").
C4 -0.0 vs 0: prediction: equal (RFC: "0"). Uncertain.
C5 non-string keys {1:"a"} vs {"1":"a"}: prediction: raises or equal; uncertain; record which.
C6 Decimal, datetime, set, bytes, custom object as values: prediction: raise (TypeError or similar) rather than coerce. Control: str vs dict values stay different.
C7 Through `ConsequenceGateway.evaluate(token, payload_with_Decimal)`: prediction: the exception escapes `evaluate` (digest is computed outside the try block), i.e. the caller gets an exception instead of a BLOCK evaluation. Same shape as the SealCanonicalizationError note from pass 1's predecessor.
C8 NFC vs NFD strings: different digests (control; expected).

## Part G — ConsequenceGateway / ConsequenceToken / ConsequenceAuthorityStore (software Ed25519 signer, real Redis on a local port)
G1 Control: mint + evaluate -> EXECUTE; second evaluate -> ALREADY_CONSUMED; altered payload -> ACTION_BINDING_MISMATCH; expired token -> TOKEN_INVALID; token whose signature is changed -> TOKEN_INVALID.
G2 Marker TTL vs token TTL. The store's marker TTL (default 90 s, env-configurable) and the token TTL (60 s default; ttl_seconds is a mint argument) are not tied by any check. With store ttl=2 s and token ttl=60 s: evaluate, wait 3 s, evaluate again: prediction EXECUTE twice (replay after marker expiry). With the defaults (90 > 60): second evaluate stays ALREADY_CONSUMED. Also verify() accepts a token with exp - iat larger than the default: prediction yes (no maximum lifetime check).
G3 binding_hash delimiter: ("a:b","c") vs ("a","b:c") with equal other fields: prediction equal. Consequence: only the reason code (ALREADY_CONSUMED vs AUTHORITY_RECORD_BINDING_MISMATCH) can be wrong; both are BLOCK.
G4 Order of consume and evidence: with an evidence sink raising EvidenceChainUnavailableError on ingest, evaluate returns BLOCK/EVIDENCE_CHAIN_UNAVAILABLE after the token has been consumed; the next evaluate is ALREADY_CONSUMED. Prediction: yes (token burned for an action that was blocked). Also observe what `get_evidence_sink()` returns with no running sink and whether EXECUTE then stands (uncertain; record).
G5 verify() does not check jti == rec and ignores the header kid: a token signed by the gateway key with jti != rec and kid "x" is accepted. Prediction: accepted. Classification: note (needs a gateway-signed token).

## Part P — provider_07 adapter (src/integrations/provider_07)
P1 Posture gate. `allow_step1_unsigned=True` is refused only when CAGE_ENV.lower() is "production" or "prod", with an unset CAGE_ENV defaulting to "development"; the repo's central `resolve_posture()` defaults unset to PRODUCTION, maps staging/stage/uat/preprod to STAGING and unknown values to PRODUCTION, and its docstring says it replaces ad-hoc CAGE_ENV comparisons. Prediction: construction with the flag succeeds for unset, "staging", "stage", "uat", "preprod", "prd", "live", "production " (trailing space) and "", and is refused for "production", "PROD"; for each accepted value `is_enforcing()` is True. Control: flag False constructs for all values.
P2 With the flag on, a response carrying signature "unsigned-placeholder" and decision ALLOW with a non-empty authority_record_id is admitted without any JWKS call; with the flag off the same response is refused. Prediction: yes to both.
P3 JWKS refresh on unknown kid (#399): N verifications each carrying a different unknown kid cause N remote JWKS fetches after the first warm-up (no cooldown), and concurrent lookups fetch concurrently. Prediction: N and N. Control: a known kid causes no fetch while the cache is fresh.
P4 Provider07JwksClient accepts an http:// JWKS URL, and the adapter's default JWKS URL is `{endpoint}/.well-known/jwks.json` (same host as the inference endpoint). Prediction: both true (read from code; construction test only).
P5 A refresh that returns a manifest without the current keys empties the cache (a fetch of `{"keys": []}` makes the previously known kid unknown). Prediction: yes; fail-closed in effect.

## Not in pass 2a
STPA/FTRA, actuator_02/OpenShell, provider_02 HITL, provider_09; KMS-signed tokens under a real posture.

## Finding vs note
Finding: a stated invariant or a repository-wide convention (here, the central posture helper) fails on a constructed input. Note: behaviour consistent with the module's own stated trade-offs, or needing a signed artifact only the gateway can make.

## Amendment 1 (after the Part C and P1/P4 runs; before the Part G and P2/P3/P5 runs)
Recorded outcomes so far. Part C: C1 hit (NaN/Infinity raise ValueError); **C2 missed** (predicted distinct, observed EQUAL: both ints canonicalize to 9007199254740992, which is what RFC 8785 specifies); C3, C4 hit; C5 observed int keys raise AttributeError (not equal, not a ValueError); C6 hit (Decimal, datetime, set, bytes, custom object raise TypeError; a tuple is accepted as a list); C8 hit. P1 hit for every value (flag constructs for unset, "", "production ", staging, stage, uat, preprod, prd, live; refused for production, prod, PROD, Production; the central helper reports enforcing for every one of the accepted non-dev values); P4 hit.
Added before running Part G (because of C2):
G6 Through the real gateway: a token minted for an action payload with `"account_id": 9007199254740992` is evaluated against a payload with `"account_id": 9007199254740993`. Prediction: EXECUTE (the digests are equal, the payloads are not). Control: ...994 (a different double) gives ACTION_BINDING_MISMATCH. Also record what the seal path does with the same value (`generate_seal` canonicalization); prediction: it refuses ints above 2^53 (SealCanonicalizationError), so the two paths in the same repository disagree about such values.
C7 stays as written (exception escaping `evaluate`), now with an Decimal payload and an int-key payload.

## Amendment 2 (after the Part G and provider_07 runtime runs)
Outcomes: Part G: G1–G6 and C7 all hit as predicted (G2 replay after marker expiry; G3 colon collision; G4 token consumed then BLOCK on evidence failure; G5 accepted; G6 EXECUTE for the colliding id and the seal path refuses it). Provider_07 runtime: P2 hit (both unset and staging admit the unsigned placeholder with the flag on; flag off is refused by the kid lookup); P3 hit (20 unknown kids -> 20 fetches sequentially, 20 concurrently).
**Harness flaw in P5.** The recorded `P5_after_empty_manifest_known_kid_resolves: true` does not test the property: my script looked up the known kid while the cache was still warm from the preceding lookups, so no refresh happened against the emptied manifest. The result is discarded; P5 is re-run below with the refresh forced first (an unknown-kid lookup while the manifest is empty, then the known kid).
