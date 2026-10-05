# CAGE deep probe, pass 2b — preregistration (2026-10-05, before any pass-2b run)

Target: google/cybernetic-agent-governance-engine at main 7e07cba (unchanged). Same rules as passes 1 and 2a. Pass 2b covers: the STPA validator (`stpa_validator.py`), the actuator_02 adapter (`integrations/actuator_02`, OpenShell supervisor; httpx mock transport, software Ed25519 signer), its OCSF telemetry ingestor, and the evidence sink's best-effort `ingest()` as the consequence gateway uses it (left open as "G4b" in pass 2a). NOT covered, deferred to pass 2c: FTRA (`ftra/`), provider_02 HITL/bundle conformance, provider_09 decision points, KMS-backed signing.

## Part S — STPAValidator
S1 Core UCA-1 ("write_db requires a signed approval token") checks only `params.get("approval_token") is None`. Prediction: `write_db` with `approval_token` equal to `""`, `"garbage"`, `0`, `False`, `{}` yields no violation; with the key absent or None yields STPA_UCA_1 (control).
S2 Core UCA-1 applies only when `action_name == "write_db"` exactly. Prediction: `"write_db "`, `"WRITE_DB"`, `"write-db"`, `"write_db​"` yield no violation from the validator on its own (the governor's registry refused such names in the earlier pass; not re-tested here).
S3 A contributed rule sharing a core rule's `uca_id` replaces it: `STPAValidator([UcaRule("UCA-1", action="other", predicate=lambda *_: None)]).validate("write_db", {})` returns []; without the contributed rule it returns STPA_UCA_1. Prediction: yes, silently (no log line at WARNING or above). A differently cased id ("uca-1") does not replace it (both active).
S4 "Fails closed whenever a rule predicate raises": a predicate that raises -> HARD violation (control); a predicate returning `0` raises TypeError out of `validate()` (outside the try block); returning `{}` is treated as safe; returning `{"a": 1}` yields a list of non-Violation items. Prediction: all three as stated.

## Part A — actuator_02 adapter (mock transport; signer = Ed25519 test key; credential broker stubbed)
A1 Receipt verification matrix with a resolver configured: (a) valid signed receipt bound to the request's envelope digest -> accepted, VERIFIED; (b) receipt with the `signature` member removed, `require_signed_receipts=False` -> accepted, UNVERIFIED; with `require_signed_receipts=True` -> rejected (SIGNED_RECEIPT_REQUIRED); (c) signed receipt with `status` changed -> INVALID, rejected; (d) validly signed receipt bound to another envelope digest -> INVALID (ENVELOPE_MISMATCH); (e) validly signed receipt lacking `envelope_digest` -> INVALID. Prediction: all as stated.
A2 Key-manifest outage (resolver raises) -> UNVERIFIED, accepted when not strict; rejected when strict. Prediction: yes.
A3 `executor_id` allow-list is (`actuator_02`, `a02`, `openshell`, `actuator_01`), and `actuator_01` is also the dataclass default for `ExecutionClearance.executor_id`. Prediction: a clearance with the default executor id is sent to the supervisor; `cage_finance_broker` (what the finance tool provider sets) and `ACTUATOR_02` (case) are rejected (EXECUTOR_ID_MISMATCH).
A4 Brokered-header filter: headers named `x-cage-routing-seal` and `X-Cage-Envelope-Digest` are dropped; `x_cage_routing_seal` and `X-CAGE_Routing-Seal` (underscore variants) pass through unchanged. Prediction: as stated (observed on the outgoing request).
A5 What the adapter checks of the clearance's seal and freshness: a clearance with `routing_seal="aaa.bbb.ccc"` (JWS-shaped, not a seal), `issued_at=0`, `approvals=[]`, `required_quorum=5` is POSTed to the supervisor. Prediction: yes (shape check only; the module documents the seal as verified upstream).
A6 The constructor accepts an `http://` endpoint. Prediction: yes.
A7 Two clearances whose `params` differ only by an integer id above 2^53 (…992 vs …993) produce the same `envelope_digest` and the same `X-CAGE-OpenShell-Assertion`. Prediction: yes (same class as the pass 2a finding).

## Part O — OcsfEvidenceIngestor
O1 Secret-key masking recurses into dicts and lists of dicts but not lists of lists: `{"a": [[{"token": "s"}]]}` retains `token: s`; `{"a": [{"token": "s"}]}` is redacted (control). Prediction: yes.
O2 `disposition` -> control id: `Blocked`, `Denied`, `Dropped`, `Rejected` -> AC-3; `Block`, `Deny`, `Quarantined`, `Isolated`, `Unauthorized`, `Access Revoked`, `Error` -> AU-2. Prediction: as stated.
O3 `governance_decision_digest` accepts any 8-128 character string (no lookup). Prediction: yes. `metadata` has no size cap: a 1 MB value is accepted by the ingestor. Prediction: yes.
O4 A bearer token inside a value under an innocuous key survives the ingestor's masking and the evidence sink's PII sanitizer. Prediction: yes.
O5 The issue #405 pattern is reachable through sandbox telemetry: the sink's `_append` runs `PIISanitizer().sanitize_dict(event)` synchronously on the whole record; for metadata `{"cmd": "swift " * n}`, that call takes >1 s at 16 KB. Prediction: yes (measured with the same sanitizer call, no Redis).

## Part G4b — evidence best-effort in the consequence gateway
`EvidenceStreamSink.ingest()` returns None (best effort) when its Redis is None or when the write raises a non-chain-restore exception; only `EvidenceChainUnavailableError` is re-raised. Prediction: with a real, not-started sink (Redis None) and with a started-style sink whose `_append` raises RuntimeError, `ConsequenceGateway.evaluate` returns EXECUTE/OK with no evidence record; with `_append` raising EvidenceChainUnavailableError it returns BLOCK (pass 2a G4).

## Finding vs note
Finding: a stated invariant (docstring/README) or an in-repo convention fails on a constructed input. Note: consistent with stated trade-offs, or needs trusted (plugin/gateway) code.

## Amendment 1 (after the pass 2b runs; recorded, not a prediction)
Outcomes: every numbered prediction in Parts S, A, O and G4b matched. One unpredicted observation: importing `src.gateway.governance.stpa_validator` first (before `contracts`) raises `ImportError: cannot import name 'UcaRule' from partially initialized module` (circular import with `contracts.py`); the scripts import `contracts` first. A second unpredicted observation: in A1b (receipt with the `signature` member removed, resolver configured, strict off) the adapter emits no finding at all (`codes: []`), so the receipt is accepted as UNVERIFIED silently. No misses to record in this pass.
