# PREREG: stub-substitution detector for borrowed assurance (toy model)

Written 2026-10-20 BEFORE model.py was run. Plain code and plain vocabulary; it is meant to be understandable to someone who has not seen any related project.

## Question
Can a mechanical test tell a component whose claimed success genuinely depends on an upstream check from one that only cites it?

## Setup (all deterministic)
- Authority store with an integer current version. Badge-style tokens carry (id, version, expires_at, action).
- Upstream U: `check_current(token_version, current_version) -> bool` (equal versions = current). U's own suite: GREEN.
- Five components, each exposing `execute(token, payload, authority, now) -> "EXECUTE"|"BLOCK"`; each is documented "preserves U's version check; status inherited from U's suite (GREEN)":
  - A: calls U at the boundary.
  - A2: calls U through a wrapper function (indirect).
  - B: carries the version as a claim, mixes it into a binding hash, never compares it to current.
  - C: no version compare; blocks only on token expiry (short TTL).
  - D: same code as B, but its own suite contains no stale-token case.
- Scenario: token issued at version N, authority revoked to N+1, original token presented. Expected: BLOCK. Variants: stale+unexpired (S), stale+expired (SE), fresh (F), tampered payload (T).

## Detector
For each component run its own suite twice: real U, and U replaced by an always-True stub. Classify:
- DEPENDENT: the stale case (S) is BLOCK with real U and EXECUTE with the stub.
- BORROWED: S is EXECUTE with real U and with the stub (U's GREEN is cited, never exercised at this component).
- OTHER-REASON: S or SE is BLOCK in both runs (success may be real, attribution to U is wrong).
- UNREACHED: the component's suite has no stale case (cannot tell; not the same as borrowed).
Detector positive control: a stub that always returns False (blocks everything) must change F's outcome for A, A2; if it changes nothing for them the harness is not wired to U.

## Predictions (fixed now)
A: DEPENDENT. A2: DEPENDENT (indirect call is still found because the test replaces U, not static analysis). B: BORROWED. C: OTHER-REASON on SE (expired) and BORROWED on S (stale+unexpired). D: UNREACHED. Positive control: F flips for A and A2 under the always-False stub; F does not flip for B, C, D.
Inherited status line: all five report GREEN inherited from U's suite; own S-case result is RED for B and C and D-if-run, which is the borrowed-assurance gap.

## What would show the detector is wrong
Any prediction above missing; or a component whose behaviour depends on U only through a path the stub does not replace (e.g. a copy of U's logic inlined). That inlined-copy case is NOT predicted to be caught and is declared as a known limit.

## Not claimed
This shows the test discriminates in a constructed model. It says nothing about how common the pattern is in real systems and nothing about any real project.
