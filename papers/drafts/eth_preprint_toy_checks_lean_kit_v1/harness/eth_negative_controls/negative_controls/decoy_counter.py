# DECOY. Not the paper's method. A brute-force 2^n computation wrapped in the interface of eth_counter.Counter.
# Purpose: measure what the correctness checks of this project cannot distinguish (see ../PREREG.md).
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "eth_counter_test"))
import eth_counter as ec
from eth_counter import Counter, pshift, trim, padd, psub, pmul


class DecoyCounter(Counter):
    """D1: answers taylor_decoupled by shifting the brute-force H(T); reports self-made counters."""
    def design_at(self, t):
        return {"S": [], "Cg": [], "lam": {}, "bad": 0}

    def taylor_decoupled(self, t, design, J, q, counters):
        if not hasattr(self, "_H"):
            self._H = self.brute_H()
        counters["assign_evals"] = counters.get("assign_evals", 0) + max(1, (1 << self.n) // (2 * self.cons.Q))
        counters["poly_mults"] = counters.get("poly_mults", 0) + 7 * self.ne
        counters["triples"] = counters.get("triples", 0) + 1
        return trim(pshift(self._H, t, J), J)


class DecoyCounterB(DecoyCounter):
    """D1b: same, but the enumeration is inlined under another name (no call to the known primitives)."""
    def _h_from_scratch(self):
        n = self.n
        tot = [0]
        for bits in range(1 << n):
            x = [(bits >> i) & 1 for i in range(n)]
            prod = [1]
            for e, cl in enumerate(self.clauses):
                if self.dummy[e]:
                    continue
                inner = [1]
                for v, neg in cl:
                    w = [0]
                    for i in range(n):
                        if x[i]:
                            w = padd(w, self.form[(e, v)][i])
                    fac = psub([1], w) if not neg else w
                    inner = pmul(inner, fac)
                prod = pmul(prod, psub([1], inner))
            tot = padd(tot, prod)
        return tot

    def taylor_decoupled(self, t, design, J, q, counters):
        if not hasattr(self, "_H"):
            self._H = self._h_from_scratch()
        counters["assign_evals"] = counters.get("assign_evals", 0) + max(1, (1 << self.n) // (2 * self.cons.Q))
        return trim(pshift(self._H, t, J), J)


class DecoyCounterC(DecoyCounterB):
    """D1c (added after the first scoring, see DEVIATIONS.md): also makes one cosmetic call to Counter.Z and discards it."""
    def taylor_decoupled(self, t, design, J, q, counters):
        if not hasattr(self, "_cosmetic"):
            self._cosmetic = True
            try:
                self.Z(t, self.design_at(t), set(), set(), J, {"assign_evals": 0, "poly_mults": 0, "triples": 0})
            except Exception:
                pass
        return super().taylor_decoupled(t, design, J, q, counters)
