# The induction lemma behind Theorem D.1, written explicitly (reconstruction)
Status: **my reconstruction** of the statement that the proof of Theorem D.1 (OpenAI, "The Exponential Time Hypothesis is False", 25 Oct 2026, Appendix D.4) runs, but never isolates. Not authored by the paper's authors, not independently reviewed. Every obligation below cites the paper's lemma it uses and the status of my checks (R = read and re-derived by hand; T = tested numerically/exactly at small scale; M = modeled in the log domain; N = not tested). Where I add something the paper leaves implicit I mark it **[added]**.

## 0. Fixed data (all from D.4.1-D.4.2)
- s: size parameter; lambda = ceil(log2 s); e = 4 lambda. f in Z[U] monic of degree e, irreducible mod 2. O = Z_(2)[U]/(f), K = Q[U]/(f), A = O[V]/(V^ell), A_p = A/2^p, ell <= Cs. v2 on K is multiplicative (D.4.1).
- eps = 1/(128*1024), r = 64, Delta = ceil(s^{9/10}), H = ceil(s/floor(sqrt lambda)).
- Depth schedule (function of d only): u_d = floor(eps lambda / 2^d); a_d = 2 sum_{j<=d} u_j (a_{-1} = 0); L_d = 2^{a_d}; D_arr,d = r^{2 a_d}; alpha_d = 2^{a_d+1}; S_d = {-L_d, ..., L_d - 1}; C(T) = prod_{t in S_d}(T - t).
- For a call with M edges at depth d: h = ceil(3M/u_d); active nodes T_d = {t in S_d \ {0} : v2(t) < u_d}; for t in T_d: i = v2(t), q_t = h (u_d - i), D_t = L_d/2^i, child precision p_t = p + 8 h D_t + 8 M (a_d + 1).
- Interpolation values: Z = a set of M(2L_d - 1) + 1 elements of O with coordinates in {0,1} on 1, U, ..., U^{e-1}, with pairwise distinct residues mod 2 (so pairwise differences are units of O; 2^e = 2^{4 lambda} > Cs 2^{a_d+1} suffices).
- Depth bound d* = least d with C s 8^{-d} <= H (so d* = log8(C sqrt lambda) + O(1)).

## 1. Objects **[added: the paper never defines the class the recursion acts on]**
**Tagged network.** N = (G, (tau_v)_{v in V}): G = (V_1 u V_2, E) a bipartite multigraph (parallel edges allowed, distinct ports); every edge carries one bit; delta(v) = ordered ports of v. Every vertex v has an *immutable description* <v> (shared by reference), a *creation precision* kappa(v) >= 1, and an entry routine that, given a bit assignment b on delta(v), outputs integers in [0, 2^{kappa(v)}) (the coordinates of the entry in the basis U^i V^j, 0 <= i < e, 0 <= j < ell). The **canonical lift** entry~_v(b) in A is the element with exactly those integer coordinates. Contraction of the lifted tensors:
  Z(N) = sum_{b in {0,1}^E} prod_{v} entry~_v(b|delta(v))  in A.
(Canonical lifts need not respect addition or multiplication; Z(N) is *defined* with them, D.4.1.)

**Admissibility.** N is (d,p)-admissible if
- (A1) M(N) := |E| <= C s 8^{-d};
- (A2) every vertex has degree <= Delta;
- (A3) |V| <= s^{c_V} for a fixed constant c_V;
- (A4) kappa(v) <= p for all v; each description has <= s^{c_D} bits; each entry is computable in time <= (s + L)^b 2^{A s^{9/10}} and space <= (s + L)^b for L = L_{d'}, d' <= d;
- (A5) p <= pi_d, where pi_0 = C s and pi_{d+1} = pi_d + 8 ceil(3 M_d/u_d) 2^{a_d} + 8 M_d (a_d + 1) with M_d := C s 8^{-d} (the worst-case precision schedule).

**Root.** The input of Theorem D.1 (bipartite network, <= Cs edges, degrees <= Delta, entries in B_{P0,ell} = (Z/2^{P0})[V]/(V^ell), poly(s) vertices, entries computable in time (s+L)^b 2^{A s^{9/10}}) is a (0, P0)-admissible tagged network with kappa = P0 whose entries are the integer representatives of the B-entries; and (reduction of the integer polynomial Z(N) modulo 2^{P0}) = (the contraction in B_{P0,ell}), because contraction is a polynomial in the entries. So the Theorem is the case d = 0, p = P0 of the lemma. (A5) at d = 0 requires P0 <= Cs, which is the theorem's hypothesis 1 <= P0 <= Cs.

## 2. The lemma
**Parameter regime (P)** (replaces "for all sufficiently large s"; see section 5). For every d < d*: (P1) u_d >= 1 and 2u_d <= a_d; (P2) a_d <= 4 eps lambda, L_d and D_arr,d <= s^{1/1000}; (P3) with M > H: M >= 2 D_arr,d^2 Delta, M >= L_d D_arr,d, 2 L_d <= Delta; (P4) M(2L_d - 1) + 1 <= 2^e; (P5) u_d <= M. (Correctness uses only (P1)-(P5); the running-time bound additionally uses (P6) below.)

**Lemma (Contract).** Assume (P). For every d >= 0, every p >= 1 and every (d,p)-admissible tagged network N there is a deterministic algorithm Contract(N,d,p) that outputs Z(N) mod 2^p (a vector of e*ell residues mod 2^p). Let c(M,d) bound its number of leaf evaluations. If (P6) [precision schedule, D.11: pi_d is polynomial in s and p_t = O_C(M D_t/u_d) for all t in T_d, M > H] also holds then
  - c(M,d) <= prod_{d'=d}^{d*-1} s^{c_1} exp(c_2 (s/sqrt lambda) 2^{-5d'/2}),
  - the running time is <= s^{c_3} * 2^{H} * (calls) + (entry-evaluation cost, <= (s+L)^b 2^{O(s^{9/10})} per entry), and the space is polynomial in s + L (depth-first; O(log lambda) stack frames).

## 3. Proof (strong induction on M(N); M strictly drops by a factor > 8 per recursive level)
**Base (leaf): M <= H.** Enumerate all b in {0,1}^E (2^M <= 2^H), compute each product of entries mod 2^p (each entry from its description mod 2^kappa, lifted, reduced mod 2^p, using kappa <= p by (A4)), sum. Correct by definition of Z(N). Cost 2^H poly. [R]

**Step (active: M > H, so d < d* by (A1)).**
1. *Packing.* By (A1),(A2),(P3) the hypotheses (D.6) of Lemma D.3 hold; Lemma D.3 gives (deterministically) labels in [r]^{a_d} for the vertices on each side and an embedding of the edges into <= 3M/L_d packets of L_d slots such that each edge occupies the same slot at its two ends, per packet and coordinate the unordered symbol pair is fixed and its orientation is bit i of the slot number when the symbols differ, and each symbol of each coordinate has <= 3M/r real ports per side. [R; T at (r,a) <= (3,2)] 
2. *Deformation.* For each packet and slots x,y: W_xy(T) = C(T)/(C'(0)(T - (y - x))); W(0) = I; deg W_xy = 2L - 1. Let rows/columns be the two sides of N (the side V_1 vs V_2 as given), A(Y) = product of lifted row tensors on row-port bits Y, B(X) likewise for columns, and
   F(T) = sum_{X,Y in {0,1}^M} A(Y) B(X) prod_{row ports x} l_{Y_x}((W(T) X)_x),  l_0(z) = 1 - z, l_1(z) = z.
   Then F(0) = sum_X A(X) B(X) = Z(N) (identity because W(0) = I); F in (K[V]/V^ell)[T] has degree <= M(2L - 1); and for every t in S_d, F(t + alpha z) in A[z] (Lemma D.4: v2(C'(t)) = v2(C'(0)), W(t + alpha z) in O[z]). [R; T for D.4 a <= 4]
3. *Recovery.* Lemma D.5 (u = u_d, 1 <= u <= a_d by (P1), M >= u by (P5)): F(0) mod 2^p is a Z-linear function (explicit, (D.9)) of the first q_t coefficients of F(t + alpha z) mod 2^{p_t} for t in T_d. [R; T for a <= 3]
4. *Evaluating F(t + alpha zeta) mod 2^{p_t}* (t in T_d, zeta in Z). Put i = v2(t) < u_d and group vertices by their symbol in coordinate i (this grouping depends on t). W(t) is local; the crossing entries of W(t + alpha zeta) are expanded by (D.12) modulo 2^{p_t} into modes of weight b+1 (coefficient divisible by 2^{weight}), the number of mode variables of each weight is <= 6M/D_t (D.13), and only exponent tuples beta with sum w beta < p_t contribute (D.14). The identity (D.16) holds: F(t + alpha zeta) = sum_{beta : sum w beta < p_t} prod_{g in [r]} Z_{g,beta} (mod 2^{p_t}), where Z_{g,beta} = Z(N_{g,beta}) for the **child network** N_{g,beta}: sides = (retained group-g vertices, one packet vertex per packet), edges = the retained ports (row-port bits Y_x and column-port bits X_y of group g) joining a retained vertex to its packet vertex; retained vertices keep their tensors and descriptions; the packet vertex of packet pi has the tensor (extraction of the beta-coefficient, over the targeted modes, of the product of the affine row factors of group g in pi) times (the powers L_Z(X)^{beta_Z} of the source-mode forms of group g), entries computed modulo 2^{p_t} from the description (pi, t, zeta, beta, p_t, pointers to the parent's descriptions) and then canonically lifted, kappa(packet) := p_t. [R; T for (D.16) at a <= 3, p <= 5]
5. *The children are (d+1, p_t)-admissible.* (A1): |E(N_{g,beta})| <= 6M/r = 3M/32 < M/8 <= C s 8^{-(d+1)}. (A2): retained vertices keep their degree (each port becomes one child edge), packet vertices have <= 2 L_d <= Delta ports by (P3). (A3): |V(N_{g,beta})| <= |V| + 3M. (A4): retained tensors are evaluated from their immutable descriptions (kappa <= p <= p_t, so their canonical representatives are unchanged); a packet entry costs exp(O(L_d log s)) <= exp(O(s^{1/1000} log s)) <= 2^{A s^{9/10}}; descriptions are polynomial-size. (A5): p_t <= p + 8 h D_t + 8M(a_d+1) <= pi_{d+1} because h, D_t <= 2^{a_d}, M <= M_d are monotone. [R; M for (A5)] 
6. *Call the children and interpolate.* By the induction hypothesis (M(N_{g,beta}) < M(N)) Contract(N_{g,beta}, d+1, p_t) returns Z_{g,beta} mod 2^{p_t}. Sum over beta and multiply over g to get F(t + alpha zeta) mod 2^{p_t}. For each t in T_d evaluate at all zeta in Z; since F(t + alpha z) in A[z] has degree <= M(2L - 1) and the zeta differences are units, Lagrange interpolation over A_{p_t} gives F(t + alpha z) mod 2^{p_t}. Apply step 3. Return F(0) mod 2^p = Z(N) mod 2^p. [R]

**Complexity (needs (P6)).** Per call the number of (t, zeta, beta, g) is s^{O(1)} * #beta, #beta <= exp(theta p_t + (6M/D_t) sum_j -ln(1 - e^{-theta j})) <= exp((1 + pi^2) sqrt(M p_t/D_t)) = exp(O_C(M/sqrt(u_d))) (D.15); with M <= C s 8^{-d}, u_d = Theta(lambda/2^d): exp(O_C((s/sqrt lambda) 2^{-5d/2})). The leaf count multiplies over depths, giving exp(O(s/sqrt lambda) + O(lambda log lambda)); each leaf costs 2^H poly; entry costs are as in (A4); the stack has O(log lambda) frames, each of size poly(s + L). [R; M]

## 4. Proof obligations and status
| # | Obligation | Source | Status |
|---|---|---|---|
| O1 | W(0) = I; deg 2L-1; W(t+alpha z) integral and even off the diagonal t | Lemma D.4 | R, T (a <= 4, 262,144 coefficients) |
| O2 | sum q_t > M(2L-1); valuation of E_t(0) >= -6 D_t h; recovery from data mod 2^{p_t} | Lemma D.5, (D.9),(D.10) | R, T (10,328 valuation cases; 396/396 recoveries at stated margin; fails at zero margin) |
| O3 | packing with properties (1)-(3) | Lemma D.3 | R, T ((r,a) <= (3,2)) |
| O4 | mode expansion valid mod 2^{p_t}; weights; counts | (D.12)-(D.14) | R, T (36,084 crossing pairs; 42 count cases) |
| O5 | identity (D.16) and the child network | D.4.6 | R, T (110/110 node-trials, one packet, L <= 8) |
| O6 | children admissible (A1)-(A5) | D.4.6, (D.11) | R; M (A5), thresholds in section 5 |
| O7 | interpolation points and unit differences | D.4.1, D.4.4 | R |
| O8 | complexity recurrence | D.4.7 | R, M |
| O9 | tuple counting bound | (D.15) | R, T |
| O10 | canonical lifting consistency | D.4.1 | R; T on an abstract bookkeeping model (added 2026-10-29, `harness/eth_o10_counter_model/`) |

## 5. The quantifier "for all sufficiently large s" made numerical (not a proof; log-domain evaluation with worst-case M)
- (P1)-(P5) hold at every active depth from lambda_2 = 2.10e6 (C = 12) / 8.39e6 (C = 144), bound by u_d >= 1 at the last depth (u_{d*-1} = floor(eps lambda/2^{d*-1}) >= 1).
- (P6) (the claim p_t = O(M D_t/u) with leading constant 24) holds from lambda_1 = 2.94e7 (C = 12) / 6.71e7 (C = 144) at every depth.
- Both are far below the literal "u >= lambda^{4/5}" of (D.5) (which would need lambda >= 2^546+) and below Lemma 4.8's thresholds (1.1e10-1.4e11) needed for the Section 5/6 parameters. For lambda below these thresholds the paper's fallback (exhaustive search) applies.

## 6. What this lemma makes visible (differences from the paper's text)
1. The recursion is run on tagged networks with entries in A_p, a strict generalization of the stated hypothesis (entries in B_{P0,ell}). **[added]**
2. Correctness of each call is the statement "output = Z(N) mod 2^p" for the *lifted* tensors; the root case coincides with the true contraction. Nothing in the paper contradicts this reading; the sentence "reducing F(0) modulo the call's precision gives the required answer" is exactly step 2/3 plus this definition. **[added]**
3. The child's two sides are (retained vertices, packet vertices), not (rows, columns) of the parent; Lemma D.3 is applied afresh to the child with that orientation. **[added]**
4. The parameter schedule depends on d only, while "active" depends on M > H; (A1) makes the two consistent (active at depth d implies d < d*).
5. Complexity uses (P6), correctness does not; so the induction is valid for all lambda satisfying (P1)-(P5) even if the running time is not controlled there.

## 7. Not covered
Lemma D.3-D.5, (D.12)-(D.16) were tested only at tiny L, p (a <= 4, p <= 5); the induction itself was never *run* (the tuple count at toy parameters exceeds 10^108). O10 (canonical lifting) was read, and since tested only on an abstract bookkeeping model (see `harness/eth_o10_counter_model/`). This reconstruction has not been reviewed by anyone else, and a Lean or independent formalization would be the way to settle it.
