*Copied verbatim from the evaluator's working note below the rule. The date in its title line is the working note's own; the work was done on 2026-10-26. The file was written before any tool output was inspected; that order is the evaluator's own record and is not independently timestamped.*

---

# Preregistration — research_mcp failure-semantics probe (written 2026-10-27, BEFORE any tool output was inspected)
Object: our own public server `tools/research_mcp` (read at the public repo's current `Main`, local working copy; nothing modified there). Motivation: arXiv 2610.32555 (MCP-Injector) injects MCP-level faults and measures agent degradation; it does not test whether a client can tell "scanned, nothing found" from "not scanned" for tools whose success output is an empty findings list. Method here: no LLM and no third-party artifact; a deterministic probe plus a response-level fault simulation with two toy client rules. **Toy clients are not an LLM agent; results say what a rule can distinguish from the response, not what a model does.** Same-source caveat: I wrote both the probe and the predictions. Post-hoc status of anything not listed here is stated in RESULTS.md.

## Part A — what the responses look like (static probe over the registered tools)
Inputs per tool: (a) text with known flags, (b) clean text, (c) empty string, (d) invalid parameter, (e) missing API key for the three Groq tools.
A1 Error payloads use a top-level "error" key; success payloads do not. [0.85]
A2 Clean-text scans return a distinct "zero findings" shape (empty list or zero count), distinguishable from an error payload by one key check. [0.8]
A3 Most tools do not echo anything about the input (length, hash) or about what was run (rules evaluated), so a truncated input or a skipped rule set is invisible in the output. [0.8]
A4 At least one registered tool returns a non-dict success value (bare list or string), so a generic `"error" in result` check would be wrong or raise. [0.3]
A5 The empty-string input (c) returns a "clean-looking" result (no error, zero findings) for at least half of the text-scanning tools. [0.7]

## Part B — fault simulation on real responses
Faults applied to the real response of each text-scanning tool on the known-flagged input (ground truth: findings present): F1 protocol-level error (isError), F2 payload-level error object, F3 empty object `{}`, F4 null/empty text, F5 key drift (rename the findings key), F6 findings zeroed (keep shape), F7 text corruption (random character replacement, paper OP1-style; may break JSON), F8 word substitution (OP2-style), F9 silent drop (client timeout), F10 truncated JSON.
Client rules: R_naive = "clean iff the response parses as JSON, has no 'error' key, and the findings key is missing or empty". R_env (after the wagered fix) = "clean iff ok is true, tool name matches, schema_version known, scanned_chars equals the length sent, rules_evaluated > 0, and n_findings == 0; otherwise unknown or flagged".
B1 Under the paper-style text operators (F7, F8, F10, plus F1, F9) R_naive false-clean (concluding clean when findings exist) is at most 5%: corruption mostly breaks parsing or raises. [0.8]
B2 Under shape-preserving faults (F3, F4, F5, F6) R_naive false-clean is at least 80%. [0.8]
B3 Weighted by the paper's mined profile (Table 2, six modes mapped to F1/F2, F7, F8, F9, F6/F5), R_naive false-clean overall is between 2% and 25%. [0.6]
B4 R_env cuts false-clean on F3, F4, F5 to at most 10%, and does not change F6 (a fault that zeroes findings but leaves the envelope intact) by more than 30 points. [0.7]

## Fix wagered before measuring
Server-side envelope around every text-scanning tool result: `{ok, tool, schema_version, scanned_chars, rules_evaluated, n_findings, result}`, plus one sentence in the server instructions: an empty findings list means clean only if ok is true, scanned_chars equals what was sent and rules_evaluated > 0. Prototype in scratch only; the public repo is not modified.
Wager: the envelope plus rule removes the false-clean reads of F3, F4, F5 and leaves F6 largely unchanged; it costs roughly 10-20 lines in `server.py` and does not alter the wrapped functions' own output (kept under `result`).

## Reporting
Predictions that fail are reported as failed. The probe prints raw shapes; any tool I cannot call without credentials or a corpus is listed as not probed.
