"""Independent exact re-evaluation of the Ramsey-multiplicity construction in BakeLab/Epi-results@97fa6a4
(mathematics/ramsey-c45/construction.graph6, a 1,024-vertex graph).  Own graph6 decoder and clique counter (cliq.c).
Usage: python3 -I ramsey_check.py DIR   (DIR holds construction.graph6 and a copy of cliq.c (cliq.c is in this folder); needs gcc; runs in a temporary copy)
Objective (from the repository README): t(K4,W) + t(K5,1-W) for the graphon W of the graph, with the complement taken with loops."""
import sys, os, subprocess, tempfile, shutil
from fractions import Fraction
src = sys.argv[1].rstrip('/') + '/'
g6 = open(src + 'construction.graph6').read().strip()
b = [ord(c) - 63 for c in g6]
if b[0] != 63:
    n = b[0]; data = b[1:]
else:
    n = (b[1] << 12) | (b[2] << 6) | b[3]; data = b[4:]
bits = ''.join(format(x, '06b') for x in data)
A = [[0] * n for _ in range(n)]
k = 0
for j in range(1, n):
    for i in range(j):
        if bits[k] == '1': A[i][j] = A[j][i] = 1
        k += 1
edges = sum(map(sum, A)) // 2
print('n =', n, ' edges =', edges)
tmp = tempfile.mkdtemp()
open(tmp + '/adj.txt', 'w').write('\n'.join(''.join(map(str, r)) for r in A) + '\n')
shutil.copy(src + 'cliq.c', tmp + '/cliq.c')
subprocess.run(['gcc', '-O2', '-o', tmp + '/cliq', tmp + '/cliq.c'], check=True)
run = lambda *a: [int(x) for x in subprocess.run([tmp + '/cliq', *a], cwd=tmp, capture_output=True, text=True, check=True).stdout.split()]
G = run(); Gc = run('c')
print('G cliques K1..K5:', G); print('complement cliques K1..K5:', Gc)
K4 = G[3]
hom5 = 1 * Gc[0] + 15 * 2 * Gc[1] + 25 * 6 * Gc[2] + 10 * 24 * Gc[3] + 120 * Gc[4]
obj = Fraction(24 * K4, n ** 4) + Fraction(hom5, n ** 5)
print('objective =', obj, '=', float(obj))
print('equals 4427841832181/2^49:', obj == Fraction(4427841832181, 2 ** 49))
print('published comparison 2129191/2^28 =', float(Fraction(2129191, 2 ** 28)), '; improved:', obj < Fraction(2129191, 2 ** 28))
inj = Fraction(24 * K4, n ** 4) + Fraction(120 * Gc[4], n ** 5)
print('injective-only variant (no loops) would give', float(inj))
shutil.rmtree(tmp)
