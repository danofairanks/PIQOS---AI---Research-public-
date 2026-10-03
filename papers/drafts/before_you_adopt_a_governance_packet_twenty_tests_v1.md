# Before You Adopt a Governance Packet: Twenty Tests

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.** Companion handout to the paper "Governance Packets: Levels, Depth, and Twenty Tests for Adopters."

**Purpose.** A checklist an adopter can run on *any* governance packet or
policy-admission pipeline (decision records, gates, receipts, reference
suites) before relying on it. It reports patterns and gives the test; it
characterizes no author, intent, or conduct, and it makes no prevalence
claim. Layer: these tests probe the **binding/definitional layer** and are
orthogonal to behavioral/output-layer security testing — clearing one does
not clear the other.

**Three levels of "governance".** (1) *Organizational* — roles, inventories, policies, human review; (2) *technical boundary* — gates between a model and its effects; (3) *model-level* — training and representation shaping. A packet at one level does not cover the others; check which level each claim is about.

**How to score.** Run the test yourself; record the input, the output, and
the commit/version tested. "Passed" means the failure could not be
produced; "failed" means it was; "not testable" is a valid outcome and is
itself information. Do not score from documentation alone.

| # | Test | What a failure looks like |
|---|---|---|
| 1 | For each gate predicate (standing, freshness, authority, validity): who supplies its truth value? Can a third party falsify it? | The gate's author marks it satisfied |
| 2 | Re-derive one reference ("golden") expected value from the written spec, without running the implementation | Expected values match only because they were produced by the code |
| 3 | Push one input set through **every** path that claims equivalence; compare verdict, reason code, and executed flag | Paths agree on verdict but not on reason code, or disagree on verdict |
| 4 | Diff the closed-world registries (known actions/permissions) of every path | The demonstrated path denies what the hardened path allows, or the reverse |
| 5 | Submit an input carrying an unknown, stale, or expired-authority field to every path | One path silently ignores it; another rejects it |
| 6 | Trace which path the README/demo actually runs. Is the strongest control on it? | The strongest mechanism exists but is not on the demonstrated path |
| 7 | Before counting any refusal result, show one valid, bounded request that succeeds (positive control) | A component that refuses everything scores full marks |
| 8 | Ask whether the "independent" observer shares a process or trust domain with the effect it observes | Independence is of call path, not of authority; the ceiling is unstated. Moving the observer out-of-band or nearer the hardware improves separation of process, not of who configures it or who verifies it |
| 9 | After authorization, change the underlying state; is the effect still permitted? | Authority fixed at T0 survives the state change |
| 10 | Over a fixed window, compare commits that touch a known gap with commits that touch only documentation or routing. **Count every ref — non-default branches and open PRs as well as the default branch** (a default-branch-only view can miss a real response) | Vocabulary, layers, or receipts change while the gap stays open |
| 11 | Give the packet to a reviewer (human or model) with a **required executed check**; count elaborations vs. executed tests | Reviewers elaborate the document instead of testing it |
| 12 | Try to construct an input the system accepts that violates each stated invariant | No input can violate it: the invariant is vocabulary, not a constraint |
| 13 | Read the low-traffic channel first (issue tracker, PR bodies, claim-boundary and non-claims files, commit history). List every stated limit and fix cycle, then check whether each appears with equal specificity in the front-page or announcement claims | Real limits and fix cycles exist only in the basement; the front page carries generic or no hard-wall limits |
| 14 | Ask whether a non-maker, non-AI party could reproduce the claimed check from artifacts alone; check what the attestation says it did *not* verify | "Verified" means the maker identified themselves and an artifact exists; function was never checked |
| 15 | Name the layer the packet attaches at (context, harness/OS, tool-call interface, decode-time, representation, weights). Compare against the front-page claims | Claims require a deeper layer than the packet actually attaches to |
| 16 | For each technical challenge raised in the packet's public history, look for an executed test in the reply | The reply describes the challenger or re-labels the challenge instead of running a check |
| 17 | For each governance claim, name what **ends the chain of checking** (the terminus) and whether it is outside the control of the party being governed. Do this once per level | The only answer is another layer, document, party or AI inside the same system — nothing external ever answers the claim |
| 18 | Take each summary score and write it as a failure rate. At your own monthly volume, how many failures is that? What is the chance of at least one failure in a typical workflow? What share of failures would you see? What does one failure cost? | The score is quoted as success and none of these four numbers is stated |
| 19 | Ask the maker to show the mechanism on the effect channel and one forced violation it denied. Then ask to see it fail when deliberately disabled, so a gate that never fires can be told apart from a model that never errs. Check that the thing doing the binding is the thing the claim is about | The claim is about the model, the evidence is about a wrapper, a document or test outputs; the mechanism is not exhibited, cannot be seen firing, or sits where the governed system can alter it |
| 20 | When someone replies "we agree", "we're converging" or "closer than it first appears", do three things. (a) Write the original finding in one sentence, including the gap it names. (b) Write in one sentence what the other party agreed to. (c) List what was executed, published or changed as a result: a test run, an artifact, a replaced definition, a revised number. Then ask whether (a) and (b) are about the same gap, and whether (c) is empty | The agreement is about a neighboring point the finding never disputed, the gap the finding names is untouched, and (c) is empty: the agreement is a statement only |

**What this checklist does NOT establish.** Not that any specific packet
fails any test; not that passing all of them makes a packet safe; not a
substitute for behavioral-layer testing; not evidence about prevalence.
Test 10 is a monitoring pattern over time, not a one-shot test. Test 17 generalizes test 1.
