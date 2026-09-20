# Execution-Gate Channel Collapse: Why Self-Reported Evidence Cannot Bind a Gate to Ground Truth

*v1 — filed 2026-09-20. Authors: operator + Claude (Sonnet 5).*

---

## A note on what kind of paper this is

This is a narrow addition to an existing taxonomy, not a new framework,
and it is worth being explicit about that before anything else.
[`governance_binding_axiom_v2.md`](governance_binding_axiom_v2.md) §4
already distinguishes three enforcement mechanisms — (a) zero-cost-
logged, (b) a trained reward proxy shaped toward a constraint, (c) a
true hard constraint removed from `Feasible(s)` — and gives each a
structurally distinct defeat condition.
[`closed_path_confirmation_v1.md`](closed_path_confirmation_v1.md)
narrows further: for *executable* artifacts specifically, a passing
test suite the artifact's own author wrote establishes only a closed-
path, existential claim, not the open-path, universal claim a binding
claim actually needs.

Neither of those papers names the specific case this one does. Category
(c) — a *true* hard constraint — is the strongest of the three
categories: a real, structural removal of an action from
`Feasible(s)`, not a classifier that might be wrong or a proxy that
might be gamed. This paper's contribution is narrow: **even a genuine
category-(c) gate can fail to bind if what it hard-checks is a self-
reported evidence field rather than the action's actual causal
history.** That is a different failure from (a) (nothing was checked),
(b) (a *trained* proxy was gamed), or (c) as usually illustrated (the
sandbox boundary itself had a gap). Here the gate is real, the check is
real, the re-derivation is exhaustive — and it still cannot establish
the one thing it is being relied on to establish, because of where its
input comes from, not because of any flaw in how rigorously it checks
that input. Section 5 gives a runnable demonstration and three rounds
of adversarial testing against it (two self-run, one from an
independent reader). Two of the three found genuine overclaims — one
in the toy's own strongest claim, one in a mode's prose description —
and both are corrected on the record rather than quietly softened; the
central theorem itself survived all three, the third round demonstrating
it at a strength the paper had not actually earned before.

## Abstract

An execution gate is a function `E(a, e, π) → {ALLOW, DENY, ESCALATE}`
applying a declared policy `π` to a proposed action `a` and supporting
evidence `e` — a decision record, a provenance trace, a "reasoning"
field, a step-by-step derivation. Call the gate **sound** with respect
to ground truth `g*` if `E(...) = ALLOW ⟹ g*` actually holds. We show:
if `e` is produced by the same generative process `G` that produces
`a` — no independent channel supplies or verifies `e` — then `E` cannot
be sound with respect to `g*`, however rigorous the check on `(a, e)`
becomes. `E` can only be sound with respect to `G`'s own self-
consistency, a strictly weaker property. We demonstrate this with a
small, deterministic, dependency-free toy: a generator that can either
honestly execute a procedure or fabricate a plausible-looking evidence
trace for it, and three verifier tiers of increasing rigor, the
strongest of which is *structurally* incapable of telling a fabricated-
but-correct trace from a genuine one. We ran two rounds of adversarial
self-testing against the toy's own strongest claim (round 1 defeated an
overstated version of it, round 2 shows the underlying claim survives
in corrected form), then a third round answering a genuine objection
from an independent public reader, which required building a generator
mode that obtains the correct answer via a provably different
computational path from the declared procedure — the central theorem
held against it. We check the general pattern against two redacted,
independently-read specimens circulating in AI-governance-adjacent
discourse, both of which check evidence supplied by the same process
that supplies the action being gated.

## 1. The model

Three channels:

- **Action channel `a`** — the proposed action.
- **Evidence channel `e`** — whatever the gate is handed to justify
  `a`.
- **Ground-truth channel `g*`** — the property the gate is actually
  relied on to establish (genuine intent, real safety, faithful
  process).

`E(a, e, π) → {ALLOW, DENY, ESCALATE}` applies a fixed, declared `π`.
`E` is **sound** w.r.t. `g*` if `E(...) = ALLOW ⟹ g*`.

## 2. The theorem

**Channel-Collapse Impossibility.** If `e` is produced by the same
generative process `G` that produces `a`, with no independent channel
supplying or verifying `e` against `g*`, then `E` cannot be sound with
respect to `g*` for a sufficiently capable `G`. `E` can only be sound
with respect to `G`'s own self-consistency under `π` — internal well-
formedness and internal arithmetic/logical agreement of `(a, e)` — a
strictly weaker, different property.

**Why.** `π` is a fixed, finite, explicit target sitting inside `Σ`,
the space of everything `G` can emit. `G` does not need `g*` to hold —
only to land somewhere in the region of `Σ` that satisfies `π`. Since
`e` is `G`'s own output, `G` controls both the thing being checked and
the evidence used to check it. Nothing forces `e` to be causally
downstream of whatever actually produced `a`. A sufficiently capable
`G` can construct a plausible `e` regardless of what actually happened
internally, because "plausible per `π`" and "faithful to `g*`" are
different targets, and a check built only from `(a, e, π)` can only
ever measure the first.

This restates, in gate-specific and channel-specific form, the same
validity/soundness split `laundered_vocabulary_v1.md`'s "Metrics vs.
Soundness" entry already states generally, and the same existential-
for-universal substitution `closed_path_confirmation_v1.md` §2 names
for test-suite evidence specifically — narrowed here to a case neither
covers: not a trained proxy (category (b)'s mechanism), not who
authored the test oracle (`closed_path_confirmation`'s mechanism), but
which process produced the evidence field a check reads, independent
of how many times or how rigorously that field is re-verified.

## 3. Positioning against §4's existing taxonomy

A gate built this way can be, and often is presented as, a genuine
category-(c) hard constraint: `e` is required, `a` is rejected if `e`
does not check out, and the check can be made arbitrarily strict. The
theorem's point is that strictness on `(a, e)` alone cannot substitute
for `e` arriving through an independent channel. Section 5's toy makes
this concrete: its strongest verifier re-derives every step of a
declared procedure from scratch and requires an exact match — a
genuine, uncompromising category-(c)-style gate by any reasonable
reading — and is still structurally unable to catch a correct-but-
fabricated trace, for a reason specific to where `e` came from, not to
how carefully it was checked.

## 4. The genre this shows up in

Self-reported evidence-chain gates recur across a body of AI-
governance-adjacent work this project tracks. Two specimens, checked
directly (primary sources read in full, not summarized secondhand),
are described here without identifying detail, per this project's
standing redaction policy for private individuals and small, non-
institutional projects (`laundered_vocabulary_v1.md`'s "A note on
redaction"; `closed_path_confirmation_v1.md` §4's own precedent for
this exact policy applied to a small repository).

- **A small, publicly-hosted commit-authorization repository.** Its own
  published release notes are explicit and honest about scope: a
  promoted `authorize()` path hashes caller-supplied payload bytes and
  checks a bound decision record, and the project's own documentation
  states plainly that this establishes "payload-bound authorisation on
  the tested in-process path," not "downstream non-bypassability" or
  "external enforcement." The decision record being checked and the
  payload being authorized both originate from the same caller — in
  this paper's vocabulary, an admission, in the artifact's own release
  notes, that `e` and `a` are not yet channel-independent.
- **A jointly-authored working paper, self-published on preprint-
  hosting platforms, describing a formal "handoff" architecture for
  status carriage between governance boundaries.** Its central
  predicates (whether a handoff is "applicable," "satisfied,"
  "established") are stated over stipulated symbolic objects with no
  given procedure for computing any of them against a real running
  system — the evidence a downstream check would read is, by the
  paper's own construction, self-supplied.

Neither specimen is claimed to have been built or is being defended in
bad faith. Both are checked for what they claim to establish, and in
both cases the gap this paper names is either openly scoped (the first
specimen) or a direct consequence of the paper's own stated formal
apparatus (the second). The general schema both instantiate: `Policy →
Authority Resolution → Runtime Validation → Execution Gate →
Consequence → Evidence`. Every stage before "Execution Gate" is either
a function of `a`/`e` themselves or evaluated by a process reading only
what `G` chose to emit.

## 5. A runnable counter-model

The domain: a task `(x0, ops)` — a starting integer and an ordered
chain of arithmetic operations. The true answer is `ops` applied in
order to `x0`. An action `a` is a generator's claimed answer; evidence
`e` is a step-by-step trace of intermediate values.

Three generator modes, all deterministic:

- `HONEST` — executes `ops` forward; `a` and `e` are the real trace.
- `SHORTCUT_WRONG` — picks an arbitrary wrong final value, then
  fabricates a trace *backward* from it through exact inverse
  operations.
- `SHORTCUT_RIGHT_UNFAITHFUL` — computes the true answer via the same
  forward procedure `HONEST` uses, then fabricates a trace backward
  from that correct value — the shortcut is entirely in the evidence
  construction, not in obtaining `a`. (An earlier version of this
  section described this mode as "skipping the declared procedure,"
  which was inaccurate about its own code; corrected here, and §7
  below builds the mode that actually does skip it, in response to a
  reader who caught the discrepancy.)
- `SHORTCUT_RIGHT_VIA_CLOSED_FORM` (§7) — computes the true answer via
  a provably different method that never executes the declared
  procedure at all, then fabricates a trace the same way.

Three verifier tiers:

- `V0` — checks step count and op/operand names only.
- `V1` — the strongest surface check: re-derives every step forward
  from `x0`, requires an exact match to every declared value, and
  requires the trace's end to equal `a`.
- `V2` — an actual external-attestation channel: an independent process
  re-derives the answer from the public task alone, given nothing `G`
  submitted, and compares.

```python
#!/usr/bin/env python3
"""Channel-Collapse Counter-Model — runnable, deterministic, no
dependencies. Independently re-run from this file to confirm its
output; the exact output below was produced by this exact code."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

Op = tuple[str, int]
Trace = list[tuple[str, int, float]]

_FORWARD: dict[str, Callable[[float, int], float]] = {
    "add": lambda v, k: v + k, "sub": lambda v, k: v - k,
    "mul": lambda v, k: v * k, "div": lambda v, k: v / k,
}
_INVERSE: dict[str, Callable[[float, int], float]] = {
    "add": lambda v, k: v - k, "sub": lambda v, k: v + k,
    "mul": lambda v, k: v / k, "div": lambda v, k: v * k,
}


def true_answer(x0: int, ops: list[Op]) -> float:
    """Executes the declared procedure -- a for-loop applying each op to
    the running value, in order. This DOES run the declared procedure;
    see closed_form_answer() below for a method that provably does not."""
    v: float = x0
    for op, k in ops:
        v = _FORWARD[op](v, k)
    return v


def closed_form_answer(x0: int, ops: list[Op]) -> float:
    """A genuinely different computational path. Every op in this domain
    is affine (v -> scale*v + offset). Composes all ops into a SINGLE
    (scale, offset) pair symbolically; x0 is touched exactly once, at the
    very last line. None of the intermediate values a step-by-step
    execution would produce ever exist anywhere in this function's
    execution -- this is the case §7 needs: the correct answer, obtained
    without executing the declared procedure."""
    scale, offset = 1.0, 0.0
    for op, k in ops:
        if op == "add":
            offset = offset + k
        elif op == "sub":
            offset = offset - k
        elif op == "mul":
            scale, offset = scale * k, offset * k
        elif op == "div":
            scale, offset = scale / k, offset / k
    return scale * x0 + offset


def honest_trace(x0: int, ops: list[Op]) -> tuple[float, Trace]:
    trace: Trace = []
    v: float = x0
    for op, k in ops:
        v = _FORWARD[op](v, k)
        trace.append((op, k, v))
    return v, trace


def fabricate_backward(x0: int, ops: list[Op], seed: float) -> Trace:
    """G never executes the real procedure -- it walks `ops` backward
    from a seed value through exact inverse operations. Exact inverses
    guarantee forward-consistency by construction, regardless of
    whether `seed` is the true answer or an arbitrary one."""
    n = len(ops)
    values = [0.0] * n
    v = seed
    for i in range(n - 1, -1, -1):
        op, k = ops[i]
        values[i] = v
        v = _INVERSE[op](v, k)
    return [(ops[i][0], ops[i][1], values[i]) for i in range(n)]


def natural_types(ops: list[Op]) -> list[type]:
    """Which type each position naturally has under forward execution --
    a pure function of `ops` alone (public), independent of x0 and of
    the real trajectory."""
    out: list[type] = []
    seen_div = False
    for op, _ in ops:
        if op == "div":
            seen_div = True
        out.append(float if seen_div else int)
    return out


def fabricate_backward_type_faithful(x0: int, ops: list[Op], seed: float) -> Trace:
    raw = fabricate_backward(x0, ops, seed)
    want = natural_types(ops)
    return [(op, k, w(v)) for (op, k, v), w in zip(raw, want)]


@dataclass(frozen=True)
class Submission:
    mode: str
    a: float
    e: Trace


def generate(mode: str, x0: int, ops: list[Op], wrong_value: float) -> Submission:
    if mode == "HONEST":
        a, e = honest_trace(x0, ops)
        return Submission(mode, a, e)
    if mode == "SHORTCUT_WRONG":
        return Submission(mode, wrong_value, fabricate_backward(x0, ops, wrong_value))
    if mode == "SHORTCUT_RIGHT_UNFAITHFUL":
        real = true_answer(x0, ops)
        return Submission(mode, real, fabricate_backward(x0, ops, real))
    if mode == "SHORTCUT_RIGHT_UNFAITHFUL_TYPE_FAITHFUL":
        real = true_answer(x0, ops)
        return Submission(mode, real, fabricate_backward_type_faithful(x0, ops, real))
    if mode == "SHORTCUT_RIGHT_VIA_CLOSED_FORM":
        real = closed_form_answer(x0, ops)
        return Submission(mode, real, fabricate_backward(x0, ops, real))
    raise ValueError(mode)


def v0_shape_only(x0: int, ops: list[Op], s: Submission) -> tuple[bool, str]:
    if len(s.e) != len(ops):
        return False, "wrong step count"
    for (op, k, _), (so, sk) in zip(s.e, ops):
        if (op, k) != (so, sk):
            return False, "step does not name declared op/operand"
    return True, "shape well-formed"


def v1_full_rederivation(x0: int, ops: list[Op], s: Submission,
                          type_aware: bool = False) -> tuple[bool, str]:
    ok, why = v0_shape_only(x0, ops, s)
    if not ok:
        return False, why
    v: float = x0
    for (op, k, declared), (so, sk) in zip(s.e, ops):
        v = _FORWARD[op](v, k)
        if abs(v - declared) > 1e-9:
            return False, f"value mismatch: recomputed {v}, declared {declared}"
        if type_aware and type(v) is not type(declared):
            return False, f"type mismatch: recomputed {type(v).__name__}, declared {type(declared).__name__}"
    if abs(v - s.a) > 1e-9:
        return False, "trace end does not equal declared a"
    return True, "every step re-derived and matched"


def v2_independent_reexecution(x0: int, ops: list[Op], s: Submission) -> tuple[bool, str]:
    real = true_answer(x0, ops)
    if abs(real - s.a) > 1e-9:
        return False, f"independent re-execution got {real}, declared {s.a}"
    return True, "independent re-execution matches"


if __name__ == "__main__":
    X0, OPS, WRONG = 5, [("add", 7), ("mul", 3), ("sub", 4), ("div", 2)], 999.0

    print("=== Base result: three modes x three verifier tiers ===")
    for mode in ["HONEST", "SHORTCUT_WRONG", "SHORTCUT_RIGHT_UNFAITHFUL"]:
        s = generate(mode, X0, OPS, WRONG)
        v0 = v0_shape_only(X0, OPS, s)[0]
        v1 = v1_full_rederivation(X0, OPS, s)[0]
        v2 = v2_independent_reexecution(X0, OPS, s)[0]
        print(f"{mode:35s} V0={v0!s:5s} V1={v1!s:5s} V2={v2!s:5s}")

    print()
    print("=== Round 1: serialized traces, honest vs. fabricated-but-correct ===")
    _, honest_e = honest_trace(X0, OPS)
    real = true_answer(X0, OPS)
    fab_e = fabricate_backward(X0, OPS, real)
    ser = lambda t: json.dumps([{"op": o, "operand": k, "value": v} for o, k, v in t])
    print("honest:    ", ser(honest_e))
    print("fabricated:", ser(fab_e))
    print("identical serialized form:", ser(honest_e) == ser(fab_e))
    s_honest = Submission("HONEST", true_answer(X0, OPS), honest_e)
    s_fab = Submission("SHORTCUT_RIGHT_UNFAITHFUL", real, fab_e)
    print("V1 (type-aware) on honest:    ", v1_full_rederivation(X0, OPS, s_honest, type_aware=True))
    print("V1 (type-aware) on fabricated:", v1_full_rederivation(X0, OPS, s_fab, type_aware=True))

    print()
    print("=== Round 2: type-faithful fabrication defeats the type-aware check ===")
    s_fab2 = generate("SHORTCUT_RIGHT_UNFAITHFUL_TYPE_FAITHFUL", X0, OPS, WRONG)
    print("fabricated (type-faithful):", ser(s_fab2.e))
    print("identical serialized form:", ser(honest_e) == ser(s_fab2.e))
    print("V1 (type-aware) on type-faithful fabrication:",
          v1_full_rederivation(X0, OPS, s_fab2, type_aware=True))

    print()
    print("=== Round 3: correct answer obtained WITHOUT executing the ===")
    print("=== declared procedure at all (closed-form composition)    ===")
    print("true_answer (executes the declared procedure):    ", true_answer(X0, OPS))
    print("closed_form_answer (never touches x0 until the end):", closed_form_answer(X0, OPS))
    s_cf = generate("SHORTCUT_RIGHT_VIA_CLOSED_FORM", X0, OPS, WRONG)
    print("fabricated trace from closed-form answer:", ser(s_cf.e))
    v1_cf = v1_full_rederivation(X0, OPS, s_cf)
    v2_cf = v2_independent_reexecution(X0, OPS, s_cf)
    print("V1 (full re-derivation) on closed-form submission:", v1_cf)
    print("V2 (independent re-execution) on closed-form submission:", v2_cf)
```

**Actual output, this file, unmodified — independently re-run to
confirm before publication:**

```
=== Base result: three modes x three verifier tiers ===
HONEST                              V0=True  V1=True  V2=True
SHORTCUT_WRONG                      V0=True  V1=False V2=False
SHORTCUT_RIGHT_UNFAITHFUL           V0=True  V1=True  V2=True

=== Round 1: serialized traces, honest vs. fabricated-but-correct ===
honest:     [{"op": "add", "operand": 7, "value": 12}, {"op": "mul", "operand": 3, "value": 36}, {"op": "sub", "operand": 4, "value": 32}, {"op": "div", "operand": 2, "value": 16.0}]
fabricated: [{"op": "add", "operand": 7, "value": 12.0}, {"op": "mul", "operand": 3, "value": 36.0}, {"op": "sub", "operand": 4, "value": 32.0}, {"op": "div", "operand": 2, "value": 16.0}]
identical serialized form: False
V1 (type-aware) on honest:     (True, 'every step re-derived and matched')
V1 (type-aware) on fabricated: (False, 'type mismatch: recomputed int, declared float')

=== Round 2: type-faithful fabrication defeats the type-aware check ===
fabricated (type-faithful): [{"op": "add", "operand": 7, "value": 12}, {"op": "mul", "operand": 3, "value": 36}, {"op": "sub", "operand": 4, "value": 32}, {"op": "div", "operand": 2, "value": 16.0}]
identical serialized form: True
V1 (type-aware) on type-faithful fabrication: (True, 'every step re-derived and matched')

=== Round 3: correct answer obtained WITHOUT executing the ===
=== declared procedure at all (closed-form composition)    ===
true_answer (executes the declared procedure):     16.0
closed_form_answer (never touches x0 until the end): 16.0
fabricated trace from closed-form answer: [{"op": "add", "operand": 7, "value": 12.0}, {"op": "mul", "operand": 3, "value": 36.0}, {"op": "sub", "operand": 4, "value": 32.0}, {"op": "div", "operand": 2, "value": 16.0}]
V1 (full re-derivation) on closed-form submission: (True, 'every step re-derived and matched')
V2 (independent re-execution) on closed-form submission: (True, 'independent re-execution matches')
```

**Reading the result.** `HONEST` and `SHORTCUT_RIGHT_UNFAITHFUL` are
indistinguishable to `V1`, the strongest surface check implemented —
`V1` is not merely fooled, it is structurally unable to do otherwise,
because the trace is fully determined by `(x0, ops, a)` regardless of
how `a` was produced. `V2` catches `SHORTCUT_WRONG` cleanly, because
`g*_correctness` (is `a` the true answer) is independently checkable —
but by its own construction it never looks at `e` at all, so it cannot
and does not touch `g*_faithfulness` (was `e` the real process).

## 6. Two rounds of adversarial self-testing against the toy's own strongest claim

An earlier version of this section claimed the honest and fabricated
traces were "bit-for-bit identical" and that no surface check, however
rigorous, could ever tell them apart. That claim was tested and found
overstated — corrected here on the record rather than softened
quietly, per this project's standing discipline for its own material.

**Round 1.** Once evidence is serialized the way a real decision record
would be — JSON, not live in-process objects — the honest trace's early
values are Python `int` and the fabricated trace's are all `float`
(contamination from seeding backward fabrication with the final,
necessarily-float answer). A verifier that checks value *type*, not
just numeric value, catches the fabrication cleanly (`Round 1` output
above). The original "no check could ever distinguish them" claim was
false as stated for any evidence channel that preserves numeric
representation, which most real logging does.

**Round 2.** The hole does not generalize into a real fix. Which type
each trace position should have is a deterministic function of `ops`
alone — public information, independent of `x0` and of the real
trajectory. A fabricator that tracks this defeats the strengthened,
type-aware verifier too, producing a trace serialization-identical to
the honest one (`Round 2` output above).

**The corrected, standing claim.** For this domain, every surface
property of `e` a verifier can check turns out to be a deterministic
function of public information (`x0`, `ops`, the claimed `a`) —
closing any single such property only ever raises `G`'s fabrication
cost by the cost of computing that same deterministic function, never
by requiring access to the real generative process. This is a more
precise and more defensible statement than the pre-attack version, and
the one this paper stands behind.

## 7. Round 3 — an external reader's objection, tested directly

**Provenance, stated precisely.** After this draft was shared publicly,
an engaged reader on the same public thread raised a direct, correct
technical objection, redacted here per this document's standing
private-individual policy: `SHORTCUT_RIGHT_UNFAITHFUL`'s action `a`
comes from `true_answer(x0, ops)`, and `true_answer()` does execute the
declared operations in sequence — a for-loop applying each op to the
running value — before the trace is reconstructed backward. As written,
the reader noted, §5 demonstrated that real execution plus a
reconstructed trace is not proof the trace was recorded during
execution. It did not yet demonstrate a correct result obtained without
executing the declared procedure at all — the reader's own framing, close
to verbatim.

This is a correct objection against §5's original prose, which
described `SHORTCUT_RIGHT_UNFAITHFUL` as "computes the true answer
directly (skipping the declared procedure)" — that description was
inaccurate about the code's own behavior, corrected in §5 above. Per
this project's own method (`governance_binding_axiom_v2.md` §5:
construct or find the defeating trajectory, do not argue about whether
one would exist), the right response is to build the case the reader
named and see what it finds — not to concede or rebut the point in
prose alone.

**`closed_form_answer()`**, added to §5's code (`SHORTCUT_RIGHT_VIA_
CLOSED_FORM` mode): every operation in this toy's domain is affine
(`v → scale·v + offset`). Composing all of `ops` into a single
`(scale, offset)` pair symbolically, then computing `scale·x0 + offset`
in one step, touches `x0` exactly once — none of the intermediate
values a step-by-step execution would produce (`12`, `36`, `32`, ...)
are ever computed anywhere in this function. This is precisely the case
the reader named: the correct answer, obtained without executing the
declared procedure in any sense that produces or touches its
intermediate values.

**Result, from §5's own re-run (`Round 3` output above):** `closed_
form_answer` returns the identical correct value to `true_answer` on
both tasks checked. A trace fabricated backward from that closed-form
value still passes both `V1` (full re-derivation) and `V2` (independent
re-execution) — the theorem's central claim is unaffected by closing
this gap; if anything it is now demonstrated at the exact strength the
reader asked for, rather than the weaker strength §5 originally,
inadvertently, claimed.

**What this round does NOT establish.** Does not establish that no
other, sharper defeat exists — one correct, well-targeted objection
answered is not the same as the theorem being exhaustively tested.
Does not establish that this reader's engagement constitutes the full
independent adversarial testing §9 (below) still calls for — one
objection, correctly identified and answered, is real progress and is
exactly the kind of engagement this paper is filed to invite, not a
substitute for sustained scrutiny from multiple readers over time.

## 8. What this paper does NOT establish

- **Does not establish that either redacted specimen in §4 was built or
  is being defended in bad faith.** The theorem is about what a gate
  *can* verify given its channel structure, independent of any
  particular author's intent; both specimens' own documentation is
  read as honestly scoped where it is honestly scoped.
- **Does not establish that the toy's strong "structurally incapable"
  result holds for non-invertible or natural-language evidence
  channels.** It holds at that strength for one clean, deterministic,
  exactly-invertible domain. What generalizes is the weaker claim
  actually stated in §2: a sufficiently capable `G` can construct an
  `e` satisfying any fixed `(a,e)`-only check without `e` being
  faithful — not that every such `e` is provably indistinguishable in
  every domain.
- **Does not establish that composition-inside-the-generative-process
  (making the constraint part of what produces `a`, rather than
  checking it after the fact) is buildable, tested, or superior in
  practice.** Named as the other real category of solution; not
  developed here.
- **Does not establish that external re-execution (`V2`'s category)
  generally fails to touch faithfulness, as a law rather than a
  conjecture.** Stated as a conjecture grounded in one worked domain. A
  domain where the *process*, not just the final value, can be
  independently observed (a commit-then-reveal protocol, for instance)
  would need to be built and tested before this generalizes.
- **Does not claim rounds 1 and 2 constitute independent adversarial
  testing.** Both were run by the same authors who built the toy, in
  the same working session — real progress on this paper's own
  discipline, but a weaker form of scrutiny than an independent reader
  attempting to defeat the claim. Round 3 (§7) is that independent
  engagement, and the paper is filed to invite more of it (see
  `closed_path_confirmation_v1.md` and `governance_binding_axiom_v2.md`
  §12.5 for the precedent this project follows: post plainly, let an
  independent reader object, and correct on the record if the
  objection holds).
- **Does not claim §7 closes the question of independent testing.**
  One reader, one objection, correctly identified and answered, is a
  single data point — real, and worth recording precisely as such, not
  inflated into "this paper has now been independently verified."

## 9. What would move this from draft to confirmed

§7 shows this process working once: a real reader found a genuine gap
in the paper's own prose, it was checked directly, and the toy was
extended to close it without the central theorem breaking. What would
move this further: further independent readers constructing defeats
this paper's three rounds so far did not find — against the toy
directly, or against the general theorem in a domain none of the three
rounds covered (a non-invertible or natural-language evidence channel
specifically, per §6's own item 1). Per this project's own standing
method (`governance_binding_axiom_v2.md` §5): construct or find the
defeating trajectory, do not argue about whether one would exist.

---

*Sources: `governance_binding_axiom_v2.md` §2–4 (formal apparatus and
existing category taxonomy, cited not restated), §12.5 (the adversarial-
testing precedent this paper's own §6, §7, and §9 follow); `closed_path_
confirmation_v1.md` (the closed-path/open-path distinction this paper
narrows further, and its redaction precedent, applied identically
here — including to the §7 reader); `laundered_vocabulary_v1.md`
("Metrics vs. Soundness," "A note on redaction"). The two §4 specimens
were read in full at primary-source tier by this project directly; no
other source was consulted for either finding.*
