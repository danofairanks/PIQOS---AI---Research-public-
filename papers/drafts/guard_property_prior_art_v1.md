# Where the Guard Property Comes From: A Prior-Art Note on "No Effect Without a Passing Gate"

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The object examined is a property statement published in a public repository, `github.com/LalaSkye/no-direct-bind`, pinned at commit `37af380`; the repository is named by its path because the claim is what its files say. No individual is named and no intent is attributed. Cited prior work is named by its standard citation. The companion draft `model_local_proofs_travel_v1.md` covers how that repository's claim travelled and narrowed; this note asks only where the property itself comes from.

**Disclosure.** Drafted with AI assistance. The web searches and the reading were done by one model, so the search is a same-source check, not independent verification. Section 2 says, row by row, what was read in full, what was read in part, and what is known only from a search result or an index entry. The sandbox that ran the searches could not reach several primary hosts; the texts that were read were supplied by the project's operator.

## 1. The question

The repository states a property of a 13-state model: `NoDirectBind == (phase = "EXECUTED") => (resolvedAllow = TRUE)`. In its own README the property "holds because the model defines the only edge into `EXECUTED` as guarded by `resolvedAllow`", and the claim was narrowed from "theorem" to "model-local property" on 2026-08-30. The question here is narrower than whether the property is true: **is "no effect state is reachable except through an authorizing guard" a new result, or a restatement?**

## 2. What was read, and at what level

| Work | What it contributes | Read |
|---|---|---|
| Anderson et al., Computer Security Technology Planning Study, ESD-TR-73-51 (1972) | Source usually cited for the reference monitor concept | **Not read.** Existence, date and number confirmed by the bibliography of Saltzer and Schroeder [2] and by a collection index whose keyword list includes "reference monitor"; the attribution of the concept to "the Anderson panel" is confirmed by a 1976 report's introduction as quoted in that index |
| Schell, Downey and Popek, Preliminary Notes on the Design of Secure Military Computer Systems, MCI-73-1 (1973) | Names the principles complete mediation, isolation, simplicity | Abstract as quoted in the collection index; paper not read |
| Saltzer and Schroeder, The Protection of Information in Computer Systems (1975) | Complete mediation; fail-safe defaults | The design principles read verbatim; the passages on identification, protection dynamics and authority to change access control lists read; the rest by keyword search only (read as a saved web version, v1.3). Remembered authority checks and revocation during use are addressed there (complete mediation; "problem of dynamics") |
| Reference monitor article (encyclopedia) | Three requirements: always invoked, tamper-proof, evaluable | Read in full; secondary source |
| Schneider, Enforceable Security Policies, ACM TISSEC 3(1):30–50 (2000) | Characterizes which policies monitoring can enforce | Abstract, introduction, section 2 and the pragmatics passage read; sections 3–5 skimmed |
| HALO, arXiv 2607.27636v1 (30 July 2026; preprint) | Agent-era admission and dispatch protocol with a gate-boundary proposition | Main text and the proof statements and threats section of the supplement read; evaluation sections not read |
| Lampson, Protection (1971; Princeton Symposium; reprinted ACM Operating Systems Review 1974) and Dynamic protection structures (1969) | Subjects, objects and the access matrix: access control formulated abstractly | **Protection (1971) read** (PDF and the author's web version; pages 9–10 by keyword search only) as of v1.2; *Dynamic protection structures* (1969) not read. Dates were first taken from the bibliography of Saltzer and Schroeder [2]; the characterization ("the problem of access control is formulated very abstractly for the first time, using the concepts of subjects, object, and access matrix") is from a 1976 report's introduction as quoted in the collection index |
| Graham and Denning, Protection: principles and practice (1972); Harrison, Ruzzo and Ullman, Protection in operating systems (1976) | Rules for changing an access matrix; safety of rights in a matrix model | Graham and Denning **not read**. Harrison, Ruzzo and Ullman read as an eleven-page conference-length PDF as of v1.2 (the CACM version was not read); named from memory only before that |
| Alpern and Schneider, Defining Liveness (1985); Hardy, The Confused Deputy (1988); Strom and Yemini, Typestate (1986) | Safety properties; ambient authority; state-dependent operation validity | **Not read**; known from search results only |

## 3. What the lineage says

**Mediation (1973–1975).** The 1973 notes state that the system must "interpose itself between any reference to sensitive data and accession of that data", that the validating mechanism must be "an isolated, tamper-proof component", and that it must be simple enough to certify (quoted from the index abstract). Saltzer and Schroeder state, verbatim, "Every access to every object must be checked for authority", and that "the default situation is lack of access". The repository's guard-before-effect with a default hold is these two principles. The 1975 text also warns that "proposals to gain performance by remembering the result of an authority check be examined skeptically. If a change in authority occurs, such remembered results must be systematically updated", the concern now discussed as check-to-use or stale approval, and says complete mediation includes "initialization, recovery, shutdown, and maintenance".

**The authorization-state model (1969–1976).** The access matrix (subjects by objects, cells holding rights) is the older object that a guard consults: "allowed" means a right is in a cell, and a changed authority state means a changed matrix. Seen that way, the repository's `resolvedAllow` is one matrix lookup with the matrix left implicit, and the "stale authority" and "rollback" concerns of the agent-era literature are questions about when a cell was last read and whether an older matrix state can be restored. The safety question for such models (whether a right can leak) was posed in the mid-1970s as well (named from memory; not read here). That bears on the repository's own limit: a check over a declared model says nothing about commands or paths the model omits.

**Enforceability (2000).** ("Safety property" here is the formal-methods term from the 1985 liveness paper: a property whose violation shows in a finite prefix of an execution. It is not the AI-safety sense.) Schneider's execution-monitoring class "includes security kernels, reference monitors, firewalls, and most other operating system and hardware-supported enforcement mechanisms", and a policy is enforceable by such a mechanism only if it is a safety property. "No effect state without an ALLOW" is a safety property of that kind. Schneider also states the conditions under which an automaton-style gate gives its guarantee: its input must be "both correct and complete" and the "complete mediation" requirement "is one way to discharge this assumption"; the mechanism must be isolated, its state not writable by the target.

**Agent-era restatement (2026).** HALO's gate-boundary integrity proposition says that if the adapter is called for an action, then retention, prerequisite readiness, an unchanged witness and an unused authorization all hold at the decision point, and the token authorizes at most one call. The supplement's proof turns on the gate being "the adapter's sole entry"; the stated preconditions are a trusted catalog, faithful state providers and an enforced ledger, and bypasses, undeclared dependencies and provider failures are outside its boundary. The authors write that the contribution "is not a new predicate language, freshness metric, or authorization primitive". In the text read, HALO cites none of the mediation or enforceability works above. What it adds is dependency-closed retention, a hash-bound exact-action identity with a one-shot token consumed in the same critical section as the call, and scoped fresh readmission. Its evaluation is the authors' own.

## 4. What the model-local check does and does not establish

The enumeration over 13 states checks a model whose only edge into the effect state is guarded; the property cannot fail in that model, and the repository's README says so. The reference-monitor lineage names the three things such a model leaves out: that the gate is always invoked, that it is isolated from what it governs, and that it can be verified. Schneider's paper makes the first two explicit assumptions of any gate-style guarantee. HALO states the same assumptions in its trust model. The check is therefore a correct restatement of the 1970s property inside a toy topology, not a new result, and the repository's own narrowing agrees.

## 5. What remains open

- Whether the repository's gate-token semantics (its ALLOW and HOLD states and evidence labels) differ in substance from the 1975 default-deny gate. This note did not compare them and does not establish that they are new or old.
- The primary wording of the 1972 report and of the 1973 notes, which would settle the attribution dispute noted in the encyclopedia article (one oral history credits a 1972 conference paper by other authors).
- Sections 3–5 of the 2000 paper, the 1985, 1986 and 1988 papers, HALO's evaluation, and the access-matrix papers of 1969–1976.

## 6. Limitations

One model searched and read; the sandbox blocked the primary hosts for the 1972 and 1973 reports; the 1972 and 1973 rows rest on indexes and quotations; the 2026 paper is a preprint and was read only in part; the search covered a few queries and found no source using the repository's exact name, which is weak evidence that none exists; the comparison to HALO is of stated propositions, not of behaviour; nothing here tests the repository's code.

## 7. Reproduction

No code is involved. Each cited work can be retrieved from the references below; the verbatim passages quoted in section 3 are from the saved copies the project's operator supplied.

## References

Sources: [1] the repository `github.com/LalaSkye/no-direct-bind` at commit `37af380` (README). [2] J. H. Saltzer and M. D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE, 1975. [3] J. P. Anderson, Computer Security Technology Planning Study, ESD-TR-73-51, Air Force Electronic Systems Division, October 1972. [4] R. R. Schell, P. J. Downey and G. J. Popek, Preliminary Notes on the Design of Secure Military Computer Systems, MCI-73-1, January 1973. [5] F. B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1):30–50, 2000. [6] B. Alpern and F. B. Schneider, Defining liveness, Information Processing Letters 21(4):181–185, 1985. [7] N. Hardy, The confused deputy, 1988. [8] R. E. Strom and S. Yemini, Typestate: a programming language concept for enhancing software reliability, IEEE Transactions on Software Engineering 12:157–171, 1986. [9] HALO: Heterogeneous Admission through Localized Obligations for Safe Agentic Execution, arXiv:2607.27636v1, 30 July 2026. [10] B. W. Lampson, Protection, Proc. 5th Princeton Symposium on Information Science and Systems, 1971; and Dynamic protection structures, AFIPS FJCC 1969 (as cited in [2]). [11] G. S. Graham and P. J. Denning, Protection: principles and practice, 1972; M. A. Harrison, W. L. Ruzzo and J. D. Ullman, Protection in operating systems, Communications of the ACM, 1976 (named from memory). [12] the collection "Early Computer Security Papers, Part I" (index and landing page), UC Davis Computer Security Laboratory.

## Revision log

- *2026-10-09, v1.5.* Biba (MITRE MTR-3153, 1975 edition) and Bell and La Padula (MTR-2997 Rev. 1, 1976) read in part from scans: the threat taxonomy and the statement that dynamic access control does not address internal threats (Biba); the star property, trusted subjects and the section on indirect communication paths (Bell and La Padula). Mapped in section 5a of `rsi_gate_audit_results_v1.md`.
- *2026-10-09, v1.4.* Clark and Wilson (1987) read in part as a reprint (NIST SP 500-160, Appendix A1, rules pages); relevant for certification versus enforcement, total input validation, and separating the certifier from execution. Mapped in section 3a of `public_admissibility_evaluators_v1.md`. Bell-LaPadula and Biba still not read.
- *2026-10-08, v1.3.* Saltzer and Schroeder read beyond the design principles (identification, dynamics, authority to change access control lists); the row says which parts.
- *2026-10-08, v1.2.* Read Lampson (1971) and Harrison, Ruzzo and Ullman as primaries; the row text above says which parts. A detailed mapping to a different draft is in section 3a of `public_admissibility_evaluators_v1.md`. Graham and Denning still not read.
- *2026-10-08, v1.1.* Added the access-matrix lineage (Lampson 1969 and 1971; Graham-Denning; Harrison-Ruzzo-Ullman), marked not read.
- *2026-10-07, v1.* First version. Rows marked "not read" are the next revision's work; the order is the 1972 report, then the 1973 notes, then the remaining sections of the 2000 paper.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
