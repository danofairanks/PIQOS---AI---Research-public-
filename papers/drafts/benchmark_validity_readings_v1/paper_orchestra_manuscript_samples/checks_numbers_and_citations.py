# Checks for the four gallery manuscripts. Third-party text is not stored here. To reproduce:
#  1. fetch the two source papers (arXiv:2403.13778 for the trajectory-prediction source, arXiv:2406.15079 for the optimisation source), pdftotext -layout each;
#  2. read each gallery page image into text (OCR; transcription errors exist), one text file per manuscript;
#  3. run the functions below. Image hashes are in the README.
import re
def body(t):
    t=re.sub(r'===== PAGE \d+ =====','',t); t=re.sub(r'-\n','',t); return re.sub(r'\s+',' ',t)
def trim(t):
    for k in ('REFERENCES','References'):
        if k in t: return t[:t.rfind(k)]
    return t
def decimals(t): return set(re.findall(r'(?<![\d.])\d+\.\d+%?(?![\d.])',t))
def fidelity(sample_text, source_text):
    s=decimals(source_text); s|={x.rstrip('%') for x in s}
    t=decimals(trim(body(sample_text)))
    un=sorted(x for x in t if x.rstrip('%') not in s)
    return len(t),len(t)-len(un),un
# Recorded results (this run):
RECORDED = {
 'trajectory-style, plots off': (53,51,['0.03 (derived: 0.1 - 0.07)','2.00 (source prints 2.0)']),
 'trajectory-style, plots on' : (57,47,['ten figure-axis tick labels and 2.00']),
 'optimisation-style, plots off': (125,120,['OCR splits and section numbers']),
 'optimisation-style, plots on' : (111,105,['OCR splits and section numbers']),
}
# Single-task vs multi-task cells in the optimisation-style manuscript's Table 1 (gap %, single, multi): multi-task worse in every cell.
CELLS=[(0.30,0.91),(2.34,3.16),(2.61,3.82),(-0.04,0.43),(0.10,0.12),(0.23,0.37),(2.82,3.84),(2.73,4.13)]
if __name__=='__main__':
    print('multi-task worse than single-task in %d of %d cells; mean extra gap %.2f points'%(sum(m>s for s,m in CELLS),len(CELLS),sum(m-s for s,m in CELLS)/len(CELLS)))
    for k,(n,f,u) in RECORDED.items(): print(k,'decimal tokens',n,'found in source',f,'not found',u)
    print('Table 1 of the trajectory-style manuscripts: four smoothed-model rows identical to the source (1.26/2.27/8.0/46; 1.23/2.0/9.0/49; 1.17/2.05/9.3/53; 1.14/2.07/10.6/57); Tables 2-6 identical')
    print('source preprints (arXiv listings): 2024-03-20 and 2024-06-21; pipeline research cutoffs per the paper: Nov 2024 and Oct 2024')
    print('citations: 12/12 arXiv-identified references resolve with matching titles in each of two reference lists checked; name glitches in two entries; one relevant-looking but irrelevant citation (a driving-motion transformer cited for routing solvers)')
