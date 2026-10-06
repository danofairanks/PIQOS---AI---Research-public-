# PREREG — probe of github.com/grahamb-ai/runtime-authority-reference-implementation (2026-10-06)
Written BEFORE any probe in this folder was run. Pin: HEAD 26893c2 (code identical to the evidence-pinned `ea36ac1`; `git diff --stat ea36ac1 HEAD` = README only). Not the CAGE-cited vendor file (not public); standalone.
Declared boundary (README + evidence repo + `docs/limitations_and_next_steps.md`, read before running): reference implementation, not production; a constrained catalogue of four sentence patterns, unmatched sentences "silently produce nothing, no error"; no identity infrastructure; "sealed" = persisted, not signed; currency not checked; one active policy globally; `delegation_validity` dormant (no expiry accepted); delegation `max_amount` tightening-only; "default refusal where no policy rules apply to an action"; "exact monetary-boundary evaluation" (evidence: 100000 ALLOW / 100001 ESCALATE); authority evaluated first and short-circuits.
Control: their own suite (52 tests) passes in my environment at HEAD (observed before this prereg).
Environment: venv with fastapi/sqlmodel/etc.; SQLite via DATABASE_URL; engine-level calls plus the real FastAPI app through TestClient.

## Predictions
Extraction (policy text -> rules; engine `evaluate`):
X1 "Unauthorized roles for payment.release: intern." is extracted as an authority GRANT for "intern" (the `authorized roles` pattern matches inside "Unauthorized roles"); evaluate(role=intern) -> ALLOW. YES. Same for "No authorized roles for payment.release: contractor." YES.
X2 "The manager may approve payment.release up to USD 100,000." yields no rule (currency code before the amount); with a role list present a manager order of 10,000,000 -> ALLOW. YES.
X3 Amount parsing: "up to $2 million" -> 2.0; "up to 100k" -> 100.0; "up to 5,000.50" -> 5000.0; "up to 100.000" -> 100.0; "up to 1,5" -> 15.0. YES (all as stated; a stricter-than-intended ceiling except 15.0 which is also stricter than 1.5? no: 15 > 1.5, looser).
X4 Evidence-only action: the policy has an evidence rule for payment.release but its authority sentence is phrased outside the catalogue ("Only managers are authorized to release payment.release.") -> rule set has the evidence rule only; evaluate(role=intern or empty, evidence attached) -> ALLOW (no authority check exists). YES.
X5 With only a role-limit rule ("The manager may approve payment.release up to 10,000.") and no role list, role "intern" with amount 10,000,000 -> ALLOW (no rule names the role). YES.
X6 Two limit sentences for the same role/action: the FIRST in text order is applied, whether stricter or looser ("up to 100,000" then "up to 10,000" -> limit 100,000; reversed -> 10,000). YES.
X7 The upload summary reports counts only and does not list ignored sentences (a document with 3 sentences, 1 understood -> total_rules 1, no skipped list). YES.
Evaluation inputs (HTTP, with rules loaded via upload):
V1 `context.amount` omitted on an authorized role -> ceiling and threshold-evidence rules both skipped -> ALLOW. YES.
V2 `amount` as string "250000" -> unhandled error (HTTP 500, no decision); `true` -> treated as 1 -> ALLOW; -5 -> ALLOW; NaN -> ESCALATE; inf -> ESCALATE.
V3 Action `Payment.Release` (case) or leading space -> REFUSE (no rules) (rule actions are lowercased, order actions are not).
V4 `delegation.max_amount` larger than the policy limit has no effect (tightening only holds); NaN has no effect; negative -> ESCALATE for any amount.
V5 `delegation.expires_at` in the past is ignored (dormant, declared) -> ALLOW.
V6 Any caller can POST /api/v1/specs/upload (no auth) and it deletes ALL existing rules; after uploading "Authorized roles for payment.release: attacker." the earlier-authorized role gets REFUSE and `attacker` gets ALLOW. YES (declared: no identity infra, one active policy).
V7 Exact boundary: amount == limit ALLOW, limit + 0.01 ESCALATE (control, matches their evidence).
V8 Currency ignored: 100000 JPY passes like EUR (declared; control).
Controls: unknown action REFUSE; role not in A1 list REFUSE; authority failure short-circuits (admissibility checks absent from record).

## Classification
Each result: control-holds / within-declared-boundary / outside-declared-boundary. Items the limitations doc already names (silent drop, no auth, currency, dormant delegation, single active policy) are within-declared; consequences the documents do not state (a prohibition list read as a grant; fail-open when the authority sentence is missed; unnamed roles unrestricted; omitted amount bypass; string amount 500) are recorded as outside-declared unless the README's wording covers them. No issue filed; the repository is the maintainer's reference demonstrator and any report would be the user's call.
