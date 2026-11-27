"""Quote check for the reading: every quoted string in the reading must occur in the paper's text layer.
Usage: python3 quote_checks.py <pdf_text_file> ; the PDF is not stored here (sha256 in the output).
Normalisation: unicode NFKC, join line breaks, collapse whitespace, remove hyphenation at line ends."""
import sys, re, unicodedata
txt = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'-\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()
T = norm(txt)
QUOTES = [
 "We propose a background independent quantization of vacuum general relativity on four dimensional Lorentzian spacetimes.",
 "for which this algebra generates a type I factor",
 "each sum over intermediate states converges absolutely",
 "with a given maximum size has a finite dimensional Hilbert space",
 "We end by deriving the semiclassical Einstein equations to one loop as the low energy limit of this theory.",
 "Several of the calculations and proofs in this paper were developed through detailed, back and forth collaboration with",
 "amounting to ∼ 400M total tokens spent",
 "In Appendix C.2 we argue that (4.27) is finite on a dense set of wavefunctions, as required for it to define a self adjoint clock operator",
 "is a heuristic for the noncommuting operators in (4.26)",
 "We defer to future work whether different choices of ω in Section 4.2 yield unitarily equivalent representations",
 "this provides strong evidence at finite GN and ℏ that",
 "Since we choose a pure extension",
 "we can choose a pure state ω on A",
 "even though expanding first in GN yields a logarithmic divergence",
 "recovering at one loop the coefficient",
 "when the Euclidean cylinder has finite trace",
 "quantization requires a symplectic area of order",
 "on the smooth background as in Section 5.2",
 "these estimates bound the number of modes",
 "at one loop by bounding the number of graviton states",
 "This is incompatible with the positive right hand side",
 "Both subtracted two point functions have a finite coincidence limit at S",
]
import hashlib
print('quote check against', sys.argv[1])
missing = 0
for q in QUOTES:
    ok = norm(q) in T
    missing += (not ok)
    print(('FOUND   ' if ok else 'MISSING ') + q[:110])
print(f'{len(QUOTES)-missing}/{len(QUOTES)} quoted strings found in the PDF text layer')
