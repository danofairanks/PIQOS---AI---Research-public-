"""Checks on TheoPhysEval Table IV / X (PREREG.md). Stdlib only. Run: python3 -I checks_from_reported_tables.py"""
import re, math, hashlib, os, itertools
here = os.path.dirname(os.path.abspath(__file__))
print("PREREG sha256:", hashlib.sha256(open(os.path.join(here, "PREREG.md"), "rb").read()).hexdigest())
txt = open(os.path.join(here, "extracted_text.txt"), encoding="utf-8").read()
pages = {int(a): b for a, b in re.findall(r"=====PAGE (\d+)=====\n(.*?)(?=\n=====PAGE|\Z)", txt, re.S)}
flat = lambda s: " ".join(s.split())

# ---- parse Table IV (page 50)
p50 = flat(pages[50]); i = p50.index("TABLE IV")
body = p50[p50.index("GLM R I R I R I R I R I") + len("GLM R I R I R I R I R I"):p50.index("Solved")]
rows = re.findall(r"(.+?\(§\d+[a-z]\))\s+((?:[01]\s+){9}[01])", body + " ")
names = []; G = {}   # G[agent][track] = list of 0/1
agents = ["Astra", "Opus", "Gemini", "DeepSeek", "GLM"]
for ag in agents: G[ag] = {"R": [], "I": []}
for nm, nums in rows:
    v = list(map(int, nums.split())); names.append(nm.strip())
    for k, ag in enumerate(agents):
        G[ag]["R"].append(v[2 * k]); G[ag]["I"].append(v[2 * k + 1])
print("rows parsed:", len(names))
printed = {"Astra": (49, 46), "Opus": (46, 46), "Gemini": (34, 31), "DeepSeek": (27, 25), "GLM": (21, 26)}
print("\n== C1 parse vs printed totals")
ok = True
for ag in agents:
    r, i_ = sum(G[ag]["R"]), sum(G[ag]["I"]); same = (r, i_) == printed[ag]; ok &= same
    print(f"  {ag:9s} R={r} I={i_} printed={printed[ag]} {'OK' if same else 'MISMATCH'}")
print("  all match:", ok)

def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
print("\n== C2 Wilson 95% CIs")
for ag in agents:
    for tr in "RI":
        k = sum(G[ag][tr]); lo, hi = wilson(k, 50); print(f"  {ag:9s} {tr}: {k}/50 = {k/50:.2f}  CI [{lo:.3f}, {hi:.3f}]")

def binom_two_sided(b, n):  # exact sign test, p=0.5
    if n == 0: return 1.0
    k = min(b, n - b); s = sum(math.comb(n, j) for j in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * s)
print("\n== C3 paired R vs I per agent (exact McNemar)")
tot_b = tot_c = 0
for ag in agents:
    b = sum(1 for r, i_ in zip(G[ag]["R"], G[ag]["I"]) if r == 1 and i_ == 0)   # R only
    c = sum(1 for r, i_ in zip(G[ag]["R"], G[ag]["I"]) if r == 0 and i_ == 1)   # I only
    tot_b += b; tot_c += c
    print(f"  {ag:9s} R-only={b} I-only={c} net(R-I)={b-c:+d} discordant={b+c} p={binom_two_sided(b, b+c):.3f}")
print(f"\n== C4 pooled: R-only={tot_b} I-only={tot_c} net={tot_b-tot_c:+d} discordant={tot_b+tot_c} exact p={binom_two_sided(tot_b, tot_b+tot_c):.3f}")
print("   (treats agent-problem pairs as independent; they are not, so this p is optimistic)")

print("\n== C5 subset claim")
unsolved_by_all_R = [n for j, n in enumerate(names) if all(G[a]["R"][j] == 0 for a in agents)]
print("  problems unsolved by every agent on R:", unsolved_by_all_R)
astraR = {j for j, v in enumerate(G["Astra"]["R"]) if v}
for ag in agents:
    for tr in "RI":
        s = {j for j, v in enumerate(G[ag][tr]) if v}
        print(f"  {ag:9s}{tr} subset of Astra-R: {s <= astraR}  (|set|={len(s)})")
print("  Problems outside Astra-R:", [names[j] for j in range(50) if j not in astraR], "-> the claim can only fail on these.")

print("\n== C6 saturation")
allR = [j for j in range(50) if all(G[a]["R"][j] for a in agents)]
allI = [j for j in range(50) if all(G[a]["I"][j] for a in agents)]
both = [j for j in range(50) if G["Astra"]["R"][j] and G["Opus"]["R"][j]]
print(f"  solved by all 5 (R)={len(allR)}  (I)={len(allI)}; solved by Astra and Opus (R)={len(both)}")
only_a = [names[j] for j in range(50) if G["Astra"]["R"][j] and not G["Opus"]["R"][j]]
only_o = [names[j] for j in range(50) if G["Opus"]["R"][j] and not G["Astra"]["R"][j]]
print(f"  Astra-R only: {only_a}\n  Opus-R only:  {only_o}")

print("\n== C7 nestedness (R)")
def frac(a, b):
    sa = [j for j in range(50) if G[a]["R"][j]]; return sum(G[b]["R"][j] for j in sa) / len(sa)
print(f"  Opus passes also Astra passes: {frac('Opus','Astra'):.3f}")
print(f"  Gemini passes also Opus passes: {frac('Gemini','Opus'):.3f}")
print(f"  DeepSeek passes also Gemini passes: {frac('DeepSeek','Gemini'):.3f}")
print(f"  GLM passes also Gemini passes: {frac('GLM','Gemini'):.3f}")

print("\n== C8 linked sets (exploratory)")
def idx(prefix): return [j for j, n in enumerate(names) if re.search(r"\(§" + prefix + r"[a-z]\)", n)]
linked = {"§6 a-d electronic structure": idx("6"), "§5 c-e maple-leaf": [j for j, n in enumerate(names) if re.search(r"\(§5[cde]\)", n)]}
for lab, js in linked.items():
    print(f"  {lab}: {len(js)} problems {[names[j] for j in js]}")
    for ag in agents:
        for tr in "RI":
            v = [G[ag][tr][j] for j in js]; print(f"    {ag:9s}{tr}: {v}")
allj = set(j for js in linked.values() for j in js)
rest = [j for j in range(50) if j not in allj]
def same_rate(js, tr):
    n = agree = 0
    for j in js:
        for ag in agents: pass
    return None
# per agent R-vs-I agreement inside linked vs outside
for lab, js in [("linked", sorted(allj)), ("rest", rest)]:
    agree = sum(G[a]["R"][j] == G[a]["I"][j] for a in agents for j in js); n = len(agents) * len(js)
    print(f"  R/I same-outcome rate, {lab}: {agree}/{n} = {agree/n:.3f}")
net_link = sum(G[a]["R"][j] - G[a]["I"][j] for a in agents for j in sorted(allj)); net_rest = sum(G[a]["R"][j] - G[a]["I"][j] for a in agents for j in rest)
print(f"  net R-I passes inside linked sets: {net_link:+d}; outside: {net_rest:+d}")
glm_link = sum(G['GLM']['R'][j] - G['GLM']['I'][j] for j in sorted(allj))
print(f"  GLM net R-I inside linked sets: {glm_link:+d}; GLM net overall: {sum(G['GLM']['R'])-sum(G['GLM']['I']):+d}")

print("\n== C9 costs (Table X)")
p56 = flat(pages[56]); body = p56[p56.index("GLM Problem R I"):]
tot = re.search(r"Total ([\d. ]+) TABLE X", body).group(1).split()
crow = re.findall(r"(\(§\d+[a-z]\))\s+((?:[\d.]+\s+){9}[\d.]+)", body)
print("  rows parsed:", len(crow))
sums = [0.0] * 10
for _, nums in crow:
    for k, v in enumerate(map(float, nums.split())): sums[k] += v
for k, (a, b) in enumerate(zip(sums, tot)): print(f"   col{k}: sum={a:.2f} printed={b}")
print(f"  Astra realistic mean per problem = {float(tot[0])/50:.2f} USD (claim: under 3)")
print(f"  Opus mean R={float(tot[2])/50:.2f}; Gemini R={float(tot[4])/50:.2f}; DeepSeek R={float(tot[6])/50:.2f}")

print("\n== C10 section 1b spend (tokens in millions: total)")
# Table V-IX first columns for 'Autonomous equation (§1b)'
for tbl, ag in [(51, "Astra"), (52, "Opus"), (53, "Gemini"), (54, "DeepSeek"), (55, "GLM")]:
    m = re.search(r"Autonomous equation \(§1b\)\s+([\d. ]+?)\s+Inertial", flat(pages[tbl]))
    v = m.group(1).split(); print(f"  {ag:9s} R total={v[3]}  I total={v[7]}")
