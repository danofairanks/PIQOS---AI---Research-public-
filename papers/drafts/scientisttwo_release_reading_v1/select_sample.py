"""Reproduces the hash selection rule: for each domain directory, the PDF whose sha256(filename) is smallest.
Usage: python3 select_sample.py <path to generated-papers/> deep_learning general_ml optimization probabilistic social_aspects theory"""
import hashlib, os, sys
root = sys.argv[1]
for d in sys.argv[2:]:
    files = sorted(os.listdir(os.path.join(root, d)))
    h = sorted((hashlib.sha256(f.encode()).hexdigest(), f) for f in files)
    print(d, h[0][1], h[0][0][:10], len(files))
