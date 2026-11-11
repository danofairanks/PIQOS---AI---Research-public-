"""Arithmetic behind the reading of six provenance sources. Numbers typed from: zkGPT (USENIX Security 2025) abstract and Table 3; the report on provable inference, Section 6. Run: python3 -I checks.py"""
print("== zkGPT Table 3 prover times (seconds), as printed")
t = {"Hao et al (summed from their paper, not run)": 6096, "ZKML (32 thread)": 4026, "Lu et al (VOLE, 32 thread, communication included)": 112.3,
     "zkLLM (6912 CUDA cores, A100)": 15.8, "zkGPT single thread, no optimisations": 319.6, "zkGPT 32 thread, no optimisations": 52.3, "zkGPT 32 thread, all optimisations": 21.8}
ours = t["zkGPT 32 thread, all optimisations"]
for k in list(t)[:4]:
    print(f"  {k}: {t[k]} s ; ratio to zkGPT optimised ({ours} s) = {t[k]/ours:.2f}x")
print("  abstract: 'nearly 279x and 185x' -> the two largest ratios above; body: 5.1x vs the VOLE-based system; '30% slower' than zkLLM (printed times: " + str(round(ours/t['zkLLM (6912 CUDA cores, A100)'], 2)) + " x the time)")
print("  ratios sorted:", sorted(round(v/ours, 2) for v in list(t.values())[:4]), "-> zkGPT is faster than 3 of 4 compared systems, slower than 1; the abstract names the 2 slowest")
print("== report, Section 6")
print("  batch of 24 requests x 1,024 tokens =", 24*1024, "tokens; / 223 s =", round(24*1024/223, 1), "tokens per second (report: 110)")
print("  one request, 1,024 tokens / 58 s =", round(1024/58, 2), "tokens per second (report: 17.6)")
print("  prefill overhead reported: 72x (66-77 across runs), up to 94x at highest vLLM load; appendix: 70-95x a forward pass")
