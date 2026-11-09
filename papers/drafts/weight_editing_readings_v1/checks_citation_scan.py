"""Do the objects cite the adverse or related literature, or use controls, or state what would count against the claim? Counts only.
Term lists fixed before running. Usage: python3 -I checks_citation_scan.py <config.json: {label: [file paths]}>
A term hit is a lead; every hit was read by hand and the reading is in the entries. Absence = not found in the saved text."""
import re, sys, json, os
CFG = json.load(open(sys.argv[1]))
ADVERSE = {
 "editing-failure literature": r"\bROME\b|\bMEMIT\b|Meng et al|model editing|knowledge editing|catastrophic forgetting|gradual forgetting|CounterFact|zsRE|KnowEdit|EasyEdit",
 "removal-durability / refusal-direction literature": r"Arditi|single direction|abliterat|relearn|unlearning|ROSI|extended-refusal",
 "self-modification integrity literature": r"reward hack|tamper|e-process|anytime-valid|Statistical G.del|Darwin G.del|trusting trust|always-valid|alpha.spending|familywise",
}
CONTROLS = {
 "controls / null results (terms)": r"deranged|negative control|null control|random[- ]direction|random control|norm-matched|harmless[- ]direction|placebo",
 "stated-in-advance wording": r"defeat condition|would (count|be counted) against|would refute|preregist|pre-registered|prespecified",
}
for label, files in CFG.items():
    ex = [f for f in files if os.path.exists(f)]
    texts = [open(f, encoding="utf8", errors="ignore").read() for f in ex]
    out = []
    for grp in (ADVERSE, CONTROLS):
        for k, rx in grp.items():
            out.append(f"{k}: {sum(len(re.findall(rx, t, re.I)) for t in texts)}")
    print(f"{label} (files read {len(ex)} of {len(files)}): " + "; ".join(out))
