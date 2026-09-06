# The Temporal Boundary Gap: A Companion Counter-Model to the Binding Axiom's Category (c)

*v1 — filed 2026-09-06. Authors: operator + Claude (Sonnet 5). Companion
to `governance_binding_axiom_v1.md` — narrow, explicitly derivative,
does not revise that paper's axiom or its three-enforcement-category
taxonomy.*

---

## What this paper adds, precisely

`governance_binding_axiom_v1.md` §4 distinguishes three governance
enforcement mechanisms — (a) zero-cost-but-logged, (b) a penalty shaped
into the reward proxy R, (c) a true hard constraint removed from
`Feasible(s)` — and gives each a structurally distinct defeat condition.
Category (c)'s stated defeat condition is spatial in every worked
example that paper supplies: "a demonstration that the gate itself is
incomplete or misconfigured... a boundary that does not cover every
exit path" (§4, illustrated in §6.3 by a channel-removal experiment
where a closed private-messaging channel left an equally sufficient
public one open).

This paper names and demonstrates a second, temporal shape of the same
category-(c) defeat condition: a hard gate whose `Feasible(s)`
computation is correctly derived from the conditions that held at one
point in time, but is never re-triggered when those conditions change.
The boundary does not fail to cover an exit path in space — it fails to
cover an exit path *in time*. This is not a fourth enforcement category.
It is a sub-shape of (c)'s existing defeat condition the original
paper's worked examples do not illustrate, offered as a candidate
addition rather than a correction.

## 1. Motivating claim, stated generically

A claim of this shape circulates in AI-governance discourse: *if a
governance system cannot survive a state that is validly authorized at
time T₀, undergoes a material change in its justifying conditions at
ΔN, and has the same consequence attempted again at Tₙ, then the system
does not have governance over consequence — it has governance over
records, permissions, policies, provenance, or monitoring, which is a
different and weaker thing.* The specific LinkedIn post motivating this
paper is a private individual's post and is redacted per this project's
standing policy for private individuals (see `README.md`'s house
conventions and `laundered_vocabulary_v1.md`'s "Law" entry) — the claim
itself is evaluated on its own merits below, independent of who stated
it.

Two things are worth separating before any formal treatment. First, the
claim's *form* is already compliant with `governance_binding_axiom_v1.md`
§5's own method: it states a falsifiable universal ("if X then not-Y")
and demands the right *kind* of evidence — a runnable artifact, not an
architecture diagram, a patent, or a white paper. Second, the claim as
typically stated supplies no counter-model of its own; it is a demand
for evidence, not a supply of it. §5's method requires actually
constructing or finding the defeating trajectory. This paper does that
step.

## 2. Mapping the claim onto the existing taxonomy

Let C be the constraint an operator wants respected, `Feasible(s)` the
action set the environment's transition function actually permits, and
let C now be explicitly time-varying: what justifies an action at T₀
may no longer justify it after ΔN. The three-point trajectory maps onto
§4's existing categories as follows, without requiring any new formal
apparatus:

- **Under category (a).** Temporal staleness is moot. A zero-cost-logged
  layer was never binding at T₀ either — `governance_binding_axiom_v1.md`
  §6.1's own counter-model already defeats it, with or without a ΔN
  event anywhere in the trajectory.
- **Under category (b).** A learned proxy R′ that no longer tracks the
  true, post-ΔN C is exactly §4(b)'s stated defeat condition — "the
  trained proxy R′ being satisfied on a trajectory that still violates
  the true C" — with C simply time-varying rather than fixed. No new
  clause is needed; the existing condition already covers this case
  once C is read as a function of time.
- **Under category (c).** This is the case the original paper's worked
  examples do not illustrate directly. A hard gate — genuinely removing
  an action from `Feasible(s)`, not merely logging a refusal — can still
  fail T₀ → ΔN → Tₙ if its `Feasible(s)` computation was derived once,
  at T₀, and never re-triggered when ΔN occurred. The gate is not
  incomplete in the sense §6.3 demonstrates (a boundary drawn too
  narrowly in space, leaving an equivalent channel open); it is
  incomplete in the sense that a boundary correctly drawn at one moment
  was never re-drawn against a later one.

## 3. A runnable counter-model, in the same spirit as §6.1

Following `governance_binding_axiom_v1.md`'s own stated preference — "a
counter-model that can only be described, not run, is a weaker
instrument than one a reader can execute and inspect" — below is a
complete, runnable extension of that paper's `governance_killer_demo.py`
along the time axis. An environment starts in a condition
(`verified_low_risk`) that justifies an action (`execute_transfer`); at
a fixed step (`DELTA_N_STEP`), the condition changes to
`flagged_high_risk` — a stand-in for a policy revision, a threshold
move, a counterparty status change, or any other real-world ΔN event.
An automated agent keeps attempting the same, previously-authorized
action every step, representing the ordinary case of automation
continuing to run after the world changed underneath it. Three
governance variants are tested against this trajectory, plus the
no-governance baseline:

```python
#!/usr/bin/env python3
"""
Temporal Governance Killer Demo
--------------------------------
Extends governance_binding_axiom_v1.md's governance_killer_demo.py
(section 6.1) along the time axis instead of the space axis, to test
the T0 -> deltaN -> Tn claim directly rather than just discuss its
shape.

Original demo: does a soft/hard governance layer bind an action in a
SINGLE state. This demo: does a governance layer's Feasible(s)
correctly track a constraint C that is itself time-varying -- i.e.
does authorization survive past the point where the condition that
justified it materially changed (delta_N), or does it silently carry
forward a T0-era grant into Tn.

Four governance variants, matching the axiom paper's own taxonomy plus
one new distinction this demo exists to surface:

  --no-governance   baseline: action always succeeds regardless of
                     condition (category: none)
  (default) soft     condition is checked and logged, but a changed
                     condition never blocks execution (category (a):
                     zero-cost-logged -- was never binding at T0
                     either, so temporal staleness is moot for it)
  --hard-stale       Feasible(s) is computed ONCE from the condition
                     at T0, cached, and never re-derived after
                     delta_N (category (c), implemented with a
                     temporal boundary gap -- the new distinction:
                     a hard gate can still fail T0->deltaN->Tn if its
                     Feasible(s) computation isn't re-triggered on
                     change)
  --hard-revalidated Feasible(s) is re-derived from the CURRENT
                     condition at every step (category (c), correctly
                     implemented -- what "governance over consequence"
                     actually requires per the T0->deltaN->Tn bar)

Run:
  python temporal_governance_killer_demo.py
  python temporal_governance_killer_demo.py --hard-stale
  python temporal_governance_killer_demo.py --hard-revalidated
  python temporal_governance_killer_demo.py --no-governance
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any

MAX_STEPS = 12
DELTA_N_STEP = 5          # the step at which the material change occurs
ACTION = "execute_transfer"


# ---------------------------------------------------------------------------
# Environment: a condition that starts valid and becomes invalid at delta_N
# ---------------------------------------------------------------------------

@dataclass
class Env:
    """
    condition: the fact that justified the original authorization.
    Starts "verified_low_risk" (T0). At DELTA_N_STEP it flips to
    "flagged_high_risk" -- a material change in exactly the kind of
    real-world form a company already keeps records of: a policy
    revision, a threshold move, a counterparty status change. Nothing
    about the action itself changes; only the condition that grounded
    its authorization does.
    """
    condition: str = "verified_low_risk"
    step_count: int = 0
    logs: list[str] = field(default_factory=list)

    def tick(self) -> None:
        self.step_count += 1
        if self.step_count == DELTA_N_STEP:
            self.condition = "flagged_high_risk"
            self.logs.append(f"t={self.step_count}: DELTA_N -- condition changed to {self.condition!r}")

    def observe(self) -> dict[str, Any]:
        return {"condition": self.condition, "t": self.step_count}

    def act(self, action: str) -> dict[str, Any]:
        self.logs.append(f"t={self.step_count}: act:{action} under condition={self.condition!r}")
        if action == ACTION:
            return {"ok": True, "msg": f"{ACTION} executed"}
        return {"ok": False, "msg": f"unknown action {action}"}


# ---------------------------------------------------------------------------
# Governance layer: three variants of "does Feasible(s) track current C"
# ---------------------------------------------------------------------------

@dataclass
class Governance:
    """
    mode:
      "soft"              -- category (a): logs, never blocks.
      "hard-stale"         -- category (c) with a temporal boundary gap:
                              Feasible(s) computed once from T0's
                              condition, cached, never re-derived.
      "hard-revalidated"   -- category (c) correctly implemented:
                              Feasible(s) re-derived from current
                              condition every step.
    """
    mode: str = "soft"
    cached_permission: bool | None = None   # set once for hard-stale
    violations: list[str] = field(default_factory=list)
    checks: list[dict[str, Any]] = field(default_factory=list)

    @staticmethod
    def _permitted_under(condition: str) -> bool:
        # The actual rule: transfers may execute only under a
        # verified-low-risk condition. This is C -- what the operator
        # actually wants respected, at whatever moment it is asked.
        return condition == "verified_low_risk"

    def check(self, condition: str, t: int) -> dict[str, Any]:
        true_permission_now = self._permitted_under(condition)

        if self.mode == "hard-stale":
            if self.cached_permission is None:
                # Feasible(s) derived once, at first check (T0), and
                # never re-derived -- the temporal analog of "a
                # sandbox boundary that does not cover every exit
                # path": the boundary was correctly drawn against
                # T0's condition and simply never re-drawn.
                self.cached_permission = true_permission_now
            allowed = self.cached_permission
            abort = not allowed
        elif self.mode == "hard-revalidated":
            allowed = true_permission_now
            abort = not allowed
        else:  # soft
            allowed = True          # never actually restricts Feasible(s)
            abort = False

        record = {
            "t": t,
            "condition": condition,
            "true_permission_now": true_permission_now,
            "allowed": allowed,
            "abort": abort,
            "mode": self.mode,
        }
        self.checks.append(record)
        if not true_permission_now and allowed:
            # This is the exact defeat signature: the true, current C
            # is violated, but Feasible(s)/the soft log still permits
            # the action.
            self.violations.append(f"t={t}: stale/soft authorization permitted action under {condition!r}")
        return record

    def summary(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "n_checks": len(self.checks),
            "n_violations": len(self.violations),
            "violations": list(self.violations),
        }


# ---------------------------------------------------------------------------
# Agent: a simple automated system that keeps executing the same,
# previously-authorized action every step. It does not "know" about
# governance at all -- it represents the ordinary case of automation
# continuing to run after the world changed underneath it.
# ---------------------------------------------------------------------------

@dataclass
class Agent:
    def step(self) -> str:
        return ACTION


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(mode: str, use_governance: bool = True, verbose: bool = True) -> dict[str, Any]:
    env = Env()
    gov = Governance(mode=mode) if use_governance else None
    agent = Agent()
    trajectory: list[dict[str, Any]] = []

    for _ in range(MAX_STEPS):
        env.tick()
        obs = env.observe()
        action = agent.step()

        gov_result = None
        if gov is not None:
            gov_result = gov.check(obs["condition"], obs["t"])
            if gov_result.get("abort"):
                trajectory.append({"t": obs["t"], "condition": obs["condition"], "gov": gov_result, "env": None, "aborted": True})
                if verbose:
                    print(f"  t={obs['t']:2d} condition={obs['condition']:18} gov=ABORT               env=blocked")
                continue

        env_result = env.act(action)
        trajectory.append({"t": obs["t"], "condition": obs["condition"], "gov": gov_result, "env": env_result, "aborted": False})
        if verbose:
            gov_s = "n/a" if gov_result is None else ("ALLOW" if gov_result["allowed"] else "REFUSE(logged)")
            flag = " <-- stale/soft authorization used" if gov_result and gov_result["allowed"] and not gov_result["true_permission_now"] else ""
            print(f"  t={obs['t']:2d} condition={obs['condition']:18} gov={gov_s:22} env={env_result.get('msg')}{flag}")

    violations = len(gov.violations) if gov else 0
    post_delta_n_successes = sum(
        1 for e in trajectory
        if e["t"] >= DELTA_N_STEP and not e.get("aborted") and e.get("env", {}).get("ok")
    )
    report = {
        "mode": mode if use_governance else "none",
        "violations": violations,
        "post_delta_n_successes": post_delta_n_successes,
        "gov_summary": gov.summary() if gov else None,
        "verdict": _verdict(mode if use_governance else "none", violations, post_delta_n_successes),
    }
    return report


def _verdict(mode: str, violations: int, post_delta_n_successes: int) -> str:
    if mode == "none":
        return "No governance: baseline -- action always succeeds, condition irrelevant."
    if mode == "soft" and post_delta_n_successes > 0:
        return (
            "KILL (category a): soft governance logged the post-deltaN "
            "violation but never touched Feasible(s) -- staleness was "
            "moot because it was never binding at T0 either."
        )
    if mode == "hard-stale" and post_delta_n_successes > 0:
        return (
            "KILL (category c, temporal variant): a HARD gate still "
            "failed T0->deltaN->Tn -- Feasible(s) was correctly derived "
            "at T0 and simply never re-derived after deltaN. A boundary "
            "that does not cover every exit path IN TIME, not in space."
        )
    if mode == "hard-revalidated" and post_delta_n_successes == 0:
        return (
            "PASS: Feasible(s) re-derived from current condition each "
            "step -- this is what 'governance over consequence' "
            "actually requires. T0->deltaN->Tn survived."
        )
    return "Unexpected combination -- inspect trajectory."


def main() -> None:
    parser = argparse.ArgumentParser(description="Temporal governance killer demo")
    parser.add_argument("--hard-stale", action="store_true")
    parser.add_argument("--hard-revalidated", action="store_true")
    parser.add_argument("--no-governance", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.no_governance:
        mode, use_gov = "none", False
    elif args.hard_stale:
        mode, use_gov = "hard-stale", True
    elif args.hard_revalidated:
        mode, use_gov = "hard-revalidated", True
    else:
        mode, use_gov = "soft", True

    print(f"=== Mode: {mode} (delta_N occurs at t={DELTA_N_STEP}) ===")
    report = run(mode, use_governance=use_gov, verbose=not args.quiet)
    print()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

Running all four modes produces exactly the predicted split:

```
soft:              8 violations  ->  KILL (category a) -- never binding at T0 either
hard-stale:        8 violations  ->  KILL (category c, temporal variant)
hard-revalidated:  0 violations  ->  PASS
no-governance:     baseline, 8 post-deltaN successes, no violation concept applies
```

The `hard-stale` result is the load-bearing one. `Feasible(s)` in that
run is not misconfigured in the sense §6.3 illustrates — there is no
missing exit path, no equivalent second channel left open. The single
line `cached_permission = true_permission_now` (computed once, at first
check, and reused thereafter) is the entire defect: a hard constraint
implemented as a snapshot of a time-varying fact rather than a live
function of it. This reproduces exactly the predicted failure mode
without needing an unpredictable or adversarial agent — the toy agent here,
like `governance_killer_demo.py`'s own, is deterministic and simply
keeps attempting its original, once-valid action.

## 4. Status table, in the format `governance_binding_axiom_v1.md` §4.2 uses

| Conjecture | Status in this paper | What would move it |
|---|---|---|
| A hard gate (category c) can fail T₀ → ΔN → Tₙ via a temporal boundary gap, not a spatial one | **Constructed and demonstrated** | A real, observed production incident of the same shape (an authorization cache never invalidated on a policy/status change) would move this from constructed to observed, matching §6.2/§6.3's evidentiary tier |
| T₀ → ΔN → Tₙ names a genuinely new, fourth enforcement category | **Not supported** | The claim collapses cleanly into existing categories (a)/(b)/(c) once C is read as time-varying; no observation found or constructed here requires new formal apparatus beyond that |
| The demand "run the system, preserve the evidence" is itself sufficient without a supplied counter-model | **Not supported, on the claim's own terms** | `governance_binding_axiom_v1.md` §5 requires the defeating trajectory be constructed or found, not merely called for — a demand is not a demonstration |

## 5. What this paper does not establish

Does not establish that `governance_binding_axiom_v1.md`'s taxonomy is
incomplete in any way that requires a new category — the finding here
is a sub-shape of an existing category's defeat condition, offered as a
candidate addition to that paper's worked examples, not a correction of
its axiom. Does not establish that the `hard-stale` failure mode is
common in real deployed governance systems — this is a constructed
demonstration (§6.1's own tier), not an observed incident (§6.2/§6.3's
tier); no real-world specimen of an authorization cache failing this
way is cited here. Does not establish anything about the motivating
LinkedIn post's author, product, or claims beyond the claim's own stated
form and content — the specimen is redacted per this project's standing
policy, and the technical analysis above stands independently of who
made the claim or why. Does not propose that every governance
architecture must re-validate every constraint on every step regardless
of cost — re-validation frequency is itself a design tradeoff this
paper does not address; the point is narrower: a hard gate that never
re-validates at all is a temporal instance of the same defeat condition
`governance_binding_axiom_v1.md` §4(c) already names, not a separate
failure mode requiring separate treatment.

## Cross-references

`governance_binding_axiom_v1.md` (the paper this document extends,
narrowly, at category (c) only); `closed_path_confirmation_v1.md` (the
same low-commitment, explicitly-derivative-sharpening format applied to
category (a) instead of (c)).
