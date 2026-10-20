"""POST-HOC (added after the preregistered run; not in PREREG predictions).
Tests the declared known limit: a component that inlines U's logic instead of calling U."""
import json, model

class E:   # genuinely enforces the version rule, but with its own copy of the comparison
    def __init__(self, u): self.u = u
    def execute(self, token, payload, current, now):
        if not model.bound_ok(token, payload): return "BLOCK"
        return "EXECUTE" if token["version"] == current else "BLOCK"

model.COMPONENTS["E"] = E
real, stub = model.run("E", model.RealU(), "S"), model.run("E", model.StubTrue(), "S")
label = model.classify("E", "S")[0]
res = {"component": "E (inlined copy of U's comparison)", "S_real": real, "S_stub": stub,
       "detector_label": label, "truth": "enforces the version rule itself",
       "reading": ("OTHER-REASON: blocked with and without U, so the claim holds but is not attributable to U; "
                   "this is the correct reading for an inlined copy. Stub-substitution tests dependence on U, not on the property.")}
json.dump(res, open("posthoc_output.json", "w"), indent=2)
print(json.dumps(res, indent=1))
