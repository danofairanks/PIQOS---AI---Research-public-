"""Arithmetic behind the reading of "AlphaProof Code: Verifying Signal's Security at the Machine-Code Level" (document dated 2026-11-10). Numbers typed from Sections 1, 2, 4, 5.2.5, 7 and Table 1. Run: python3 -I checks.py"""
print("== C1 proof volume (Section 7)")
parts = {"about the binary (shared by both security proofs)": 5.3, "computational proof": 0.86, "symbolic proof": 0.35}
print("  proof lines (M):", parts, "sum", round(sum(parts.values()), 2), "(paper: about 6.5M)")
print("  plus reintroduced-bug proofs 0.14M and allocator 0.07M:", round(sum(parts.values()) + 0.14 + 0.07, 2), "M (paper: nearly 7M counting comments and blank lines)")
print("== C2 trusted lines named in the abstract: 18,000 (statements, definitions) + 8,000 (AArch64 semantics) =", 18000 + 8000, "(abstract: about 26,000)")
print("  not in that figure: a Lean representation of the compiled machine code (about 95,000 lines; extracted by a tool, checked against the bytes, symbol names trusted); the contracts of 39 hooked routines (inside the specification directories of about 54,000 lines, only part trusted)")
print("== C3 effort (Section 7, 2.3)")
print("  five people for four weeks =", 5 * 4, "person-weeks, about", round(5 * 4 / 4.33, 1), "person-months; agents per campaign 40-80 for 24-72 h on one machine; no compute, token or dollar totals stated in the text read")
print("== C4 computational bound scale (Section 5.2.5, if nearly every message starts a new epoch)")
print("  vacuous for one session of about 25,000 messages, or for 2^20 sessions of 2^10 messages =", 2**20 * 2**10, "messages in total")
print("== C5 trusted boundary items counted in the text: 39 hooked routines replaced by contracts; 18 panic entry points end the run with SIGABRT; keygen not verified; one-time Kyber prekeys not covered; at most one one-time prekey for the responder")
