"""Which of the draft's numbers and quotations occur in the arXiv preprint of the paper it reads?
Run: python3 -I paper_checks.py /path/to/2604.09200v1.pdf        (needs pdftotext; the PDF is not stored here)
The draft reads the published PNAS article (a later version than the preprint). This script is the only primary-source
re-check available when the draft was prepared (the publisher refuses automated fetches): FOUND means the string occurs in
the preprint's text layer (whitespace-normalised); NOT FOUND means it does not, which is a finding about versions, not an error."""
import hashlib, re, subprocess, sys
pdf = sys.argv[1]
print("preprint sha256", hashlib.sha256(open(pdf, "rb").read()).hexdigest())
norm = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout)
groups = {
 "sample flows (finding 7)": ["8,412", "339", "73 failed the attention check", "10,317", "301", "66 failed the attention check", "14,779", "17,950", "8,000", "9,950"],
 "headline effects (findings 4, 6)": ["12.8", "+19.7 percentage points on petition signing", "16.2 to +23.7", "7.5pp range"],
 "condition-level correlations (findings 1, 2)": ["r = 0.05, p = 0.85", "r = 0.18, p = 0.68", "r = 0.87", "r = −0.15, p = 0.59", "r = −0.16, p = 0.70", "r = 0.44, p = 0.10", "r = 0.63, p = 0.10", "Study 1 (15 conditions)", "(8 strategies)"],
 "wording the draft quotes (findings 1, 4)": ["we observed no evidence of a correlation", "AI persuasion effects on attitudes and behaviour are uncorrelated", "effects on petition support spanned an order of magnitude", "relatively narrow range", "Wald χ2 (7) = 22.42, p = .002", "relatively low"],
 "design and reporting (findings 5, 7)": ["Study 1 was preregistered on AsPredicted; Study 2 on the Open Science Framework", "Benjamini–Hochberg", "fluoride, recycling, antibiotics, or artificial sweeteners", "£12", "Stop Rising Child Poverty"],
 "expected absent from the preprint (published-version or SI content)": ["+0.19", "−0.04", "25.2", "21.1", "37.8", "40.4", "39.2", "33.4", "0.1%", "62 to 94", "act of being asked", "scalab", "demand effect"],
}
for g, items in groups.items():
    print(f"\n[{g}]")
    for it in items:
        c = len(re.findall(re.escape(it), norm))
        print(f"  {'FOUND    ' if c else 'NOT FOUND'}  {it!r}" + (f"  (x{c})" if c else ""))
