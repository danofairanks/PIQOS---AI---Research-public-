# What an Empty Result Means: A Preregistered Failure-Semantics Probe of a Research MCP Server, and the One-Check Fix That Merged

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is this repository's own server, `tools/research_mcp`, so nothing here is about a third party. One external paper is cited for its fault model and is not evaluated here. No individual is named.

**Disclosure.** Drafted with AI assistance. One model wrote the probe, the predictions, the fault operators and the fix, so this is a same-source check. The two client rules in section 5 are toy rules, not an LLM agent: they show what a rule can tell apart from a response, not what a model would do.

## 1. The question

An MCP tool server returns a result, and a client decides what to do with it. For a scanner, the successful result for "nothing found" is an empty findings list. The question is whether a client can tell *scanned, nothing found* from *not scanned* (empty input, a truncated input, a skipped rule set, a fault upstream of the scanner), using only the response.

The motivation is the MCP-Injector paper (arXiv:2610.32555v1), which injects MCP-level faults and measures agent degradation. It does not test this particular ambiguity. Its mined fault profile is used in section 5 for weighting, and nothing else from it is evaluated here.

## 2. What was done, and how

- **Object.** `tools/research_mcp` at commit `b921ff4`, the commit before the empty-input guard merged (PR #68). Thirty tools; eight of them take a single `text` argument and scan it. Run with `mcp` 2.3.0 in a fresh environment; the repository pins 2.0.0, so the version differs.
- **Predictions** (A1 to A5, B1 to B4) were written before any tool output was inspected (`predictions_fixed_2026-10-26.md`). The file was committed together with the results, so the repository history cannot show the order; the order is the evaluator's own record.
- **Part A** is a static probe: four inputs per text scanner (known-flagged text, clean text, empty string, whitespace only), plus error probes (invalid parameters, a missing API key for the Groq-backed tools, an unknown tool).
- **Part B** applies ten fault operators (F1 to F10) to the real responses of the six scanners that produce findings on the flagged text, and applies two toy client rules. `bifp_scan_closed_path_language` and `debasinizer_scan_text` found nothing on the flagged text, which is a recall question about the chosen input, so they are excluded from Part B.
- **Evidence classes:** E1 executed here (all counts below); E2 read, limited to the paper's fault-operator table and its Table 2; E3 interpretation.
- **Re-run on 2026-10-26** from the pinned commit in a clean worktree: Parts A and B reproduce the original outputs byte for byte (the error-probe script differs only in the order of two library log lines).

## 3. Predictions scored

| # | Prediction | Result |
|---|---|---|
| A1 | Errors use a top-level `"error"` key; successes do not | **Held, with a split channel.** Runtime failures (bad path, unknown backend, missing API key) return `{"error": ...}` with no protocol error flag. Schema violations (missing or non-string `text`) and unknown tools return a protocol-level error. A client has to check both. No success payload carried an `error` key. |
| A2 | Clean-text scans return a zero-findings shape distinguishable from an error by one key check | **Held**, trivially (no `error` key). The informative fact is A5. |
| A3 | Most tools echo nothing about the input or about what was run | **Held for all eight.** Partial exception: `bifp_scan_text` lists each rule with an explanation ("No provisionalization phrasing matched"), the only tool that makes negative evidence visible. |
| A4 | At least one tool returns a non-dict success | **Not supported** (predicted 0.3). Every probed success was a dict; the 30-tool surface was not probed exhaustively. |
| A5 | Empty input returns a clean-looking result for at least half the text scanners | **Held, stronger than predicted: 8 of 8.** Empty and whitespace-only input return no error and the same structure as clean text; for most tools the output equals the clean-text output. "Scanned nothing" and "scanned, found nothing" are the same response. |
| B1 | Under F7, F8, F10 (plus F1, F9) the naive client is falsely clean at most 5% of the time | **Held** (largest value 0.4%, under F7). |
| B2 | Under shape-preserving faults F3, F4, F5, F6 the naive client is falsely clean at least 80% of the time | **Failed as stated.** F3 1.00, F5 0.83, F6 1.00, but **F4 0.00**. The preregistration was internally inconsistent: the naive rule requires a parseable JSON object, so empty or null text cannot read as clean. Counted as failed, not as an edited rule. |
| B3 | Profile-weighted naive false-clean rate between 2% and 25% | **Held: 3.71%** under the preregistered mapping (section 5), carried by one mode (invalid output, 4.04% of the profile). |
| B4 | The envelope cuts false-clean on F3, F4, F5 to at most 10% and leaves F6 within 30 points | **Failed as stated.** F3, F4 and the transport-level F5a drop to 0, but scanner-level F5b stays at 0.83, and transport-level F6a goes from 1.00 to 0.00 (a 100-point change; the wager said "largely unchanged"). |

## 4. Part A in one paragraph

All eight text scanners return a dict with no `error` key for flagged, clean, empty and whitespace inputs. Several return fixed-shape containers that are simply empty for empty input. None reports the input length, a hash, or which rules ran. Only `paper_rigor_scan` returns an `ok` field; the others return lists of flagged items or booleans such as `any_flagged`, which say nothing about whether the scan ran. Two tools returned zero signals on the known-flagged text. The three corpus tools were called with the wrong argument type (strings where objects are expected) and were **not properly probed**; the Groq-backed tools were exercised only on the missing-key path.

## 5. Part B: the fault simulation

Per-fault false-clean rate (a client concludes "clean" while findings exist), mean over the six scanners; F7, F8 and F10 use 200 seeded trials each:

| Fault | Naive rule | Envelope rule |
|---|---|---|
| F1 protocol error | 0.000 | 0.000 |
| F2 payload error | 0.000 | 0.000 |
| F3 empty object `{}` | **1.000** | 0.000 |
| F4 empty or null text | 0.000 | 0.000 |
| F5a key drift, transport level (inside the result, envelope intact) | 0.833 | 0.000 |
| F5b key drift, scanner level (envelope computed on the drifted output) | 0.833 | **0.833** |
| F6a findings zeroed, transport level | **1.000** | 0.000 |
| F6b findings zeroed, scanner level | **1.000** | **1.000** |
| F7 character corruption | 0.004 | 0.000 |
| F8 word substitution | 0.000 | 0.000 |
| F9 silent drop | 0.000 | 0.000 |
| F10 truncated JSON | 0.000 | 0.000 |
| no-fault control | flagged | flagged |

**The naive rule** is "clean iff the response parses as a JSON object, has no `error` key, and the findings field is missing or empty". **The envelope rule** assumes a wrapper `{ok, tool, schema_version, scanned_chars, rules_evaluated, n_findings, result}` and calls a result clean iff `ok` is true, the tool name and schema version match, `scanned_chars` equals the length sent, `rules_evaluated` is positive and `n_findings` is zero. In the simulation `rules_evaluated` is approximated from the number of top-level keys on a clean run; a real value would need each scanner to report its own rule count.

**Profile weighting (B3).** The six failure modes in Table 2 of the paper are weighted by their counts over the injected persistence classes (13,824 failure threads; "uncertain" excluded): explicit error 71.19%, incorrect output 13.66%, invalid output 4.04%, delayed response 1.51%, silent drop 8.20%, minor mistake 1.39%. These reproduce the paper's printed shares (65.6% explicit-error/permanent alone, 71.2% all explicit errors, 19.1% silent content modes, 9.7% timing modes). The preregistered mapping is explicit error to F1/F2, minor mistake to F7, incorrect output to F8, timing to F9, invalid output to F5/F6. Result: **3.71%** naive false-clean (`profile_weights.py`); with the envelope, 0.00% for transport-level faults and still 3.71% for scanner-level faults.

## 6. The fix, and what it does and does not do

- **What merged.** The cheapest piece, a server-side guard that returns the existing `{"error": ...}` payload for empty or whitespace-only `text` on the eight scanners, merged as PR #68 (the schema and descriptions of all 30 tools are unchanged). Re-running Part A on the merged server: all 16 empty and whitespace cases (eight tools, two inputs) now return an error payload (`partA_output_after_guard.txt`). This was not part of the preregistered wager, which proposed the envelope.
- **The envelope** converts transport-level faults (F3, F5a, F6a) into "unknown". It does **not** touch scanner-level faults (F5b, F6b): a scanner that returns a well-formed zeroed or drifted result is certified by an envelope computed from that output. The envelope adds redundancy, not independence. It also needs a per-scanner rule count, which would change the wrapped functions' output and conflicts with the server's "pure wiring" design note. The wager of "10 to 20 lines, wrapped output untouched" was optimistic.

## 7. What this does and does not establish

- It shows that, on this server, the response alone could not distinguish empty input from clean input, and that a toy client rule can be falsely clean on shape-preserving faults while being almost never fooled by corruption that breaks parsing.
- It does not show anything about LLM clients, nor about servers other than this one. Six scanners, one flagged input, toy rules, fixed seeds, and weights from a single external paper's GitHub-mined profile (which the paper itself says over-represents persistent failures).
- The empty-input guard closes one ambiguity. Scanner-level silent faults remain open.

## 8. What would change this

A client study with real agents on the same fault set; per-scanner rule counts reported by the scanners; a second flagged input per scanner; a run on `mcp` 2.0.0; and a check of the corpus and Groq-backed tools beyond their error paths.

## 9. Reproduction

Everything is in `research_mcp_failure_semantics_probe_v1/`. To reproduce the original numbers, check out commit `b921ff4`, install `tools/research_mcp` and the packages it wraps (editable), and run from this folder with the Groq key unset:

```
python3 -I partA.py     # 4 inputs x 8 text scanners   -> partA_output.txt
python3 -I partA2.py    # error-payload probes         -> partA2_output.txt
python3 -I partB.py     # fault simulation             -> partB_output.txt, partB_results.json, partB_agg.json
python3 -I profile_weights.py                          -> profile_weights_output.txt
```

The scripts import the server's own test harness from `../../../tools/research_mcp` (override with `RESEARCH_MCP_DIR`). On the current `Main` the guard is present: Part A reproduces `*_after_guard.txt` instead. `peek.py` prints the shape of one scanner's response. Tool scans of this draft are in `tool_scan_*.json`.

## References

Sources: `tools/research_mcp` in this repository at `b921ff4` and at `Main` after PR #68; arXiv:2610.32555v1, "MCP-Injector", for the fault operators (OP1 to OP6) and Table 2 (those two items were read on 2026-10-26; the rest of the paper is not evaluated here; PDF sha256 `6e0231e4…`).

## Revision log

- *2026-10-26, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
